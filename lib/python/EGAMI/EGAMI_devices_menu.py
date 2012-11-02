# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console 
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop 
from Screens.MessageBox import MessageBox
from Screens.Console import Console

from Plugins.Plugin import PluginDescriptor

from enigma import eTimer 

from Components.ConfigList import ConfigListScreen 
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, NoSave, ConfigInteger, configfile 
from Components.Sources.List import List 
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Button import Button
from Components.Harddisk import harddiskmanager
import re
import os
from os import system, remove as os_remove, rename as os_rename, popen 
from os import system, rename, path, mkdir, remove, statvfs, listdir
import time 
import datetime 

from Tools.LoadPixmap import LoadPixmap 
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN

from EGAMI.EGAMI_tools import wyszukaj_re, runBackCmd
from EGAMI.EGAMI_skins import EGHardDriveInfo_Skin, EGDeviceManager_Skin, EGDeviceManager_Setup_Skin

class HardDriveInfo(Screen):
    def __init__(self, session, args = 0):
	self.skin = EGHardDriveInfo_Skin
	Screen.__init__(self, session)
        self.menu = args
        list = []
        list.append((_("Current information directly"), "001"))
	list.append((_(" "), ""))
	list.append((_("Perform cache read timings"), "002"))
	list.append((_("Perform device read timings"), "003"))
	list.append((_(" "), ""))
	list.append((_("Device temperature info"), "004"))
	list.append((_("Updating device list"), "005"))
        self["menu"] = MenuList(list)
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"],{"ok": self.go,"back": self.close,}, -1)
        
    def go(self):
        returnValue = self["menu"].l.getCurrentSelection()[1]
        if returnValue is not None:
           if returnValue is "001":
 	       self.session.open(Console,_("Current information directly"),["cat hdparm -I /dev/sda1"])
	   elif returnValue is "002":
 	       self.session.open(Console,_("Perform cache read timings"),["cat hdparm -T /dev/sda1"])
	   elif returnValue is "003":
 	       self.session.open(Console,_("Perform device read timings"),["cat hdparm -t /dev/sda1"])
	   elif returnValue is "004":
 	       self.session.open(Console,_("Device temperature info"),["cat hddtemp /dev/sda1"])
	   elif returnValue is "005":
 	       self.session.open(Console,_("Updating device list"),["if wget \"http://www.guzu.net/linux/hddtemp.db\" -q -O /var/etc/hddtemp.db ; then exit 0; else exit 1; fi"])

