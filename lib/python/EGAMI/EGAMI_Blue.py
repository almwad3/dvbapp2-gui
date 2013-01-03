# -*- coding: utf-8 -*-
from enigma import eTimer, gFont, loadPNG, eListboxPythonMultiContent, iServiceInformation
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Button import Button
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Pixmap import MultiPixmap
from Components.ActionMap import NumberActionMap, ActionMap
from Components.config import *
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from ServiceReference import ServiceReference
from Tools.Directories import fileExists, pathExists
from os import system, listdir
from Components.PluginList import * 
from Components.Sources.List import List 
from Plugins.Plugin import PluginDescriptor 
from Components.PluginComponent import plugins 
from Components.Console import Console

import os
from xml.dom import minidom

from EGAMI.EGAMI_tools import *
from EGAMI.EGAMI_skins import EGExecute_Skin, EGEmuInfoScript_Skin, EGEmuManager_Skin, EGEmuManagerStarting_Skin
from EGAMI.EGAMI_Green import EGExtrasMenu
from os import popen, listdir


class EgamiBluePanel:
	def __init__(self):
		self["EgamiBluePanel"] = ActionMap( [ "InfobarExtensions" ],
			{
				"EgamiBluePanelShow": (self.showEgamiBluePanel),
			})

	def showEgamiBluePanel(self):
		self.session.openWithCallback(self.callEgAction, EmuManager)

	def callEgAction(self, *args):
		if len(args):
			(actionmap, context, action) = args
			actionmap.action(context, action)

class EGExecute(Screen):
	def __init__(self, session, name, command):
		self.skin = EGExecute_Skin
		Screen.__init__(self, session)

		self.name = name
		self.onShown.append(self.setWindowTitle)

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"ok": self.close,
			"cancel": self.close
		}, -1)

		pipe = popen('{ ' + command + '; } 2>&1', 'r')
		self.linelist = pipe.readlines()
		result = pipe.close()

		self.offset = 0
		self.maxoffset = 0
		for x in self.linelist:
			if len(x) > self.maxoffset:
				self.maxoffset = len(x)

		self["linelist"] = MenuList(list=[], enableWrapAround=True)
		self.setList()

	def setWindowTitle(self):
		self.setTitle(self.name)

	def setList(self):
		if self["linelist"] is not None:
			if self.offset > 0:
				list = []
				for line in self.linelist:
					list.append(line[self.offset:len(line)])
				self["linelist"].setList(list)
			else:
				self["linelist"].setList(self.linelist)
			
class EGEmuInfoScript(Screen):
	__module__ = __name__
	def __init__(self, session):
		self.skin = EGEmuInfoScript_Skin
		Screen.__init__(self, session)
		self['statuslab'] = Label(_('N/A'))
		self.mlist = []
		self.populateSL()
		self['list'] = MenuList(self.mlist)
		self['list'].onSelectionChanged.append(self.schanged)
		self['actions'] = ActionMap(['WizardActions',
		'ColorActions'], {'ok': self.mygo,
		'back': self.close})
		self.onLayoutFinish.append(self.refr_sel)

	def refr_sel(self):
		self['list'].moveToIndex(1)
		self['list'].moveToIndex(0)

	def populateSL(self):
		self.scriptdesc = {}
		myscripts = listdir('/usr/scripts')
		for fil in myscripts:
		    if (fil.find('_emuinfo.sh') != -1):
			fil2 = fil[:-11]
			desc = 'N/A'
			f = open(('/usr/scripts/' + fil), 'r')
			for line in f.readlines():
				if (line.find('#DESCRIPTION=') != -1):
					line = line.strip()
					desc = line[13:]

			f.close()
			self.mlist.append(fil2)
			self.scriptdesc[fil2] = desc

	def schanged(self):
		mysel = self['list'].getCurrent()
		mytext = (' ' + self.scriptdesc[mysel])
		self['statuslab'].setText(mytext)

	def mygo(self):
		mysel = self['list'].getCurrent()
		mysel2 = (('/usr/scripts/' + mysel) + '_emuinfo.sh')
		mytitle = (_('EmuInfo Tool: ') + mysel)
		self.session.open(EGExecute, _(mytitle), mysel2)
	

