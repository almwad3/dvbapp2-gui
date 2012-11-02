# -*- coding: utf-8 -*-

from enigma import eTimer 

from Screens.Screen import Screen 
from Screens.MessageBox import MessageBox 
from Screens.Standby import TryQuitMainloop 
from Screens.Console import Console 
from Screens.VirtualKeyBoard import VirtualKeyBoard 
from Screens.LocationBox import *

from Components.ActionMap import ActionMap, NumberActionMap
from Components.Pixmap import Pixmap 
from Components.PluginComponent import plugins 
from Components.Sources.List import List 
from Components.Label import Label
from Components.config import *
from Components.ConfigList import *

from Tools.LoadPixmap import LoadPixmap 
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_SKIN_IMAGE

from os import system, remove as os_remove, rename as os_rename, popen 

import os

from EGAMI.EGAMI_skins import EGDropbearConfig_Skin, EGPcscdConfig_Skin, EGTelnetConfig_Skin, EGFtpConfig_Skin, EGSambaConfig_Skin, EGDjMountConfigRoot_Skin, EGDjMountConfig_Skin, EGUShareConfig_Skin, EGSyslogDConfig_Skin, EGCronMang_Skin, EGSetupCronConf_Skin, EGHttpd_Skin, EGInadyn_Skin, EGNfsServer_Skin, EGOpenVPNConfig_Skin
from EGAMI.EGAMI_tools import wyszukaj_re, wyszukaj_in, loadcfg


