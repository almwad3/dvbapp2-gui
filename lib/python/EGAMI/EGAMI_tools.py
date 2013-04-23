# -*- coding: utf-8 -*-
from Components.Label import Label
from Components.config import config, configfile
from Screens.Screen import Screen 
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_SKIN, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap, pixmap_cache
from os import path as os_path
from enigma import eConsoleAppContainer
import re, string
import os
from socket import *
import socket
from Components.About import about


def checkkernel():
	mycheck = 0
	if not fileExists("/media/usb"):
		os.system("mkdir /media/usb")
	if (os.path.isfile("/proc/stb/info/boxtype") and os.path.isfile("/proc/stb/info/version")): 
		if open("/proc/stb/info/boxtype").read().startswith("ini-10" or open("/proc/stb/info/boxtype").read().strip() == "ini-3000" or open("/proc/stb/info/boxtype").read().startswith("ini-50") or open("/proc/stb/info/boxtype").read().startswith("ini-70"):
			if (about.getKernelVersionString()=="3.6.0"):
				mycheck = 1
	else:
	  mycheck = 0
	  
	return mycheck
	
def getExpertInfo(theId):
        expertString = " "
        fileString = ""
        try:
            fp = open("/tmp/share.info", "r")
            while 1:
                currentLine = fp.readline()
                if (currentLine == ""):
                    break
                foundIdIndex = currentLine.find(("id:" + theId))
                if (foundIdIndex is not -1):
                    fileString = currentLine
                    break

            atIndex = fileString.find(" at ")
            cardIndex = fileString.find(" Card ")
            if ((atIndex is not -1) and (cardIndex is not -1)):
                addy = fileString[(atIndex + 4):cardIndex]
                addyLen = len(addy)
                #if (addyLen > 15):
                #   addy = ((addy[:9] + "*") + addy[(addyLen - 5):])
                expertString = (expertString + addy)
            expertString = ((expertString + "  BoxId:") + theId)
            distIndex = fileString.find("dist:")
            if (distIndex is not -1):
                expertString = (((expertString + " ") + "D:") + fileString[(distIndex + 5)])
            levelIndex = fileString.find("Lev:")
            if (levelIndex is not -1):
                expertString = (((expertString + " ") + "L:") + fileString[(levelIndex + 4)])
        except:
            print "Nothing more found...not gbox???"
        return expertString
	    	
def parse_ecm():
	addr = caid =  pid =  provid =  port = ""
	source =  ecmtime =  hops = 0
	try:
		file = open ('/tmp/ecm.info')
		for line in file.readlines():
			line = line.strip()
			if line.find('CaID') >= 0:
				x = line.split(' ')
				caid = x[x.index('CaID')+1].split(',')[0].strip()
			elif line.find('caid') >= 0:
				x = line.split(':',1)
				caid = x[1].strip()
			if line.find('pid:') >= 0:
				x = line.split(':',1)
				pid = x[1].strip()
			elif line.find('pid') >= 0:
				x = line.split(' ')
				pid = x[x.index('pid')+1].strip()
			if line.find('prov:') >= 0:
				x = line.split(':',1)
				provid = x[1].strip().split(',')[0]
			elif line.find('provid:') >= 0:
				x = line.split(':',1)
				provid = x[1].strip()
			if line.find('msec') >= 0:
				x = line.split(' ',1)
				ecmtime = int(x[0].strip())
			elif line.find('ecm time:') >= 0:
				x = line.split(':',1)
				ecmtime = int(float(x[1].strip()) * 1000)
			if line.find('hops:') >= 0:
				x = line.split(':',1)
				hops = int(x[1].strip())
			if line.find('using:') >= 0: # CCcam
				x = line.split(':',1)
				if (x[1].strip() == "emu"):
					source = 1
				elif (x[1].strip() == "net") or (x[1].strip() == "newcamd") or (x[1].strip() == "CCcam-s2s"):
					source = 2
			if line.find('from:') >= 0: # oscam
				x = line.split(':',1)
				addr = x[1].strip()
				source = 2
			elif line.find('source:') >= 0: #MgCamd
				x = line.split(':')
				if x[1].strip() == "emu":
					source = 1
				elif x[1].find("net") >= 0:
					source = 6 #GBox MgCamd
					port = x[2].strip().split(")")[0]
					addr = x[1].split(' ')[4]
				elif x[1].strip() == "newcamd":
					source = 6
			elif line.find('address:') >= 0: # CCcam
				x = line.split(':')
				if x[1].strip() != '':
					if x[1].find("/dev/sci0") >= 0:
						source = 4
					elif x[1].find("/dev/sci1") >= 0:
						source = 5
					elif x[1].find("local") >= 0:
						source = 1
					else:
						try:
							addr = x[1].strip()
							port = x[2].strip()
						except:
							addr = x[1].strip()
			elif line.find('slot-1') >= 0: # Gbox
				source = 7
			elif line.find('slot-2') >= 0:
				source = 8
			elif line.find('decode:') >= 0: # Gbox
				if line.find('Internal') >= 0:
					source = 1
				elif line.find('Network') >= 0:
					currentLine = file.readline()
                            		currentLine = currentLine.replace("\n", "")
					boxidIndex = currentLine.find("prov:")
					boxidString = currentLine[(boxidIndex + 6):(boxidIndex + 10)]
					addr = getExpertInfo(boxidString)
					source = 6
		file.close()
		return caid, pid, provid, ecmtime, source, addr, port, hops
	except:
		return 0
				
def readEmuName():
	try:
		fp = open("/etc/egami/.emuname", "r")
		emuLine = fp.readline()
		fp.close()
		emuLine = emuLine.strip("\n")
		return emuLine
	except:
		"CI"
		
def readEcmFile():
	try:
		ecmfile = file('/tmp/ecm.info', 'r')
            	ecmfile_r = ecmfile.read()
            	ecmfile.close()
		return ecmfile_r
	except:
		"ECM Info not aviable!"
		
def sendCmdtoEGEmuD(cmd):
	try:
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.connect("/tmp/egami.socket")
		print '[EG-EMU MANAGER] communicate with socket'
		s.send(cmd)
		s.close()
	except socket.error:
		print '[EG-EMU MANAGER] could not communicate with socket'
		if s is not None:
			s.close()
				
def runBackCmd(cmd):
	eConsoleAppContainer().execute(cmd)

def getRealName(string):
        if string.startswith(" "):
            while string.startswith(" "):
                string = string[1:]

        return string

def hex_str2dec(str):
	ret = 0
	try:
		ret = int(re.sub("0x","",str),16)
	except:
		pass
	return ret

def norm_hex(str):
	return "%04x" % hex_str2dec(str)
 
    
##########################################################
# Ladowanie wartosci np LOG_NAME=nazwaloga
##########################################################
def loadcfg(plik, fraza, dlugosc):
	wartosc = '0'
	if fileExists(plik):
		f = open(plik, 'r')
		for line in f.readlines():
			line = line.strip()
			if (line.find(fraza) != -1):
				wartosc = line[dlugosc:]	
		f.close()
	
	return wartosc
	
##########################################################
# Ladowanie wartosci np INADYN=0 bool
##########################################################
def loadbool(plik, fraza, dlugosc):
	wartosc = '0'
	if fileExists(plik):
		f = open(plik, 'r')
		for line in f.readlines():
			line = line.strip()
			if (line.find(fraza) != -1):
				wartosc = line[dlugosc:]	
		f.close()
		
	if(wartosc == '1'):
		return True
	else:
		return False

			
##########################################################
# Wywalanie modolow
##########################################################
def unload_modules(name):
    try:
        from sys import modules 
        del modules[name]
    except:
        pass

##########################################################
# Szukanie frazy w czyms
##########################################################
def wyszukaj_in(zrodlo, szukana_fraza):
    wyrazenie = string.strip(szukana_fraza)
    for linia in zrodlo.xreadlines():
        if wyrazenie in linia:
            return True
    return False
    
##########################################################
# Szukanie czy jest skin w skin.xml
##########################################################

def wyszukaj_re(szukana_fraza):
    wyrazenie = re.compile(string.strip(szukana_fraza),re.IGNORECASE)
    zrodlo = open("/usr/share/enigma2/" + config.skin.primary_skin.value, 'r')
    for linia in zrodlo.xreadlines():
        if re.search(wyrazenie, linia) <> None:
            return True
    zrodlo.close()
    return False