class EGDeviceManager(Screen):
    def __init__(self, session):
	self.skin = EGDeviceManager_Skin
        Screen.__init__(self, session)
	
        self["key_red"] = Button(_("Mountpoints"))
        self["key_yellow"] = Button(_("Format"))
	self["key_blue"] = Button(_("Setup HDD"))
	self["key_green"] = Button(_("Informations"))
	
        self["key_yellow_png"] = Pixmap()
        self["key_blue_png"] = Pixmap()	
        self["key_red_png"] = Pixmap()
        self["key_green_png"] = Pixmap()
		
        self["lab1"] = Label(_("Wait please while scanning your stb devices..."))
	
        self.list = []
        self["list"] = List(self.list)
	
        self["actions"] = ActionMap(["WizardActions",
         "ColorActions"], {"back": self.close,
         "red": self.mountUmount,
         "yellow": self.myFormat,
	 "blue" : self.setupHDD,
	 "green" : self.informationsHDD})
	 
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateList2)
        self.updateList()
	
	self["list"].onSelectionChanged.append(self.selectionChanged)



    def updateList(self):
        self.activityTimer.start(10)

			
    def updateList2(self):
                self.activityTimer.stop()
                self.list = []
                list2 = []
                f = open('/proc/partitions', 'r')
                for line in f.readlines():
                        parts = line.strip().split()
                        if not parts:
                                continue
                        device = parts[3]
                        if not re.search('sd[a-z][1-9]',device):
                                continue
                        if device in list2:
                                continue
                        self.buildMy_rec(device)
                        list2.append(device)

                f.close()
                self['list'].list = self.list
                self['lab1'].hide()


    def buildMy_rec(self, device):
		mypath = resolveFilename(SCOPE_CURRENT_SKIN)
		if not fileExists(mypath + "egami_icons"):
		    mypath = "/usr/share/enigma2/skin_default/"
		    
                try:
                        if device.find('1') > 0:
                                device2 = device.replace('1', '')
                except:
                        device2 = ''
                try:
                        if device.find('2') > 0:
                                device2 = device.replace('2', '')
                except:
                        device2 = ''
                try:
                        if device.find('3') > 0:
                                device2 = device.replace('3', '')
                except:
                        device2 = ''
                try:
                        if device.find('4') > 0:
                                device2 = device.replace('4', '')
                except:
                        device2 = ''
                devicetype = path.realpath('/sys/block/' + device2 + '/device')
                d2 = device
                name = 'USB: '
                mypixmap = mypath + 'egami_icons/dev_usb.png'
                model = file('/sys/block/' + device2 + '/device/model').read()
                model = str(model).replace('\n', '')
                des = ''
		dev = ''
                if devicetype.find('/devices/pci') != -1:
                        name = _("HARD DISK: ")
                        mypixmap = mypath + 'egami_icons/dev_hdd.png'
                        dev = 'HDD'
		if devicetype.find('{size}') != -1:
			cap = devicetype.replace('ATTR{size}==', '')
			cap = cap[1:-1]
			cap = int(cap)
			cap = cap / 1000 * 512 / 1000
			cap = '%d.%03d GB' % (cap / 1000, cap % 1000)
			des = (_("Size: ")) + cap
		if devicetype.find('{model}') != -1:
			name2 = devicetype.replace('ATTRS{model}==', '')
			name2 = name2[1:-1]
			if name2.find('USB CF Reader') != -1:
				name = (_("COMPACT FLASH: "))
				mypixmap = mypath + 'egami_icons/dev_cf.png'
			else:
				if name2.find('USB SD Reader') != -1:
					name = (_("SD CARD: "))
					mypixmap = mypath + 'egami_icons/dev_sd.png'
			name = name + name2
                name = name + model
                f = open('/proc/mounts', 'r')
                for line in f.readlines():
                        if line.find(device) != -1:
                                parts = line.strip().split()
                                d1 = parts[1]
                                dtype = parts[2]
                                rw = parts[3]
                                break
                                continue
                        else:
                                d1 = _("None")
                                dtype = _("unavailable")
                                rw = _("None")
                f.close()
                f = open('/proc/partitions', 'r')
                for line in f.readlines():
                        if line.find(device) != -1:
                                parts = line.strip().split()
                                size = int(parts[2])
                                if ((size / 1024) / 1024) > 1:
                                        des = _("Size: ") + str((size / 1024) / 1024) + _("GB")
                                else:
                                        des = _("Size: ") + str(size / 1024) + _("MB")
                        else:
                                try:
                                        size = file('/sys/block/' + device2 + '/' + device + '/size').read()
                                        size = str(size).replace('\n', '')
                                        size = int(size)
                                except:
                                        size = 0
                                if (((size / 2) / 1024) / 1024) > 1:
                                        des = _("Size: ") + str(((size / 2) / 1024) / 1024) + _("GB")
                                else:
                                        des = _("Size: ") + str((size / 2) / 1024) + _("MB")
                f.close()
                if des != '':
                        if rw.startswith('rw'):
                                rw = ' R/W'
                        elif rw.startswith('ro'):
                                rw = ' R/O'
                        else:
                                rw = ""                 
                        des += '\t' + _("Mount: ") + d1 + '\n' + _("Device: ") + '/dev/' + device + '\t' + _("Type: ") + dtype + rw
                        png = LoadPixmap(mypixmap)
                        res = (name, des, png, dev)
                        self.list.append(res)
		else:
			  res = ("ERROR!!!\n", "There are no devices connected to your set-top-box", "", "NONE")
			  self.list.append(res)


    def mountUmount(self):
        self.session.openWithCallback(self.updateList, EGDeviceManager_Setup)



    def myFormat(self):
		sel = self['list'].getCurrent()
		if sel:
			sel
			name = sel[0]
			des = sel[1]
			if des.find('Not Found') != -1:
				self.session.open(MessageBox, des, MessageBox.TYPE_INFO)
			elif name.find('DVD DRIVE') != -1:
				self.session.open(MessageBox,text = _("You cannot format DVD drive."), type = MessageBox.TYPE_INFO)
			elif name.find('HARD DISK') != -1:
				self.session.open(MessageBox,text = _("You cannot format HDD with this tool.\nPlease use Hdd manager in Main Menu"), type = MessageBox.TYPE_INFO)
			else:
				des = des.replace('\n', '\t')
				parts = des.strip().split('\t')
				mountp = parts[1].replace('Mount: ', '')
				device = parts[2].replace('Device: ', '')
				self.nformat = name
				self.mformat = mountp
				self.dformat = device
				mess1 = (_("Warning you are going to format ")) 
				mess2 = (_("\nALL THE DATA ON THIS DEVICE WILL BE LOST!\n Are you sure to continue?"))
				mess = mess1 + name + mess2
				self.session.openWithCallback(self.myFormatDo, MessageBox, mess, MessageBox.TYPE_YESNO)
		else:
			sel

    def myFormatDo(self, answer):
		if answer is True:
			target = self.mformat
			device = self.dformat.replace('1', '')
			check = system('killall automount')
			if target != 'NOT MAPPED':
				cmd = 'umount ' + target
				check = system(cmd)
			cmd = 'umount ' + self.dformat
			check = system(cmd)
			check = system('umount /dev/sda')
			check = system('umount /dev/sda1')
			check = system('umount /dev/sdb')
			check = system('umount /dev/sdb1')
			check = system('umount /dev/sdc')
			check = system('umount /dev/sdc1')
			check = system('umount /dev/sdd')
			check = system('umount /dev/sdd1')
			check = system('umount /dev/sde')
			check = system('umount /dev/sde1')
			mycmd = "echo -e '------------------------------------\nPartitioning: " + self.nformat + "\n------------------------------------\n\n\n ' "
			mycmd2 = 'printf "0,\n;\n;\n;\ny\n" | sfdisk -f ' + device
			self.session.open(Console, title='Partitioning...', cmdlist=[mycmd, mycmd2], finishedCallback=self.myFormatDo2)

    def myFormatDo2(self):
		target = self.mformat
		device = self.dformat.replace('1', '')
		check = system('umount /dev/sda')
		check = system('umount /dev/sda1')
		check = system('umount /dev/sdb')
		check = system('umount /dev/sdb1')
		check = system('umount /dev/sdc')
		check = system('umount /dev/sdc1')
		check = system('umount /dev/sdd')
		check = system('umount /dev/sdd1')
		check = system('umount /dev/sde')
		check = system('umount /dev/sde1')
		mycmd = "echo -e '------------------------------------\nFormatting: " + self.nformat + "\n------------------------------------\n\n\n ' "
		mycmd2 = '/sbin/mkfs.ext3 ' + device + '1'
		self.session.open(Console, title='Formatting...', cmdlist=[mycmd, mycmd2], finishedCallback=self.updateuuid)



    def updateuuid(self):
        mybox = self.session.openWithCallback(self.hreBoot, MessageBox, (_("The Box will be now restarted to remount devices.\nDon't forget to remap your device after the reboot.\nPress ok to continue")), MessageBox.TYPE_INFO)



    def hreBoot(self, answer):
	system("reboot -f")
        self.session.open(TryQuitMainloop, 2)
	
    def selectionChanged(self, sel = None):
	self["key_blue"].hide()
	self["key_blue_png"].hide()
	self["key_green"].hide()
	self["key_green_png"].hide()
	self["key_yellow"].hide()
	self["key_yellow_png"].hide()
	cur = (sel or self["list"].getCurrent())
	try:
	  if (cur[3] == "HDD"):
		  self["key_blue"].setText(_("Setup"))
		  self["key_blue"].show()
		  self["key_blue_png"].show()
		  self["key_green"].show()
		  self["key_green_png"].show()
	  elif (cur[3] == "DVD"):
		  self["key_blue"].setText(_("Eject"))
		  self["key_blue"].show()
		  self["key_blue_png"].show()
		  self["key_green"].hide()
		  self["key_green_png"].hide()
	  elif (cur[3] == "NONE"):
		  self["key_blue"].hide()
		  self["key_blue_png"].hide()
		  self["key_red"].hide()
		  self["key_red_png"].hide()
		  self["key_green"].hide()
		  self["key_green_png"].hide()
		  self["key_yellow"].hide()
		  self["key_yellow_png"].hide()
	  else:
		  self["key_blue"].hide()
		  self["key_blue_png"].hide()
		  self["key_green"].hide()
		  self["key_green_png"].hide()
		  self["key_yellow"].show()
		  self["key_yellow_png"].show()
	except:
		  self["key_blue"].hide()
		  self["key_blue_png"].hide()
		  self["key_red"].hide()
		  self["key_red_png"].hide()
		  self["key_green"].hide()
		  self["key_green_png"].hide()
		  self["key_yellow"].hide()
		  self["key_yellow_png"].hide()


    def setupHDD(self):
	cur = self["list"].getCurrent()
	if (cur[3] == "HDD"):
		from Screens.Setup import Setup
	    	self.session.open(Setup, "harddisk")
	elif (cur[3] == "DVD"):
		system("eject /dev/sr0")
	    
    def informationsHDD(self):
	cur = self["list"].getCurrent()
	if (cur[3] == "HDD"):
	    self.session.open(HardDriveInfo)
	    