class EGSoftCamInfo(Screen):
    skin = """<screen name="EGSoftCamInfo" position="center,center" size="400,310" title="EGAMI Softcam Info" >
      			<widget name="menu" position="10,10" size="340,280" scrollbarMode="showOnDemand" />
		</screen>"""
    def __init__(self, session, args = 0):
	Screen.__init__(self, session)
        self.menu = args
        list = []
        
	if pathExists('/usr/emu_scripts/'):
		softcams = listdir('/usr/emu_scripts/')
		for softcam in softcams:
			if softcam.lower().startswith('cccam') :
			    list.append((_("CCcam Info"), "1"))
	if pathExists('/usr/emu_scripts/'):
		softcams = listdir('/usr/emu_scripts/')
		for softcam in softcams:
			if softcam.lower().startswith('oscam') :
			    list.append((_("OScam Info"), "2"))			    
	if pathExists('/usr/emu_scripts/'):
		softcams = listdir('/usr/emu_scripts/')
		for softcam in softcams:
			if softcam.lower().startswith('wicardd') :
			    list.append((_("Wicardd Info"), "3"))
			    

	list.append((_("User Scripts Info"), "4"))
        self["menu"] = MenuList(list)
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"],{"ok": self.go,"back": self.close,}, -1)
        
    def go(self):
        returnValue = self["menu"].l.getCurrentSelection()[1]
        if returnValue is not None:
           if returnValue is "1":
		from Screens.CCcamInfo import CCcamInfoMain
		self.session.open(CCcamInfoMain)
	   elif returnValue is "2":
		from Screens.OScamInfo import OscamInfoMenu
		self.session.open(OscamInfoMenu)
	   elif returnValue is "3":
		from EGAMI.WicarddInfo import EGAMIWicarddMain
		self.session.open(EGAMIWicarddMain)
	   elif returnValue is "4":
		self.session.open(EGEmuInfoScript)

 	       
