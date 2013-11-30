from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Button import Button
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ActionMap import NumberActionMap, ActionMap
from Components.config import *
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Tools.Directories import fileExists
from Components.PluginList import * 
from Components.Sources.List import List 
from Plugins.Plugin import PluginDescriptor 
from Components.PluginComponent import plugins 
from Screens.Setup import Setup
import os

from EGAMI.EGAMI_tools import *
from EGAMI.EGAMI_skins import *

class EgamiGreenPanel:
	def __init__(self):
		self["EgamiGreenPanel"] = ActionMap( [ "InfobarSubserviceSelectionActions" ],
			{
				"EgamiGreenPanelShow": (self.showEgamiGreenPanel),
			})

	def showEgamiGreenPanel(self):
		self.session.openWithCallback(self.callEgAction, EGGreenPanel)

	def callEgAction(self, *args):
		if len(args):
			(actionmap, context, action) = args
			actionmap.action(context, action)
			
class EGExtrasMenu(Screen):
	def __init__(self, session):
		self.skin = EGExtrasMenu_Skin
		Screen.__init__(self, session)
		self.list = []
		self["list"] = List(self.list)
		self.updateList()
		self["actions"] = ActionMap(["WizardActions",
		"ColorActions"], {"ok": self.KeyOk,
		"back": self.close})
		
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		self.sel = self.sel[2]
		if (self.sel == 0):
			from EGAMI.EGAMI_panel import EGSwapManager
			self.session.open(EGSwapManager)
		elif (self.sel == 1):
			from EGAMI.EGAMI_panel import EGNetBrowser
			self.session.open(EGNetBrowser)
		elif (self.sel == 2):
			self.session.open(Setup, "epgsettings")
		elif (self.sel == 3):
			from EGAMI.EGAMI_devices_menu import EGDeviceManager
			self.session.open(EGDeviceManager)
		elif (self.sel == 4):
			from EGAMI.EGAMI_services import EGServicesMenu
			self.session.open(EGServicesMenu)
		elif (self.sel == 5):
			from Screens.EGAMI_wizard import EGAMIWizardSetup
			self.session.open(EGAMIWizardSetup)
		elif (self.sel == 6):
			from EGAMI.EGAMI_infobar_setup import EGInfoBarSetup
			self.session.open(EGInfoBarSetup)
		elif (self.sel == 7):
			from EGAMI.EGAMI_panel import DvbSnoop
			self.session.open(DvbSnoop)
		elif (self.sel == 8):
			from EGAMI.EGAMI_panel import EGProcessInfo
			self.session.open(EGProcessInfo)
		elif (self.sel == 9):
			from EGAMI.EGAMI_panel import EGKernelInfo
			self.session.open(EGKernelInfo)
		elif (self.sel == 10):
			from EGAMI.EGAMI_panel import EGEnigma2ConfigInfo
			self.session.open(EGEnigma2ConfigInfo)
		elif (self.sel == 11):
			self.session.open(Setup, "recording")
		elif (self.sel == 12):
			self.session.open(Setup, "subtitlesetup")
		elif (self.sel == 13):
			self.session.open(Setup, "autolanguagesetup")
		elif (self.sel == 14):
			from EGAMI.EGAMI_panel import EGSetupHttpStream
			self.session.open(EGSetupHttpStream)
		else:
			self.noYet()

	def noYet(self):
		nobox = self.session.open(MessageBox, _("Function Not Yet Available"), MessageBox.TYPE_INFO)
		nobox.setTitle(_("Info"))

	def updateList(self):
		self.list = []
		mypath = resolveFilename(SCOPE_CURRENT_SKIN)
		if not fileExists(mypath + "egami_icons"):
			mypath = "/usr/share/enigma2/skin_default/"

		mypixmap = (mypath + "egami_icons/swap_manager.png")
		png = LoadPixmap(mypixmap)
		name = (_("Swap File Settings"))
		desc = (_("Manage Your swapfile..."))
		idx = 0
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/mount_manager.png")
		png = LoadPixmap(mypixmap)
		name = (_("Mount Manager"))
		desc = (_("Manage Your network share..."))
		idx = 1
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/epg_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("EPG settings"))
		desc = (_("Configure internal epg..."))
		idx = 2
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/device_manager.png")
		png = LoadPixmap(mypixmap)
		name = (_("Devices Manager"))
		desc = (_("Manage Your devices like USB, HDD, DVD..."))
		idx = 3
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/services_manager.png")
		png = LoadPixmap(mypixmap)
		name = (_("Services Panel"))
		desc = (_("Manage Inadyn, SSH, uShare, OpenVPN, NFS..."))
		idx = 4
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/decoding_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("EGAMI Wizard"))
		desc = (_("Fast enable / disable function..."))
		idx = 5
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/osd_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("OSD Settings"))
		desc = (_("Setup an additional OSD settings..."))
		idx = 6
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/stream_info.png")
		png = LoadPixmap(mypixmap)
		name = (_("Stream Informations"))
		desc = (_("Additional stream informations..."))
		idx = 7
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/proc_info.png")
		png = LoadPixmap(mypixmap)
		name = (_("Process Informations"))
		desc = (_("Kill, manage all running processes..."))
		idx = 8
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/kernel_info.png")
		png = LoadPixmap(mypixmap)
		name = (_("Kernel Informations"))
		desc = (_("Show kernel messages..."))
		idx = 9
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/e2config_info.png")
		png = LoadPixmap(mypixmap)
		name = (_("GUI Config Informations"))
		desc = (_("Show gui2 config informations..."))
		idx = 10
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/recording_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("Recording settings"))
		desc = (_("Configure default path for recording..."))
		idx = 11
		res = (name,png,idx,desc)
		self.list.append(res)
	  
		mypixmap = (mypath + "egami_icons/subtitle_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("Subtitles settings"))
		desc = (_("Configure subtitle color, size, position..."))
		idx = 12
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/language_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("Auto language settings"))
		desc = (_("Config default audio language..."))
		idx = 13
		res = (name,png,idx,desc)
		self.list.append(res)   

		mypixmap = (mypath + "egami_icons/http_settings.png")
		png = LoadPixmap(mypixmap)
		name = (_("HTTP Stream settings"))
		desc = (_("Configure http stream..."))
		idx = 14
		res = (name,png,idx,desc)
		self.list.append(res)

		self["list"].list = self.list
	
