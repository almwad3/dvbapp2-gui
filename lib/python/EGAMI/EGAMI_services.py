# -*- coding: utf-8 -*-
from Screens.Screen import Screen 
from Screens.MessageBox import MessageBox
from Screens.NetworkSetup import *

from Components.ActionMap import ActionMap 
from Components.Sources.List import List 

from Tools.Directories import fileExists, resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap

from EGAMI.EGAMI_services_config import *
from EGAMI.EGAMI_skins import EGServicesMenu_Skin, EGServices_Skin

class EGServicesMenu(Screen):
	def __init__(self, session):
		self.skin = EGServicesMenu_Skin
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
		    self.session.open(NetworkNfs)
		elif (self.sel == 1):
		  self.session.open(EGHttpd)
		elif (self.sel == 2):
		    self.session.open(NetworkInadyn)
		elif (self.sel == 3):
		    self.session.open(EGCronMang)
		elif (self.sel == 4):
		    from Plugins.Extensions.DLNABrowser.plugin import DLNADeviceBrowser
		    self.session.open(DLNADeviceBrowser)
		    #self.session.open(EGDjMountConfig)
		elif (self.sel == 5):	    
		    self.session.open(NetworkMiniDLNA)
		elif (self.sel == 6):
		    self.session.open(EGSyslogDConfig)
		elif (self.sel == 7):
		    self.session.open(NetworkSamba)
		elif (self.sel == 8):
		    self.session.open(NetworkOpenvpn)
		elif (self.sel == 9):
		    self.session.open(NetworkFtp)
		elif (self.sel == 10):
		    self.session.open(NetworkTelnet)
		elif (self.sel == 11):
		    self.session.open(EGPcscdConfig)
		elif (self.sel == 12):
		    self.session.open(EGDropbearConfig)
		elif (self.sel == 13):	    
		    self.session.open(NetworkuShare)
		else:
		    self.noYet()

	def noYet(self):
		nobox = self.session.open(MessageBox, _("Function Not Yet Available"), MessageBox.TYPE_INFO)
		nobox.setTitle(_("Info"))


	def updateList(self):
		self.list = []
		mypath = resolveFilename(SCOPE_CURRENT_SKIN)
		if not fileExists(mypath + "egami_icons"):
			mypath = "/usr/share/enigma2/"
		    

		mypixmap = (mypath + "egami_icons/nfsserver_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("NFS Server Panel"))
		desc = (_("Manage Your NFS Server..."))
		idx = 0
		res = (name,png,idx, desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/httpd_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("HTTPD Panel"))
		desc = (_("Manage Your little WWW web-apache"))
		idx = 1
		res = (name,png,idx, desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/inadyn_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("Inadyn Panel"))
		desc = (_("Manage Inadyn, simple dyndns updater..."))
		idx = 2
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/cron_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("Cron Panel"))
		desc = (_("Manage Your cron..."))
		idx = 3
		res = (name,png,idx, desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/djmount_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("DjMount Panel"))
		desc = (_("Manage Your UpNp Client..."))
		idx = 4
		res = (name,png,idx, desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/ushare_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("MiniDLNA Panel"))
		desc = (_("Manage Your MiniDLNA UpNp Server..."))
		idx = 5
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/ushare_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("uShare Panel"))
		desc = (_("Manage Your ushare UpNp Server..."))
		idx = 13
		res = (name,png,idx,desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/syslog_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("Syslog Panel"))
		desc = (_("Manage system and kernel logs..."))
		idx = 6
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/samba_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("Samba Panel"))
		desc = (_("Manage Your samba..."))
		idx = 7
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/openvpn_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("OpenVPN Panel"))
		desc = (_("Manage Your openvpn..."))
		idx = 8
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/ftp_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("FTP Panel"))
		desc = (_("Manage Your ftp..."))
		idx = 9
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/telnet_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("Telnet Panel"))
		desc = (_("Manage Your Telnet..."))
		idx = 10
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/pcscd_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("Pcscd Panel"))
		desc = (_("Manage Your pcscd..."))
		idx = 11
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/dropbear_panel.png")
		png = LoadPixmap(mypixmap)
		name = (_("DropBear Panel"))
		desc = (_("Manage Your ssh server / client..."))
		idx = 12
		res = (name,png,idx, desc)
		self.list.append(res)
		
		self["list"].list = self.list
	    