class EmuManager(Screen):
	def __init__(self, session):
		self.skin = EGEmuManager_Skin
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
			{
				"left": self.keyLeft,
				"right": self.keyRight,
				"ok": self.restart_all,
				"cancel": self.cancel,
				"red": self.restart_all,
				"green": self.emuextended,
				"yellow": self.settings,
				"blue": self.check
			},-1)
		
		self.softcamchoices = []
		self.createConfig()
		self['config'] = MenuList(self.softcamchoices)
		self.createSetup()
		self.onShow.append(self.createSetup2)
		
	def createConfig(self):
		fsock = open('/usr/tuxbox/config/emulist.xml')
		xmldoc = minidom.parse(fsock)
		fsock.close()

		if fileExists('/usr/tuxbox/config/emulist.xml'):
			lista_emu = xmldoc.getElementsByTagName('emu')
			for lista in lista_emu:
				emulator2 = lista.getAttribute("emulator")
				emulator = str(emulator2)
				self.softcamchoices.append(emulator)
				str(emulator)
		else:
			print "Sorry, /usr/tuxbox/config/emulist.xml does not exist !"

	
	def createSetup(self):
		self["key_red"] = Label(_("Save"))
		self["choose_cam"] = Label(_("Set Default CAM"))
		self["key_green"] = Label(_("Info"))
		self["key_yellow"] = Label(_("EPG Panel"))
		self["key_blue"] = Label(_("EGAMI Panel"))
		
		try:
			service = self.session.nav.getCurrentService()
			info = service and service.info()
			videosize = str(info.getInfo(iServiceInformation.sVideoWidth)) + "x" + str(info.getInfo(iServiceInformation.sVideoHeight))
			aspect = info.getInfo(iServiceInformation.sAspect)
			if aspect in ( 1, 2, 5, 6, 9, 0xA, 0xD, 0xE ):
				aspect = "4:3"
			else:
				aspect = "16:9"
				
			provider = info.getInfoString(iServiceInformation.sProvider)
			chname = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
			self["lb_provider"] = Label(_('Provider: ') + provider)
			self["lb_channel"] = Label(_('Name: ') + chname)
			self["lb_aspectratio"] = Label(_('Aspect Ratio: ') + aspect)
			self["lb_videosize"] = Label(_('Video Size: ') + videosize)
		except:
			self["lb_provider"] = Label(_('Provider: n/a'))
			self["lb_channel"] = Label(_('Name: n/a'))
			self["lb_aspectratio"] = Label(_('Aspect Ratio: n/a'))
			self["lb_videosize"] = Label(_('Video Size: n/a'))
									
		self["ecminfo"] = Label(readEcmFile())
		

	def createSetup2(self):
		try:
			fp = open("/etc/egami/.emunumber", "r")
			emuLine = fp.readline()
			fp.close()
			emuLine = emuLine.strip("\n")
		except:
			"0"
			
		self["config"].moveToIndex(int(emuLine)-1)
		
		
	def keyLeft(self):
		self["config"].up()

	def keyRight(self):
		self["config"].down()
		
	def settings(self):
		m = checkkernel()
		if m == 1:
			from Plugins.SystemPlugins.CrossEPG.crossepg_menu import CrossEPG_Menu
			self.session.open(CrossEPG_Menu)
		else:
			self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
		  
	def check(self):
	  	m = checkkernel()
		if m == 1:
		  self.session.open(EGExtrasMenu)
		else:
		  self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
		  	
	def cleanup(self):
		os.system("rm /tmp/*.tmp && rm /tmp/hyper* && rm /tmp/gbox*")

	def myclose(self):
		self.close()
		
	def restart_all(self):
	  	m = checkkernel()
		if m == 1:
			self.cleanup()
			emuname = self["config"].getCurrent()
			index = self["config"].getSelectedIndex()
			index = str(index+1)
			if index is not None:
				try:
					emunumber_file = open('/var/etc/egami/.emunumber', 'w')
					emunumber_file.write(index)
					emunumber_file.close()
				except:
					pass
			try:
				emuname_file = open('/var/etc/egami/.emuname', 'w')
				emuname_file.write(emuname)
				emuname_file.close()
			except:
				pass
			
			sendCmdtoEGEmuD('STARTALL') #sendCmdtoEGEmuD('RESTARTEMU') sendCmdtoEGEmuD('RESTARTCS')
			self.session.openWithCallback(self.myclose, EGEmuManagerStarting, emuname)		
			unload_modules(__name__)
		else:
			self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
				
	def emuextended(self):
	  	m = checkkernel()
		if m == 1:
			self.session.open(EGSoftCamInfo)
		else:
			self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
		  
		  
	def cancel(self):
		unload_modules(__name__)
		self.close()
		


class EGEmuManagerStarting(Screen):
	def __init__(self, session, title):
		self.skin = EGEmuManagerStarting_Skin
		Screen.__init__(self, session)
		msg = ((_('Please wait while starting\n')) + title + '...')
		self['starting'] = MultiPixmap()
		self['text'] = Label(msg)
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.updatepix)
		self.onShow.append(self.startShow)
		self.onClose.append(self.delTimer)

	def startShow(self):
		self.curpix = 0
		self.count = 0
		self['starting'].setPixmapNum(0)
		self.activityTimer.start(10)

	def updatepix(self):
		self.activityTimer.stop()
		if self.curpix > 9:
			self.curpix = 0
		if self.count > 24:
			self.curpix = 10
		self['starting'].setPixmapNum(self.curpix)
		if self.count == 35:
			self.hide()
			self.close()
		self.activityTimer.start(140)
		self.curpix += 1
		self.count += 1

	def delTimer(self):
		del self.activityTimer