class EGNfsServer(ConfigListScreen,Screen):
    def __init__(self, session):
		self.skin = EGNfsServer_Skin
		
		Screen.__init__(self, session)
		session = None
		self.load_conf()
		
		self.autostart = ConfigSelection(default = self.def_autostart, choices = [("1", _("Yes")), ("0", _("No"))])
		self.clientip = ConfigIP(default = self.def_clientip)
		self.netmaskip = ConfigIP(default = self.def_netmaskip)
		self.folder = ConfigSelection(default=self.def_folder, choices=['/media/hdd', '/media/cf', '/media/usb', '/media/net'])
		self.options = ConfigSelection(default=self.def_options, choices=['ro', 'rw', 'ro,sync', 'rw,sync', 'ro,async', 'rw,async', 'ro,no_root_squash', 'rw,no_root_squash',
 'ro,no_root_squash,sync',
 'rw,no_root_squash,sync',
 'ro,no_root_squash,async',
 'rw,no_root_squash,async'])
		self.useport =  ConfigSelection(default = self.def_useport, choices = [("1", _("Yes")), ("0", _("No"))])
		self.port = ConfigText(default=self.def_port)
	
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
	
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
			"cancel": self.cancel,
			"red": self.start_nfs,
			"green": self.cancel,
			"yellow" : self.start,
			"blue" : self.stop
		}, -2)
		
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
	
		self.createInfo()
	
    def createInfo(self):
	    os.system("ps > /tmp/nfs.tmp")
	    zrodlo = open("/tmp/nfs.tmp", 'r')
	    szukana_fraza = '[nfsd]'
	    if (wyszukaj_in(zrodlo,szukana_fraza)):
			self["state"].setText(_("Status: Nfsd is running!"))
	    else:
			self["state"].setText(_("Status: Nfsd stopped!"))
	    os.system("rm -rf /tmp/nfs.tmp")
	    zrodlo.seek(0)
	    zrodlo.close()

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_("Autostart:"), self.autostart))
        self.list.append(getConfigListEntry(_("Client IP:"), self.clientip))
        self.list.append(getConfigListEntry(_("Netmask:"), self.netmaskip))
        self.list.append(getConfigListEntry(_("Folder:"), self.folder))
        self.list.append(getConfigListEntry(_("Options:"), self.options))
        self.list.append(getConfigListEntry(_("Use Port:"), self.useport))
        self.list.append(getConfigListEntry(_("    Port:"), self.port))

    def convertIP(self, ip):
        strIP = ip.split('.')
        ip = []
        for x in strIP:
			ip.append(int(x))
        return ip
		
    def load_conf(self):
		self.def_autostart = "0"
		self.def_clientip = [192,168,0,0]
		self.def_netmaskip = [255,255,255,0]
		self.def_folder = "/media/hdd"
		self.def_options = "rw,no_root_squash,async"
		self.def_useport = "0"
		self.def_port = "2049"
		
		if fileExists('/scripts/nfs_server_script.sh'):
			f = open('/scripts/nfs_server_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				x = line.split()
				if (line.find('NFSSERVER_ON=') != -1):
					self.def_autostart = line[13:14]
				elif (line.find('NFS_CL_IP=') != -1):
					self.def_clientip = line[10:]
					self.def_clientip2 = line[10:]
					self.def_clientip = self.convertIP(self.def_clientip)					
				elif (line.find('NFSNETMASKE=') != -1):
					self.def_netmaskip = line[12:]
					self.def_netmaskip2 = line[12:]
					self.def_netmaskip = self.convertIP(self.def_netmaskip)	
				elif (line.find('DIRECTORY=') != -1):
					self.def_folder = line[10:]
				elif (line.find('MOUNTD_PORT_ON=') != -1):
					self.def_useport = line[15:]
				elif (line.find('MOUNTD_PORT=') != -1):
					self.def_port = line[12:]
				elif (line.find('OPTIONS=') != -1):
					self.def_options = line[8:]
			f.close()

    def save_conf(self):
		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("NFSSERVER_ON=" + self.def_autostart), ("NFSSERVER_ON=" + self.autostart.value)))
		cel.close()
		
		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_clientip2, "%d.%d.%d.%d" % tuple(self.clientip.value)))
		cel.close()
		
		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_netmaskip2, "%d.%d.%d.%d" % tuple(self.netmaskip.value)))
		cel.close()
		
		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_folder, self.folder.value))
		cel.close()
		
		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("MOUNTD_PORT_ON=" + self.def_useport), ("MOUNTD_PORT_ON=" + self.useport.value)))
		cel.close()
		
		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_port, self.port.value))
		cel.close()

		zrodlo = open('/scripts/nfs_server_script.sh').readlines()
		cel = open('/scripts/nfs_server_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_options, self.options.value))
		cel.close()
		
    def start(self):
      		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: Nfsd is starting..."))
		os.system("/scripts/nfs_server_script.sh start2")
		self.createInfo()
		
    def stop(self):
		self["state"].setText(_("Status: Nfsd is stopping..."))
		os.system("/scripts/nfs_server_script.sh stop;killall -9 rpc.mountd nfsd portmap;killall -9 rpc.mountd nfsd portmap;killall -9 rpc.mountd nfsd portmap")
		self.createInfo()
		
    def start_nfs(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
    def cancel(self):
	    self.close(False)
	    
class EGHttpd(ConfigListScreen,Screen):
    def __init__(self, session, args = 0):
        self.skin = EGHttpd_Skin
	Screen.__init__(self, session)
	session = None	
	self.load_conf()
	
	self.httpau = ConfigSelection(default = self.def_httpau, choices = [("1", _("Yes")), ("0", _("No"))])
	self.httproot = ConfigText(default = self.def_httproot, fixed_size = False)
	self.httpport = ConfigText(default = self.def_httpport, fixed_size = False)
	self.httpconf = ConfigText(default = self.def_httpconf, fixed_size = False)

	self.createSetup()
		
	ConfigListScreen.__init__(self, self.list, session = session)
	
	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
	{
		"cancel": self.cancel,
		"red": self.start_httpd,
		"green": self.cancel,
		"yellow" : self.start,
		"blue" : self.stop
	}, -2)
		
	self["key_red"] = Label(_("Save"))		
	self["key_green"] = Label(_("Cancel"))		
	self["key_yellow"] = Label(_("Start"))
	self["key_blue"] = Label(_("Stop"))
		
	self["state"] = Label()
	
	self.createInfo()
	
    def createInfo(self):
	    	os.system("ps > /tmp/ps.tmp")
		zrodlo = open("/tmp/ps.tmp", 'r')
		szukana_fraza = 'httpd'
		if wyszukaj_in(zrodlo,szukana_fraza):
				self["state"].setText(_("Status: Httpd is running!"))
		else:
			self["state"].setText(_("Status: Httpd stopped!"))
		os.system("rm -rf /tmp/ps.tmp")
	   	zrodlo.seek(0)
	   	zrodlo.close()
		
    def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.httpau))
        	self.list.append(getConfigListEntry(_("WWW Directory:"), self.httproot))
        	self.list.append(getConfigListEntry(_("Port:"), self.httpport))
        	self.list.append(getConfigListEntry(_("HTTPD Config File:"), self.httpconf))
		
    def load_conf(self):
		self.def_httpau = "0"
		self.def_httproot = "/usr/www"
		self.def_httpport = "8047"
		self.def_httpconf = "/var/etc/httpd.conf"
		
		if fileExists('/scripts/httpd_script.sh'):
			f = open('/scripts/httpd_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('HTTP_ON=') != -1):
					self.def_httpau = line[8:9]
				elif (line.find('HTTPROOT=') != -1):
					self.def_httproot = line[9:]
				elif (line.find('HTTPPORT=') != -1):
					self.def_httpport = line[9:]
				elif (line.find('HTTPCONF=') != -1):
					self.def_httpconf = line[9:]
			f.close()
			
			
    def save_conf(self):
		zrodlo = open('/scripts/httpd_script.sh').readlines()
		cel = open('/scripts/httpd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("HTTP_ON=" + self.def_httpau), ("HTTP_ON=" + self.httpau.value)))
		cel.close()
		
		zrodlo = open('/scripts/httpd_script.sh').readlines()
		cel = open('/scripts/httpd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_httproot, self.httproot.value))
		cel.close()
		
		zrodlo = open('/scripts/httpd_script.sh').readlines()
		cel = open('/scripts/httpd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_httpport, self.httpport.value))
		cel.close()
		
		zrodlo = open('/scripts/httpd_script.sh').readlines()
		cel = open('/scripts/httpd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_httpconf, self.httpconf.value))
		cel.close()
		
    def start(self):
      		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: httpd is starting..."))
		os.system("/scripts/httpd_script.sh start2")
		self.createInfo()
		
    def stop(self):
		self["state"].setText(_("Status: httpd is stopping..."))
		os.system("/scripts/httpd_script.sh stop;killall -9 httpd")
		self.createInfo()
		
    def start_httpd(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
    def cancel(self):
	    self.close(False)
	    
class EGInadyn(ConfigListScreen,Screen):
    def __init__(self, session):
	self.skin = EGInadyn_Skin
	Screen.__init__(self, session)
	session = None
	self.load_conf()
	self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
	self.username = ConfigText(default = self.def_username, fixed_size = False)
	self.password = ConfigText(default = self.def_password, fixed_size = False)
	self.alias = ConfigText(default = self.def_alias, fixed_size = False)
	self.period = ConfigSelection(default = self.def_period, choices = [("60000", _("1 min.")),("300000", _("5 min.")),("600000", _("10 min.")),("900000", _("15 min.")),("1800000", _("30 min.")),("3600000", _("60 min."))])
	self.log_enable =  ConfigSelection(default = self.def_log_enable, choices = [("1", _("Yes")), ("0", _("No"))])
	self.log_name = ConfigText(default = self.def_log_name, fixed_size = False)
	self.dyn_system_enable = ConfigSelection(default = self.def_dyn_system_enable, choices = [("1", _("Yes")), ("0", _("No"))])
	self.dyn_system = ConfigSelection(default = self.def_dyn_system, choices=['dyndns@dyndns.org', 'default@freedns.afraid.org', 'default@zoneedit.com', 'default@no-ip.com', 'custom@http_svr_basic_auth'])
	
	self.createSetup()
		
	ConfigListScreen.__init__(self, self.list, session = session)
	self.log_enable.addNotifier(self.typeChange)
	self.dyn_system_enable.addNotifier(self.typeChange)
	
	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
	{
		"cancel": self.cancel,
		"red": self.start_inadyn,
		"green": self.cancel,
		"yellow" : self.start,
		"blue" : self.stop
	}, -2)
		
	self["key_red"] = Label(_("Save"))		
	self["key_green"] = Label(_("Cancel"))		
	self["key_yellow"] = Label(_("Start"))
	self["key_blue"] = Label(_("Stop"))
	
	self["state"] = Label()
	
	self.createInfo()
	
    def createInfo(self):
	    	os.system("ps > /tmp/ps.tmp")
		zrodlo = open("/tmp/ps.tmp", 'r')
		szukana_fraza = 'inadyn'
		if wyszukaj_in(zrodlo,szukana_fraza):
				self["state"].setText(_("Status: Inadyn is running!"))
		else:
			self["state"].setText(_("Status: Inadyn stopped!"))
		os.system("rm -rf /tmp/ps.tmp")
	   	zrodlo.seek(0)
	   	zrodlo.close()
		
    def typeChange(self, value):
		self.createSetup()
		self["config"].l.setList(self.list)
		
    def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	self.list.append(getConfigListEntry(_("Username:"), self.username))
        	self.list.append(getConfigListEntry(_("Password:"), self.password))
        	self.list.append(getConfigListEntry(_("Alias:"), self.alias))
		self.list.append(getConfigListEntry(_("Time Period:"), self.period))
		self.list.append(getConfigListEntry(_('Enable log:'), self.log_enable))
		if self.log_enable.value == "1":
        		self.list.append(getConfigListEntry(_("    Log file name:"), self.log_name))
        	self.list.append(getConfigListEntry(_("Enable dyndns system:"), self.dyn_system_enable))
		if self.dyn_system_enable.value == "1":
			self.list.append(getConfigListEntry(_("    Use system:"), self.dyn_system))
		
    def load_conf(self):
		self.def_au = "0"
		self.def_username = "user@gmail.com"
		self.def_password = "userpass"
		self.def_alias = "user@dyndns.org"
		self.def_period = "60000"
		self.def_log_enable = "0"
		self.def_log_name = "/var/log/inadyn.log"
		self.def_dyn_system_enable = "0"
		self.def_dyn_system = "dyndns@dyndns.org"
		
		if fileExists('/scripts/inadyn_script.sh'):
			f = open('/scripts/inadyn_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('INADYN_ON=') != -1):
					self.def_au = line[10:11]
				elif (line.find('INADYN_USERNAME=') != -1):
					self.def_username = line[16:]
				elif (line.find('INADYN_PASSWORD=') != -1):
					self.def_password = line[16:]
				elif (line.find('INADYN_ALIAS=') != -1):
					self.def_alias = line[13:]
				elif (line.find('UPDATE_PERIOD=') != -1):
					self.def_period = line[14:]
				elif (line.find('LOG_FILE_ON=') != -1):
					self.def_log_enable = line[12:]
				elif (line.find('LOG_NAME=') != -1):
					self.def_log_name = line[9:]
				elif (line.find('DYN_SYSTEM_ON=') != -1):
					self.def_dyn_system_enable = line[14:]
				elif (line.find('DYN_SYSTEM=') != -1):
					self.def_dyn_system = line[11:]
			f.close()
			
			
    def save_conf(self):
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("INADYN_ON=" + self.def_au), ("INADYN_ON=" + self.au.value)))
		cel.close()
		
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_username, self.username.value))
		cel.close()
		
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_password, self.password.value))
		cel.close()
		
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_alias, self.alias.value))
		cel.close()
		
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_period, self.period.value))
		cel.close()
		
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("LOG_FILE_ON=" + self.def_log_enable), ("LOG_FILE_ON=" + self.log_enable.value)))
		cel.close()
		
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_log_name, self.log_name.value))
		cel.close()
				
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("DYN_SYSTEM_ON=" + self.def_dyn_system_enable), ("DYN_SYSTEM_ON=" + self.dyn_system_enable.value)))
		cel.close()
				
		zrodlo = open('/scripts/inadyn_script.sh').readlines()
		cel = open('/scripts/inadyn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_dyn_system , self.dyn_system .value))
		cel.close()
		
    def start(self):
      		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: inadyn is starting..."))
		os.system("/scripts/inadyn_script.sh start2")
		self.createInfo()
		
    def stop(self):
		self["state"].setText(_("Status: inadyn is stopping..."))
		os.system("/scripts/inadyn_script.sh stop;killall -9 inadyn")
		self.createInfo()
		
    def start_inadyn(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
    def cancel(self):
	    self.close(False)
	    
class EGCronMang(Screen):
    def __init__(self, session):
	self.skin = EGCronMang_Skin
        Screen.__init__(self, session)
        
        self["key_red"] = Label(_("Add"))
	self["key_green"] = Label(_("Delete"))	
        self["key_yellow"] = Label(_("Start"))
	self["key_blue"] = Label(_("Stop"))
	
        self.list = []
        self["list"] = List(self.list)
        self["actions"] = ActionMap(["WizardActions", "ColorActions"], 
        {
		"ok": self.cancel,
		"back": self.cancel,
		"red": self.addtocron,
		"green": self.delcron,
		"yellow" : self.start,
		"blue" : self.stop
         })
        self.updateList()

	self["state"] = Label()
	
	self.createInfo()
	
    def createInfo(self):
	    	os.system("ps > /tmp/ps.tmp")
		zrodlo = open("/tmp/ps.tmp", 'r')
		szukana_fraza = '/usr/sbin/crond -c /etc/cron/crontabs'
		if wyszukaj_in(zrodlo,szukana_fraza):
				self["state"].setText(_("Status: Crond is running!"))
		else:
			self["state"].setText(_("Status: Crond stopped!"))
		os.system("rm -rf /tmp/ps.tmp")
	   	zrodlo.seek(0)
	   	zrodlo.close()
	   	
    def addtocron(self):
        self.session.openWithCallback(self.updateList, EGSetupCronConf)



    def updateList(self):
        self.list = []
        if fileExists("/etc/cron/crontabs/root"):
            f = open("/etc/cron/crontabs/root", "r")
            for line in f.readlines():
                parts = line.strip().split()
                line2 = (((((("Time: " + parts[1]) + ":") + parts[0]) + "\t") + "Command: ") + line[(line.rfind("*") + 1):])
                res = (line2,
                 line)
                self.list.append(res)

            f.close()
        self["list"].list = self.list



    def delcron(self):
        mysel = self["list"].getCurrent()
        if mysel:
            myline = mysel[1]
            out = open("/etc/cron/crontabs/ds.cron", "w")
            f = open("/etc/cron/crontabs/root", "r")
            for line in f.readlines():
                if (line != myline):
                    out.write(line)

            f.close()
            out.close()
            rc = system("crontab /etc/cron/crontabs/ds.cron -c /etc/cron/crontabs/")
            self.updateList()
	    
		
    def cancel(self):
	    self.close(True)

    def start(self):
      		self.stop()
		self["state"].setText(_("Status: crond is starting..."))
		os.system("/scripts/crond_script.sh start")
		self.createInfo()
		
    def stop(self):
		self["state"].setText(_("Status: crond is stopping..."))
		os.system("/scripts/crond_script.sh stop;killall -9 crond")
		self.createInfo()

class EGSetupCronConf(Screen,
 ConfigListScreen):
    def __init__(self, session):
	self.skin = EGSetupCronConf_Skin
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self["key_red"] = Label(_("Save"))
	self["key_green"] = Label(_("Virtual Keyboard"))
        self["actions"] = ActionMap(["WizardActions",
         "ColorActions"], {"red": self.checkentry,
         "back": self.close,
         "green": self.vkeyb})
        self.updateList()



    def updateList(self):
        self.cmdtime = NoSave(ConfigClock(default=0))
        self.default_command = NoSave(ConfigSelection(default="None", choices=[('None', 'None'),
         ('killall emud;sleep 3;emud&', 'Reset Emu'),
         ('halt', 'Shutdown Box'),
         ('reboot', 'Reboot Box'),
         ('killall enigma2', 'Restart Enigma2')]))
        self.user_command = NoSave(ConfigText(fixed_size=False))
        self.cmdtime.value = mytmpt = [0,
         0]
        self.default_command.value = "None"
        self.user_command.value = "None"
        res = getConfigListEntry("Time to execute command or script", self.cmdtime)
        self.list.append(res)
        res = getConfigListEntry("Predefined Command to execute", self.default_command)
        self.list.append(res)
        res = getConfigListEntry("Custom Command", self.user_command)
        self.list.append(res)
        self["config"].list = self.list
        self["config"].l.setList(self.list)



    def vkeyb(self):
        sel = self["config"].getCurrent()
        if sel:
            self.vkvar = sel[0]
            value = "ds"
            if (self.vkvar == "Custom Command"):
                value = self.user_command.value
                if (value == "None"):
                    value = ""
            if (value != "ds"):
                self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)
            else:
                self.session.open(MessageBox, "Please use Virtual Keyboard for text rows only (e.g. Custom Command)", MessageBox.TYPE_INFO)



    def UpdateAgain(self, newt):
        self.list = []
        if ((newt is None) or (newt == "")):
            newt = "None"
        self.user_command.value = newt
        res = getConfigListEntry("Time to execute command or script", self.cmdtime)
        self.list.append(res)
        res = getConfigListEntry("Predefined Command to execute", self.default_command)
        self.list.append(res)
        res = getConfigListEntry("Custom Command", self.user_command)
        self.list.append(res)
        self["config"].list = self.list
        self["config"].l.setList(self.list)



    def checkentry(self):
        msg = ""
        if (self.user_command.value == "None"):
            self.user_command.value = ""
        if ((self.default_command.value == "None") and (self.user_command.value == "")):
            msg = "You must set at least one Command"
        if ((self.default_command.value != "None") and (self.user_command.value != "")):
            msg = "Entering a Custom command you have to set Predefined command: None "
        if msg:
            self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
        else:
            self.saveMycron()



    def saveMycron(self):
        hour = ("%02d" % self.cmdtime.value[0])
        minutes = ("%02d" % self.cmdtime.value[1])
        if (self.default_command.value != "None"):
            command = self.default_command.value
        else:
            command = self.user_command.value
        newcron = (((((minutes + " ") + hour) + " * * * ") + command.strip()) + "\n")
        out = open("/etc/cron/crontabs/ds.cron", "w")
        if fileExists("/etc/cron/crontabs/root"):
            f = open("/etc/cron/crontabs/root", "r")
            for line in f.readlines():
                out.write(line)

            f.close()
        out.write(newcron)
        out.close()
        rc = system("crontab /etc/cron/crontabs/ds.cron -c /etc/cron/crontabs/")
        self.close()

class EGDjMountConfigRoot(LocationBox):
	def __init__(self, session):
		self.skin = EGDjMountConfigRoot_Skin
		inhibitDirs = ["/bin", "/boot", "/dev", "/etc", "/lib", "/proc", "/sbin", "/sys", "/usr", "/var"]
		log = loadcfg('/scripts/djmount_script.sh', 'UPNPROOT=', 9)
		LocationBox.__init__(
				self,
				session,
				text = _("Where would You like to have an UPnP root directory?"),
				currDir = log,
				bookmarks = None,
				autoAdd = True,
				editDir = False,
				inhibitDirs = [],
				minFree = None
		)

	def cancel(self):
		LocationBox.cancel(self)

	def selectConfirmed(self, ret):
		if ret:
			log = loadcfg('/scripts/djmount_script.sh', 'UPNPROOT=', 9)
			new_root = self.getPreferredFolder()
			
			zrodlo = open('/scripts/djmount_script.sh').readlines()
			cel = open('/scripts/djmount_script.sh', 'w')
			for s in zrodlo:
				cel.write(s.replace(log, new_root))
			cel.close()
			LocationBox.selectConfirmed(self, ret)
			
class EGDjMountConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGDjMountConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
		self.dir_root = ConfigText(default = self.def_dir_root)
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_djmount,
		      "green": self.cancel,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
		self.list.append(getConfigListEntry(_("DjMount UPnP root directory:"), self.dir_root))
        	
	def createInfo(self):
		os.system("ps > /tmp/djmount.tmp")
		zrodlo = open("/tmp/djmount.tmp", 'r')
		szukana_fraza = '/usr/bin/djmount'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    self["state"].setText(_("Status: DjMount is running!"))
		else:
			    self["state"].setText(_("Status: DjMount stopped!"))
		os.system("rm -rf /tmp/djmount.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
	  	self.stop()
		self.save_conf()
		self["state"].setText(_("Status: djmount is starting..."))
		os.system("/scripts/djmount_script.sh start2")
		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: djmount is stopping..."))
		os.system("/scripts/djmount_script.sh stop;killall -9 djmount")
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		self.def_dir_root = "/media/hdd"
		
		if fileExists('/scripts/djmount_script.sh'):
			f = open('/scripts/djmount_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('UPNP_ON=') != -1):
					self.def_au = line[8:9]
			f.close()
			
		self.def_dir_root = loadcfg('/scripts/djmount_script.sh', 'UPNPROOT=', 9)
			
	def save_conf(self):
		zrodlo = open('/scripts/djmount_script.sh').readlines()
		cel = open('/scripts/djmount_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("UPNP_ON=" + self.def_au), ("UPNP_ON=" + self.au.value)))
		cel.close()	

	def start_djmount(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
	def keyLeft(self):
	    ConfigListScreen.keyLeft(self)
	    self.handleKeysLeftAndRight()

	def keyRight(self):
	    ConfigListScreen.keyRight(self)
	    self.handleKeysLeftAndRight()

	def handleKeysLeftAndRight(self):
	    sel = self["config"].getCurrent()[1]
	    if sel == self.dir_root:
		    self.session.open(EGDjMountConfigRoot)
		    self.close()
		
		
class EGUShareConfig(ConfigListScreen,Screen):
    def __init__(self, session, args = 0):
        self.skin = EGUShareConfig_Skin
	Screen.__init__(self, session)
	session = None	
	
	self.load_conf()
	
	self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
	self.dir_root = ConfigText(default = self.def_dir_root)
	self.dir_port = ConfigText(default = self.def_dir_port)

	self.createSetup()
		
	ConfigListScreen.__init__(self, self.list, session = session)
	
	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
	{
		"cancel": self.cancel,
		"red": self.save_conf,
		"green": self.cancel,
		"yellow" : self.start,
		"blue" : self.stop
	}, -2)
		
	self["key_red"] = Label(_("Save"))		
	self["key_green"] = Label(_("Cancel"))		
	self["key_yellow"] = Label(_("Start"))
	self["key_blue"] = Label(_("Stop"))
	
	self["state"] = Label()
	
	self.createInfo()
	
    def createInfo(self):
	    os.system("ps > /tmp/ushare.tmp")
	    zrodlo = open("/tmp/ushare.tmp", 'r')
	    szukana_fraza = '/usr/bin/ushare'
	    if (wyszukaj_in(zrodlo,szukana_fraza)):
			self["state"].setText(_("Status: uShare is running!"))
	    else:
			self["state"].setText(_("Status: uShare stopped!"))
	    os.system("rm -rf /tmp/ushare.tmp")
	    zrodlo.seek(0)
	    zrodlo.close()
	    
    def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	self.list.append(getConfigListEntry(_("U-Share UPnP root directory:"), self.dir_root))
        	self.list.append(getConfigListEntry(_("Server Name:"), self.dir_port))
		
    def load_conf(self):
		self.def_au = "0"
		self.def_dir_root = "/media/hdd"
		self.def_dir_port = "Upnp-Dreambox-0"
		
		if fileExists('/scripts/ushare_script.sh'):
			f = open('/scripts/ushare_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('UPNP_ON=') != -1):
					self.def_au = line[8:9]
				elif (line.find('UPNPROOT=') != -1):
					self.def_dir_root = line[9:]
				elif (line.find('SERVER=') != -1):
					self.def_dir_port = line[7:]
			f.close()
			
			
    def save_conf(self):
		zrodlo = open('/scripts/ushare_script.sh').readlines()
		cel = open('/scripts/ushare_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("UPNP_ON=" + self.def_au), ("UPNP_ON=" + self.au.value)))
		cel.close()
		
		zrodlo = open('/scripts/ushare_script.sh').readlines()
		cel = open('/scripts/ushare_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_dir_root, self.dir_root.value))
		cel.close()
		
		zrodlo = open('/scripts/ushare_script.sh').readlines()
		cel = open('/scripts/ushare_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_dir_port, self.dir_port.value))
		cel.close()

    def start(self):
      		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: ushare is starting..."))
		os.system("/scripts/ushare_script.sh start2")
		self.createInfo()
		
    def stop(self):
		self["state"].setText(_("Status: ushare is stopping..."))
		os.system("/scripts/ushare_script.sh stop;killall -9 ushare")
		self.createInfo()
		
    def cancel(self):
	    self.close(False)


class EGSyslogDConfig(ConfigListScreen,Screen):
    def __init__(self, session):
        self.skin = EGSyslogDConfig_Skin
	
	Screen.__init__(self, session)
	session = None	
	self.load_conf()
	
	self.au = ConfigSelection(default = self.def_enigma_debug, choices = [("1", _("Yes")), ("0", _("No"))])
	self.enigma_debug = ConfigSelection(default = self.def_enigma_debug, choices = [("1", _("Yes")), ("0", _("No"))])
	self.kernel_debug = ConfigSelection(default = self.def_kernel_debug, choices = [("1", _("Yes")), ("0", _("No"))])
	self.buffer_size = ConfigNumber(default = self.def_buffer_size)
	self.set_idx = ConfigSelection(default = self.def_set_idx, choices = [("1", _("Yes")), ("0", _("No"))])
	self.inter_min = ConfigNumber(default = self.def_inter_min)
	self.red_size = ConfigSelection(default = self.def_red_size, choices = [("1", _("Yes")), ("0", _("No"))])
	self.log_file_name = ConfigText(default = self.def_log_file_name, fixed_size = False)
	self.rem_log = ConfigSelection(default = self.def_rem_log, choices = [("1", _("Yes")), ("0", _("No"))])
	self.rem_host = ConfigText(default=self.def_rem_host)
	self.rem_port = ConfigNumber(default=self.def_rem_port)
	
	self.createSetup()
		
	ConfigListScreen.__init__(self, self.list, session = session)
	self.rem_log.addNotifier(self.typeChange)

	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
	{
		"cancel": self.cancel,
		"red": self.start_syslogd,
		"green": self.cancel,
		"yellow" : self.start,
		"blue" : self.stop
	}, -2)
		
	self["key_red"] = Label(_("Save"))		
	self["key_green"] = Label(_("Cancel"))		
	self["key_yellow"] = Label(_("Start"))
	self["key_blue"] = Label(_("Stop"))
	
	self["state"] = Label()
	
	self.createInfo()
	
    def createInfo(self):
	    os.system("ps > /tmp/syslogd.tmp")
	    zrodlo = open("/tmp/syslogd.tmp", 'r')
	    szukana_fraza = '/sbin/klogd'
	    if (wyszukaj_in(zrodlo,szukana_fraza)):
			self["state"].setText(_("Status: syslogd and klogd are running!"))
	    else:
			self["state"].setText(_("Status: syslogd and klogd stopped!"))
	    os.system("rm -rf /tmp/syslogd.tmp")
	    zrodlo.seek(0)
	    zrodlo.close()
	    
    def typeChange(self, value):
		self.createSetup()
		self["config"].l.setList(self.list)
		
    def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	self.list.append(getConfigListEntry(_("Enigma-Debug:"), self.enigma_debug))
        	self.list.append(getConfigListEntry(_("Kernel-Debug:"), self.kernel_debug))
        	self.list.append(getConfigListEntry(_("Buffer size [kB]:"), self.buffer_size))
        	self.list.append(getConfigListEntry(_("Set index mark:"), self.set_idx))
        	self.list.append(getConfigListEntry(_("Interval in min:"), self.inter_min))
        	self.list.append(getConfigListEntry(_("Reduce size logging:"), self.red_size))
        	self.list.append(getConfigListEntry(_("Log file name:"), self.log_file_name))
        	self.list.append(getConfigListEntry(_("Remote logging:"), self.rem_log))
		if self.rem_log.value == "1":
			self.list.append(getConfigListEntry(_("	Remote host:"), self.rem_host))
			self.list.append(getConfigListEntry(_("	Remote port:"), self.rem_port))
		
		
    def load_conf(self):
		self.def_enigma_debug = "0"
		self.def_kernel_debug = "0"
		self.def_buffer_size = 16
		self.def_set_idx = "1"
		self.def_inter_min = 20
		self.def_red_size = "0"
		self.def_log_file_name = "/var/log/messages"
		self.def_rem_log = "0"
		self.def_rem_host = "192.168.0.1"
		self.def_rem_port = 514
		
		if fileExists('/scripts/syslogd_script.sh'):
			f = open('/scripts/syslogd_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('SYSLOGD_ON=') != -1):
					self.def_enigma_debug = line[11:]
				elif (line.find('KLOGD_ON=') != -1):
					self.def_kernel_debug = line[9:]
				elif (line.find('BUFFERSIZE=') != -1):
					self.def_buffer_size = line[11:]
				elif (line.find('MARKINT=') != -1):
					self.def_inter_min = line[8:]
				elif (line.find('REDUCE=') != -1):
					self.def_red_size = line[7:]
				elif (line.find('LOGFILE=') != -1):
					self.def_log_file_name = line[8:]
				elif (line.find('REMOTE=') != -1):
					self.def_rem_log = line[7:]
				elif (line.find('REMOTE_HOST=') != -1):
					self.def_rem_host = line[12:]
				elif (line.find('REMOTE_PORT=') != -1):
					self.def_rem_port = line[12:]
			f.close()
			
			
    def save_conf(self):
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("SYSLOGD_ON=" + self.def_enigma_debug), ("SYSLOGD_ON=" + self.enigma_debug.value)))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("KLOGD_ON=" + self.def_kernel_debug), ("KLOGD_ON=" + self.kernel_debug.value)))
		cel.close()

		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_buffer_size, str(self.buffer_size.value)))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_inter_min, str(self.inter_min.value)))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("REDUCE=" + self.def_red_size), ("REDUCE=" + self.red_size.value)))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_log_file_name, self.log_file_name.value))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("REMOTE=" + self.def_rem_log), ("REMOTE=" + self.rem_log.value)))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_rem_host, self.rem_host.value))
		cel.close()
		
		zrodlo = open('/scripts/syslogd_script.sh').readlines()
		cel = open('/scripts/syslogd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_rem_port, str(self.rem_port.value)))
		cel.close()


    def start(self):
      		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: syslogd is starting..."))
		os.system("/scripts/syslogd_script.sh start2")
		self.createInfo()
		
    def stop(self):
		self["state"].setText(_("Status: syslogd is stopping..."))
		os.system("/scripts/syslogd_script.sh stop;killall -9 syslogd klogd")
		self.createInfo()
		
    def start_syslogd(self):
		self.save_conf()
		self.close(True)
		
    def cancel(self):
	    self.close(False)
	    
	    
class EGSambaConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGSambaConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_samba,
		      "green": self.cancel,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	
	def createInfo(self):
		os.system("ps > /tmp/smbd.tmp")
		zrodlo = open("/tmp/smbd.tmp", 'r')
		szukana_fraza = '/usr/sbin/smbd -D'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    self["state"].setText(_("Status: Samba is running!"))
		else:
			    self["state"].setText(_("Status: Samba stopped!"))
		os.system("rm -rf /tmp/smbd.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: samba is starting..."))
		os.system("/scripts/samba_script.sh start2")
		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: samba is stopping..."))
		os.system("/scripts/samba_script.sh stop;killall -9 smbd nmbd")
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		
		if fileExists('/scripts/samba_script.sh'):
			f = open('/scripts/samba_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('SAMBA_ON=') != -1):
					self.def_au = line[9:10]
			f.close()
			
			
	def save_conf(self):
		zrodlo = open('/scripts/samba_script.sh').readlines()
		cel = open('/scripts/samba_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("SAMBA_ON=" + self.def_au), ("SAMBA_ON=" + self.au.value)))
		cel.close()	

	def start_samba(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
class EGOpenVPNConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGOpenVPNConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_openvpn,
		      "green": self.showLog,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Log"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	
	def createInfo(self):
		os.system("ps > /tmp/openvpn.tmp")
		zrodlo = open("/tmp/openvpn.tmp", 'r')
		szukana_fraza = '/usr/sbin/openvpn --daemon'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    self["state"].setText(_("Status: OpenVPN is running!"))
		else:
			    self["state"].setText(_("Status: OpenVPN stopped!"))
		os.system("rm -rf /tmp/openvpn.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
	        self.stop()
		self.save_conf()
		self["state"].setText(_("Status: openvpn is starting..."))
		os.system("/scripts/openvpn_script.sh start2")
		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: openvpn is stopping..."))
		os.system("/scripts/openvpn_script.sh stop;killall -9 openvpn")
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		
		if fileExists('/scripts/openvpn_script.sh'):
			f = open('/scripts/openvpn_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('OPENVPN_ON=') != -1):
					self.def_au = line[11:12]
			f.close()
			
			
	def save_conf(self):
		zrodlo = open('/scripts/openvpn_script.sh').readlines()
		cel = open('/scripts/openvpn_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("OPENVPN_ON=" + self.def_au), ("OPENVPN_ON=" + self.au.value)))
		cel.close()	

	def start_openvpn(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
	
	def showLog(self):
		from EGAMI.EGAMI_filemanager import EGFileViewer
		self.session.open(EGFileViewer, "/etc/openvpn/openvpn.log")


class EGFtpConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGFtpConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_ftpd,
		      "green": self.cancel,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
		
		
        def createInfo(self):
	  	self.my_ftp_active = False
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			f = open('/etc/inetd.conf', 'r')
			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == 'ftp':
					self.my_ftp_active = True
					continue
			f.close()
		else:
			fileExists('/etc/inetd.conf')
		if self.my_ftp_active == True:
			self["state"].setText(_("Status: FTP is running!"))
		else:
			self["state"].setText(_("Status: FTP stopped!"))
			
	def createInfo2(self):
		os.system("ps > /tmp/vsftpd.tmp")
		zrodlo = open("/tmp/vsftpd.tmp", 'r')
		szukana_fraza = 'vsftpd'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    print "running!"
			    self["state"].setText(_("Status: FTP is running!"))
		else:
			    print "nie running"
			    self["state"].setText(_("Status: FTP stopped!"))
		os.system("rm -rf /tmp/vsftpd.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
		self["state"].setText(_("Status: FTP is starting..."))
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			inme = open('/etc/inetd.conf', 'r')
			out = open('/etc/inetd.tmp', 'w')
			for line in inme.readlines():
				if line.find('vsftpd') != -1:
					line = line.replace('#', '')
				out.write(line)
			out.close()
			inme.close()
		else:
			fileExists('/etc/inetd.conf')
		if fileExists('/etc/inetd.tmp'):
			fileExists('/etc/inetd.tmp')
			system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			rc = system('killall -HUP inetd')
			rc = system('ps')
		else:
			fileExists('/etc/inetd.tmp')
		

		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: FTP is stopping..."))
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			inme = open('/etc/inetd.conf', 'r')
			out = open('/etc/inetd.tmp', 'w')
			for line in inme.readlines():
				if line.find('vsftpd') != -1:
					line = '#' + line
				out.write(line)
			out.close()
			inme.close()
		else:
			fileExists('/etc/inetd.conf')
		if fileExists('/etc/inetd.tmp'):
			fileExists('/etc/inetd.tmp')
			system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			rc = system('killall -HUP inetd')
			rc = system('ps')
		else:
			fileExists('/etc/inetd.tmp')
			
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			f = open('/etc/inetd.conf', 'r')
			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == 'ftp':
					self.def_au = "1"
					continue
			f.close()	
		else:
			self.def_au = "0"  
			fileExists('/etc/inetd.conf')
			
			
	def save_conf(self):
		if(self.au.value == "1"):
			if fileExists('/etc/inetd.conf'):
				fileExists('/etc/inetd.conf')
				inme = open('/etc/inetd.conf', 'r')
				out = open('/etc/inetd.tmp', 'w')
				for line in inme.readlines():
					if line.find('vsftpd') != -1:
						line = line.replace('#', '')
					out.write(line)
				out.close()
				inme.close()
			else:
				fileExists('/etc/inetd.conf')
			if fileExists('/etc/inetd.tmp'):
				fileExists('/etc/inetd.tmp')
				system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			else:
				fileExists('/etc/inetd.tmp')
		else:
			if fileExists('/etc/inetd.conf'):
				fileExists('/etc/inetd.conf')
				inme = open('/etc/inetd.conf', 'r')
				out = open('/etc/inetd.tmp', 'w')
				for line in inme.readlines():
					if line.find('vsftpd') != -1:
						line = '#' + line
					out.write(line)
				out.close()
				inme.close()
			else:
				fileExists('/etc/inetd.conf')
			if fileExists('/etc/inetd.tmp'):
				fileExists('/etc/inetd.tmp')
				system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			else:
				fileExists('/etc/inetd.tmp')
			  
	def start_ftpd(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
		
class EGTelnetConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGTelnetConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_ftpd,
		      "green": self.cancel,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
		
		
        def createInfo(self):
	  	self.my_ftp_active = False
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			f = open('/etc/inetd.conf', 'r')
			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == 'telnet':
					self.my_ftp_active = True
					continue
			f.close()
		else:
			fileExists('/etc/inetd.conf')
		if self.my_ftp_active == True:
			self["state"].setText(_("Status: Telnet is running!"))
		else:
			self["state"].setText(_("Status: Telnet stopped!"))
			
	def createInfo2(self):
		os.system("ps > /tmp/telnetd.tmp")
		zrodlo = open("/tmp/telnetd.tmp", 'r')
		szukana_fraza = 'telnetd'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    print "running!"
			    self["state"].setText(_("Status: Telnet is running!"))
		else:
			    print "nie running"
			    self["state"].setText(_("Status: Telnet stopped!"))
		os.system("rm -rf /tmp/telnetd.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
		self["state"].setText(_("Status: Telnet is starting..."))
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			inme = open('/etc/inetd.conf', 'r')
			out = open('/etc/inetd.tmp', 'w')
			for line in inme.readlines():
				if line.find('telnetd') != -1:
					line = line.replace('#', '')
				out.write(line)
			out.close()
			inme.close()
		else:
			fileExists('/etc/inetd.conf')
		if fileExists('/etc/inetd.tmp'):
			fileExists('/etc/inetd.tmp')
			system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			rc = system('killall -HUP inetd')
			rc = system('ps')
		else:
			fileExists('/etc/inetd.tmp')
		

		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: Telnet is stopping..."))
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			inme = open('/etc/inetd.conf', 'r')
			out = open('/etc/inetd.tmp', 'w')
			for line in inme.readlines():
				if line.find('telnetd') != -1:
					line = '#' + line
				out.write(line)
			out.close()
			inme.close()
		else:
			fileExists('/etc/inetd.conf')
		if fileExists('/etc/inetd.tmp'):
			fileExists('/etc/inetd.tmp')
			system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			rc = system('killall -HUP inetd')
			rc = system('ps')
		else:
			fileExists('/etc/inetd.tmp')
			
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		if fileExists('/etc/inetd.conf'):
			fileExists('/etc/inetd.conf')
			f = open('/etc/inetd.conf', 'r')
			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == 'telnet':
					self.def_au = "1"
					continue
			f.close()	
		else:
			self.def_au = "0"  
			fileExists('/etc/inetd.conf')
			
			
	def save_conf(self):
		if(self.au.value == "1"):
			if fileExists('/etc/inetd.conf'):
				fileExists('/etc/inetd.conf')
				inme = open('/etc/inetd.conf', 'r')
				out = open('/etc/inetd.tmp', 'w')
				for line in inme.readlines():
					if line.find('telnetd') != -1:
						line = line.replace('#', '')
					out.write(line)
				out.close()
				inme.close()
			else:
				fileExists('/etc/inetd.conf')
			if fileExists('/etc/inetd.tmp'):
				fileExists('/etc/inetd.tmp')
				system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			else:
				fileExists('/etc/inetd.tmp')
		else:
			if fileExists('/etc/inetd.conf'):
				fileExists('/etc/inetd.conf')
				inme = open('/etc/inetd.conf', 'r')
				out = open('/etc/inetd.tmp', 'w')
				for line in inme.readlines():
					if line.find('telnetd') != -1:
						line = '#' + line
					out.write(line)
				out.close()
				inme.close()
			else:
				fileExists('/etc/inetd.conf')
			if fileExists('/etc/inetd.tmp'):
				fileExists('/etc/inetd.tmp')
				system('mv -f  /etc/inetd.tmp /etc/inetd.conf')
			else:
				fileExists('/etc/inetd.tmp')
			  
	def start_ftpd(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		
class EGPcscdConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGPcscdConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("1", _("Yes")), ("0", _("No"))])
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_samba,
		      "green": self.cancel,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	
	def createInfo(self):
		os.system("ps > /tmp/pcscd.tmp")
		zrodlo = open("/tmp/pcscd.tmp", 'r')
		szukana_fraza = '/usr/sbin/pcscd'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    self["state"].setText(_("Status: Pcscd is running!"))
		else:
			    self["state"].setText(_("Status: Pcscd stopped!"))
		os.system("rm -rf /tmp/pcscd.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: pcscd is starting..."))
		os.system("/scripts/pcscd_script.sh start2")
		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: pcscd is stopping..."))
		os.system("/scripts/pcscd_script.sh stop;killall -9 pcscd")
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		
		if fileExists('/scripts/pcscd_script.sh'):
			f = open('/scripts/pcscd_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('PCSCD_ON=') != -1):
					self.def_au = line[9:10]
			f.close()
			
			
	def save_conf(self):
		zrodlo = open('/scripts/pcscd_script.sh').readlines()
		cel = open('/scripts/pcscd_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("PCSCD_ON=" + self.def_au), ("PCSCD_ON=" + self.au.value)))
		cel.close()	

	def start_samba(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)
		

class EGDropbearConfig(ConfigListScreen, Screen):
	def __init__(self, session):
		self.skin = EGDropbearConfig_Skin
		Screen.__init__(self, session)
		session = None	
		
		self.load_conf()
			
		self.au = ConfigSelection(default = self.def_au, choices = [("0", _("Yes")), ("1", _("No"))])
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
		      "cancel": self.cancel,
		      "red": self.start_samba,
		      "green": self.cancel,
		      "yellow" : self.start,
		      "blue" : self.stop
		}, -2)
			
		self["key_red"] = Label(_("Save"))		
		self["key_green"] = Label(_("Cancel"))		
		self["key_yellow"] = Label(_("Start"))
		self["key_blue"] = Label(_("Stop"))
		
		self["state"] = Label()
		
		self.createInfo()
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Autostart:"), self.au))
        	
	def createInfo(self):
		os.system("ps > /tmp/drop.tmp")
		zrodlo = open("/tmp/drop.tmp", 'r')
		szukana_fraza = '/usr/sbin/dropbear'
		if (wyszukaj_in(zrodlo,szukana_fraza)):
			    self["state"].setText(_("Status: DropBear is running!"))
		else:
			    self["state"].setText(_("Status: DropBear stopped!"))
		os.system("rm -rf /tmp/drop.tmp")
		zrodlo.seek(0)
		zrodlo.close()
	    
	def start(self):
		zrodlo = open('/etc/init.d/dropbear').readlines()
		cel = open('/etc/init.d/dropbear', 'w')
		for s in zrodlo:
			cel.write(s.replace(("NO_START=" + self.def_au), "NO_START=0"))
		cel.close()
		self.stop()
		self.save_conf()
		self["state"].setText(_("Status: dropbear is starting..."))
		os.system("/etc/init.d/dropbear start")
		self.createInfo()
		
	def stop(self):
		self["state"].setText(_("Status: dropbear is stopping..."))
		os.system("/etc/init.d/dropbear stop;killall -9 dropbear")
		self.createInfo()
		
	def cancel(self):
	      self.close(False)


	def load_conf(self):
		self.def_au = "0"
		
		if fileExists('/etc/init.d/dropbear'):
			f = open('/etc/init.d/dropbear', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('NO_START=') != -1):
					self.def_au = line[9:10]
			f.close()
			
			
	def save_conf(self):
		zrodlo = open('/etc/init.d/dropbear').readlines()
		cel = open('/etc/init.d/dropbear', 'w')
		for s in zrodlo:
			cel.write(s.replace(("NO_START=" + self.def_au), ("NO_START=" + self.au.value)))
		cel.close()	

	def start_samba(self):
		self.save_conf()
		self.createInfo()
		self.load_conf()
		self.close(True)