class EGGreenPanel(Screen):
	def __init__(self, session):
		self.skin = EGGreenPanel_Skin
		Screen.__init__(self, session)
		self.list = []
		self["list"] = List(self.list)
		self["key_red"] = Label(_("Addons"))
		self["key_green"] = Label(_("Extras"))
		self["key_yellow"] = Label(_("File Manager"))
		self["key_blue"] = Label(_("Scripts"))
		self.updateList()
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
		'ok': self.save,
		'back': self.close,
		'red': self.Addons,
		'yellow': self.File,
		'green': self.Extras,
		'blue': self.Script
		}, -1)
	    
	def save(self):
		self.run()
	    
	def run(self):
		mysel = self["list"].getCurrent()
		if mysel:
			plugin = mysel[3]
			plugin(session=self.session)
	
	def updateList(self):
		self.list = [ ]
		self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
		for plugin in self.pluginlist:
			if plugin.icon is None:
				png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/icons/plugin.png"))
			else:
				png = plugin.icon
			res = (plugin.name, plugin.description, png, plugin)
			self.list.append(res)
		
		self["list"].list = self.list

	def reloadPluginList(self):
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.updateList()
		
	def Addons(self):
		m = checkkernel()
		if m == 1:
			from EGAMI.EGAMI_addon_manager import EGAddonMenu
			self.session.openWithCallback(self.reloadPluginList, EGAddonMenu)
		else:
			self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
			
	def File(self):
		    m = checkkernel()
		    if m == 1:
			from EGAMI.EGAMI_filemanager import EGFileManager
			self.session.open(EGFileManager)
		    else:
		      self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
		      
	def Script(self):
		m = checkkernel()
		if m == 1:
			from EGAMI.EGAMI_panel import SmartScript
			self.session.open(SmartScript)
		else:
			self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
		
	def Extras(self):
		m = checkkernel()
		if m == 1:
			self.session.open(EGExtrasMenu)
		else:
			self.session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash EGAMI Image'), MessageBox.TYPE_INFO, 3)
