#!/usr/bin/python
# -*- coding: utf-8 -*-

# napiprojekt.pl API is used with napiproject administration consent

import sys
sys.path.append('/usr/lib/enigma2/python/EGAMI')

import EGAMI_pynapi
import EGAMI_subconv
import urllib2
import sys
import re
import os.path
from xml.etree import ElementTree as ET


def napiprojekt_fps(digest):
    url = "http://napiprojekt.pl/api/api.php?mode=file_info&client=dreambox&id=%s" % (urllib2.quote(digest))
    element = ET.parse( urllib2.urlopen(url)  )
    fps = element.find("video_info/fps").text
    return float(fps)

def read_sub(fmt, subs):
    if fmt == "tmp":
        return EGAMI_subconv.read_tmp(subs)
    elif fmt == "srt":
        return EGAMI_subconv.read_srt(subs)
    elif fmt == "sub2":
        return EGAMI_subconv.read_sub2(subs)
    elif fmt == "mpl2":
        return EGAMI_subconv.read_mpl2(subs)

def get_sub_from_napi(file):

	dest = file[:-4] + '.srt'
	
	print "Processing subtitle for:\n path: %s\n file: %s"  % os.path.split(file)
	digest = EGAMI_pynapi.calculate_digest(file)
	
	if digest:
		subs = EGAMI_pynapi.get_subtitle(digest).replace("\r","").split('\n')
		fmt = EGAMI_subconv.detect_format(subs)
		print "Subtitle format: ", fmt
		if fmt == "mdvd":
			fps = napiprojekt_fps(digest)
			print "FPS:", fps, " Convert to SRT utf8..."
			s = EGAMI_subconv.read_mdvd(subs, fps)
		else:
			s = read_sub(fmt, subs)
		
		subs = "".join(EGAMI_subconv.to_srt(s)).decode("CP1250").encode("utf-8-sig")

		dst = open( dest, 'w')
		dst.write(subs)
		dst.close()
	
		print "Saved:", dest

def get_all(file):
	rex = re.compile('.*\\.%s$' % file[-3:], re.I )
	
	(dir, fname) = os.path.split(file)

	for f in os.listdir(dir):
		if rex.match(f):
			try:
				get_sub_from_napi(os.path.join(dir, f))
			except:
				print "  Error: %s" % ( sys.exc_info()[1])

def lets_go(opt, file):		
  try:
    if opt == "get":
      get_sub_from_napi(file)
    if opt == "all":
      get_all(file)
  except:
    print "  Error: %s" % ( sys.exc_info()[1])
