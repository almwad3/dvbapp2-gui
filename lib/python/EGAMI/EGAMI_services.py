# -*- coding: utf-8 -*-
from enigma import eTimer
from Screens.Screen import Screen 
from Screens.Console import Console 
from Screens.MessageBox import MessageBox

from Components.Button import Button
from Components.ActionMap import ActionMap 
from Components.Pixmap import Pixmap 
from Components.Sources.List import List 
from Components.config import *

from string import split, strip

from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_SKIN, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap, pixmap_cache

from os import path as os_path
import os

from EGAMI.EGAMI_services_config import *
from EGAMI.EGAMI_skins import EGServicesMenu_Skin, EGServices_Skin
from EGAMI.EGAMI_tools import wyszukaj_re, wyszukaj_in, loadbool, loadcfg, EGPLoadPixmap, runBackCmd


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
	    self.session.open(EGNfsServer)
        elif (self.sel == 1):
	   self.session.open(EGHttpd)
        elif (self.sel == 2):
	    self.session.open(EGInadyn)
        elif (self.sel == 3):
	    self.session.open(EGCronMang)
        elif (self.sel == 4):
	    from Plugins.Extensions.DLNABrowser.plugin import DLNADeviceBrowser
	    self.session.open(DLNADeviceBrowser)
	    #self.session.open(EGDjMountConfig)
        elif (self.sel == 5):
	    from Plugins.Extensions.DLNAServer.plugin import DLNAServer
	    self.session.open(DLNAServer)	    
	    #self.session.open(EGUShareConfig)
        elif (self.sel == 6):
	    self.session.open(EGSyslogDConfig)
        elif (self.sel == 7):
	    self.session.open(EGSambaConfig)
        elif (self.sel == 8):
	    self.session.open(EGOpenVPNConfig)
        elif (self.sel == 9):
	    self.session.open(EGFtpConfig)
        elif (self.sel == 10):
	    self.session.open(EGTelnetConfig)
        elif (self.sel == 11):
	    self.session.open(EGPcscdConfig)
        elif (self.sel == 12):
	    self.session.open(EGDropbearConfig)
        else:
            self.noYet()

    def noYet(self):
        nobox = self.session.open(MessageBox, "Function Not Yet Available", MessageBox.TYPE_INFO)
        nobox.setTitle(_("Info"))


    def updateList(self):
        self.list = []
	mypath = resolveFilename(SCOPE_CURRENT_SKIN)
	if not fileExists(mypath + "egami_icons"):
	    mypath = "/usr/share/enigma2/skin_default/"
	    

        mypixmap = (mypath + "egami_icons/nfsserver_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("NFS Server Panel"))
        desc = (_("Manage Your NFS Server..."))
	idx = 0
        res = (name,
         png,
         idx, desc)
        self.list.append(res)
        
        mypixmap = (mypath + "egami_icons/httpd_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("HTTPD Panel"))
	desc = (_("Manage Your little WWW web-apache"))
        idx = 1
        res = (name,
         png,
         idx, desc)
        self.list.append(res)
        
        mypixmap = (mypath + "egami_icons/inadyn_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("Inadyn Panel"))
        desc = (_("Manage Inadyn, simple dyndns updater..."))
	idx = 2
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/cron_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("Cron Panel"))
	desc = (_("Manage Your cron..."))
        idx = 3
        res = (name,
         png,
         idx, desc)
        self.list.append(res)
        
        mypixmap = (mypath + "egami_icons/djmount_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("DjMount Panel"))
        desc = (_("Manage Your UpNp Client..."))
	idx = 4
        res = (name,
         png,
         idx, desc)
        self.list.append(res)
        
        mypixmap = (mypath + "egami_icons/ushare_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("MiniDLNA Panel"))
	desc = (_("Manage Your MiniDLNA UpNp Server..."))
        idx = 5
        res = (name,png,idx,desc)
        self.list.append(res)

        
        mypixmap = (mypath + "egami_icons/syslog_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("Syslog Panel"))
        desc = (_("Manage system and kernel logs..."))
	idx = 6
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/samba_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("Samba Panel"))
        desc = (_("Manage Your samba..."))
	idx = 7
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/openvpn_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("OpenVPN Panel"))
        desc = (_("Manage Your openvpn..."))
	idx = 8
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/ftp_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("FTP Panel"))
        desc = (_("Manage Your ftp..."))
	idx = 9
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/telnet_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("Telnet Panel"))
        desc = (_("Manage Your Telnet..."))
	idx = 10
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/pcscd_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("Pcscd Panel"))
        desc = (_("Manage Your pcscd..."))
	idx = 11
        res = (name,
         png,
         idx,desc)
        self.list.append(res)

        mypixmap = (mypath + "egami_icons/dropbear_panel.png")
        png = LoadPixmap(mypixmap)
        name = (_("DropBear Panel"))
        desc = (_("Manage Your ssh server / client..."))
	idx = 12
        res = (name,
         png,
         idx,desc)
        self.list.append(res)
        
        self["list"].list = self.list
        