class EGDeviceManager_Setup(Screen,
 ConfigListScreen):
    def __init__(self, session):
	self.skin = EGDeviceManager_Setup_Skin
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self["key_yellow"] = Label(_("Unmount All"))
        self["actions"] = ActionMap(["WizardActions", "ColorActions"], 
        {"back": self.close,
         "green": self.saveMypoints,
	 "blue" : self.close,
	 "yellow": self.deleteMypoints,
	 "red" : self.close})
	 
        self.updateList()
	
    def updateList(self):
                self.list = []
                list2 = []
                f = open('/proc/partitions', 'r')
                for line in f.readlines():
                        parts = line.strip().split()
                        if not parts:
                                continue
                        device = parts[3]
                        if not re.search('sd[a-z][1-9]',device):
                                continue
                        if device in list2:
                                continue
                        self.buildMy_rec(device)
                        list2.append(device)
                f.close()
                self['config'].list = self.list
                self['config'].l.setList(self.list)




    def buildMy_rec(self, device):
                try:
                        if device.find('1') > 0:
                                device2 = device.replace('1', '')
                except:
                        device2 = ''
                try:
                        if device.find('2') > 0:
                                device2 = device.replace('2', '')
                except:
                        device2 = ''
                try:
                        if device.find('3') > 0:
                                device2 = device.replace('3', '')
                except:
                        device2 = ''
                try:
                        if device.find('4') > 0:
                                device2 = device.replace('4', '')
                except:
                        device2 = ''
                devicetype = path.realpath('/sys/block/' + device2 + '/device')
                d2 = device
                name = 'USB: '
                model = file('/sys/block/' + device2 + '/device/model').read()
                model = str(model).replace('\n', '')
                des = ''
                if devicetype.find('/devices/pci') != -1:
                        name = _("HARD DISK: ")
                name = name + model
                f = open('/proc/mounts', 'r')
                for line in f.readlines():
                        if line.find(device) != -1:
                                parts = line.strip().split()
                                d1 = parts[1]
                                dtype = parts[2]
                                break
                                continue
                        else:
                                d1 = _("None")
                                dtype = _("unavailable")
                f.close()
                f = open('/proc/partitions', 'r')
                for line in f.readlines():
                        if line.find(device) != -1:
                                parts = line.strip().split()
                                size = int(parts[2])
                                if ((size / 1024) / 1024) > 1:
                                        des = _("Size: ") + str((size / 1024) / 1024) + _("GB")
                                else:
                                        des = _("Size: ") + str(size / 1024) + _("MB")
                        else:
                                try:
                                        size = file('/sys/block/' + device2 + '/' + device + '/size').read()
                                        size = str(size).replace('\n', '')
                                        size = int(size)
                                except:
                                        size = 0
                                if (((size / 2) / 1024) / 1024) > 1:
                                        des = _("Size: ") + str(((size / 2) / 1024) / 1024) + _("GB")
                                else:
                                        des = _("Size: ") + str((size / 2) / 1024) + _("MB")
                f.close()
                item = NoSave(ConfigSelection(default='/media/' + device, choices=[('/media/' + device, '/media/' + device),
                ('/media/hdd', '/media/hdd'),
                ('/media/hdd2', '/media/hdd2'),
                ('/media/hdd3', '/media/hdd3'),
                ('/media/usb', '/media/usb'),
                ('/media/usb2', '/media/usb2'),
                ('/media/usb3', '/media/usb3')]))
                if (d1 == '/media/egamiboot'):
                        item = NoSave(ConfigSelection(default='/media/egamiboot', choices=[('/media/egamiboot', '/media/egamiboot')]))
                if dtype == 'Linux':
                        dtype = 'ext3'
                else:
                        dtype = 'auto'
                item.value = d1.strip()
                text = name + ' ' + des + ' /dev/' + device
                res = getConfigListEntry(text, item, device, dtype)

                if des != '' and self.list.append(res):
                        pass




    def saveMypoints(self):
                mycheck = False
                for x in self['config'].list:
                        self.device = x[2]
                        system('umount /dev/' + self.device)
                        file('/etc/fstab.tmp', 'w').writelines([l for l in file('/etc/fstab').readlines() if self.device not in l])
                        rename('/etc/fstab.tmp','/etc/fstab')

                for x in self['config'].list:
                        self.device = x[2]
                        self.mountp = x[1].value
                        self.type = x[3]
                        if not path.exists(self.mountp):
                                mkdir(self.mountp, 0755)
                        out = open('/etc/fstab', 'a')
                        line = '/dev/' + self.device + '            ' + self.mountp + '           ' + self.type + '       defaults              0 0\n'
                        out.write(line)
                        out.close()
                        system('mount /dev/' + self.device)

                message = _("Devices changes need a system restart to take effects.\nRestart your Box now?")
                ybox = self.session.openWithCallback(self.restBo, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_("Restart box."))

    def deleteMypoints(self):
	system("unmount /mnt/card;umount /mnt/cf;umount /mnt/hdd;umount /mnt/usb;umount /mnt/usb2;umount /mnt/usb3")
        nobox = self.session.open(MessageBox, (_("EGAMI Devices Manager has just unmounted all your devices.")), MessageBox.TYPE_INFO, 3)
        nobox.setTitle(_("Info"))
	self.close()
	
    def restBo(self, answer):
        if (answer is True):
	    system("reboot -f")
            self.session.open(TryQuitMainloop, 2)
        else:
            self.close()

