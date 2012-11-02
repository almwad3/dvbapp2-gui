from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox 
from Screens.Console import Console 

from Components.Sources.List import List
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label 
from Components.ScrollLabel import ScrollLabel 
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Network import iNetwork

from Plugins.SystemPlugins.NetworkBrowser.NetworkBrowser import NetworkBrowser

from Tools.Directories import fileExists

from EGAMI.EGAMI_tools import runBackCmd, unload_modules, wyszukaj_re, checkkernel, wyszukaj_in
from EGAMI.EGAMI_skins import EGProcessInfo_Skin, EGKernelInfo_Skin, EGAdvancedStreamInfo_Skin, EGSmartScript_Skin, EGSwapManager_Skin, EGKernelModulesManager_Skin
 

import time, os

class EGSwapManager(ConfigListScreen, Screen):
    def __init__(self, session):

		self.skin = EGSwapManager_Skin
		Screen.__init__(self, session)
		
		self.load_conf()
		
		self.enable = ConfigSelection(default=self.def_enable, choices = [("1", _("Yes")), ("0", _("No"))])
		self.size = ConfigSelection(default = self.def_size, choices = [("8192", _("8 MB")), ("16384", _("16 MB")),("32768", _("32 MB")),("65536", _("64 MB")),("131072", _("128 MB")),("262144", _("256 MB")),("524288", _("512 MB")),("1048576", _("1 GB"))])
		self.place = ConfigSelection(default=self.def_place, choices = ["/media/usb","/media/hdd","/media/cf","/media/mbX","/media/ba"])
		self.name = ConfigText(default = self.def_name, fixed_size = False)
		
		self.createSetup()
		
		ConfigListScreen.__init__(self, self.list, session = session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
			"ok": self.cancel,
			"cancel": self.cancel,
			"red": self.active_swap,
			"green": self.deactive_swap,
			"yellow": self.remove_swap,
			"blue": self.create_swap
		}, -2)
		
		self["key_red"] = Label(_("Active"))		
		self["key_green"] = Label(_("Deactive"))		
		self["key_yellow"] = Label(_("Remove"))
		self["key_blue"] = Label(_("Create"))
		self["state"] = Label()
		
		self.createInfo()
		
		
    def createInfo(self):
	    	os.system("cat /proc/swaps > /tmp/swaps.tmp")
		zrodlo = open("/tmp/swaps.tmp", 'r')
		szukana_fraza = 'file'
		file = ((self.def_place) + self.def_name)
		if fileExists(file):
			self["state"].setText(_((((((("Swapfile exist: "  + file) + " ") + self.def_size) + " MB on ") + self.def_place + "\n\nPress Red Button to active"))))
			if wyszukaj_in(zrodlo,szukana_fraza):
					self["state"].setText(_((((((("Swapfile actived: "  + file) + " ") + self.def_size) + " MB on ") + self.def_place + "\n\nPress Green Button to deactive"))))
		else:
			self["state"].setText(_("Swapfile does not exist\n\nPress Blue Button to create"))
		os.system("rm -rf /tmp/swaps.tmp")
	   	zrodlo.seek(0)
	   	zrodlo.close()
				
    def load_conf(self):
		self.def_enable = "0"
		self.def_size = "8192"
		self.def_place = "/media/hdd"
		self.def_name = "/swapfile"
		
		if fileExists('/scripts/swap_script.sh'):
			f = open('/scripts/swap_script.sh', 'r')
			for line in f.readlines():
				line = line.strip()
				if (line.find('SWAP_ON=') != -1):
					self.def_enable = line[8:]
				elif (line.find('SWAP_PATH=') != -1):
					self.def_place = line[10:]
				elif (line.find('SWAP_SIZE=') != -1):
					self.def_size = line[10:]
				elif (line.find('SWAP_FILE=') != -1):
					self.def_name = line[10:]
			f.close()

			
    def active_swap(self):
	        self.enable.value = "1"
		self.save_conf()
		runBackCmd("/scripts/swap_script.sh start")
		self.session.open(MessageBox, _("Please wait...activing swapfile!!!"), MessageBox.TYPE_INFO, timeout=3)
		self.load_conf()
		time.sleep(1)
		self.createInfo()

    def deactive_swap(self):
	    	self.enable.value = "0"
		self.save_conf()
		runBackCmd("/scripts/swap_script.sh stop")
		self.session.open(MessageBox, _("Please wait...deactiving swapfile!!!"), MessageBox.TYPE_INFO, timeout=4)
		time.sleep(1)
		self.load_conf()	
		self.createInfo()

    def remove_swap(self):
	    	self.enable.value = "0"
		runBackCmd("/scripts/swap_script.sh delete")
		self.session.open(MessageBox, _("Please wait...removing swapfile!!!"), MessageBox.TYPE_INFO, timeout=4)
		self.load_conf()
		time.sleep(1)
		self.createInfo()

    def create_swap(self):
	        self.enable.value = "1"
		self.save_conf()
		runBackCmd("/scripts/swap_script.sh create")
		self.session.open(MessageBox, _("Please wait...creating swapfile!!!"), MessageBox.TYPE_INFO, timeout=6)
		time.sleep(1)
		self.load_conf()
		self.createInfo()
		
    def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("enable/disable Swap:"), self.enable))
		self.list.append(getConfigListEntry(_("Swap Size:"), self.size))
		self.list.append(getConfigListEntry(_("Swap Place:"), self.place))
		self.list.append(getConfigListEntry(_("Swap File Name:"), self.name))
		

    def save_conf(self):
		zrodlo = open('/scripts/swap_script.sh').readlines()
		cel = open('/scripts/swap_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(("SWAP_ON=" + self.def_enable), ("SWAP_ON=" + self.enable.value)))
		cel.close()
		zrodlo = open('/scripts/swap_script.sh').readlines()
		cel = open('/scripts/swap_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_size, self.size.value))
		cel.close()
		zrodlo = open('/scripts/swap_script.sh').readlines()
		cel = open('/scripts/swap_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_place, self.place.value))
		cel.close()
		zrodlo = open('/scripts/swap_script.sh').readlines()
		cel = open('/scripts/swap_script.sh', 'w')
		for s in zrodlo:
			cel.write(s.replace(self.def_name, self.name.value))
		cel.close()
		
    def cancel(self):
		self.close()

class EGSetupHttpStream(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="700,500" title="Http stream settings">
		<widget name="config" position="10,10" size="680,430" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="140,450" size="140,40" alphatest="on" />
		<widget name="key_red" position="140,450" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<ePixmap position="420,450" size="140,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />
		<widget name="key_green" position="420,450" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.keyCancel,
			"back": self.keyCancel,
			"green": self.keySave,

		}, -2)
						
		self.list.append(getConfigListEntry(_("Include EIT in http streams"), config.streaming.stream_eit))
		self.list.append(getConfigListEntry(_("Include AIT in http streams"), config.streaming.stream_ait))
		self.list.append(getConfigListEntry(_("Include ECM in http streams"), config.streaming.stream_ecm))
		self.list.append(getConfigListEntry(_("Descramble http streams"), config.streaming.descramble))
		
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keySave(self):
		for x in self["config"].list:
			x[1].save()
		self.close()

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()
	    
	    
class SmartScript(Screen):
    def __init__(self, session):
	self.skin = EGSmartScript_Skin
	Screen.__init__(self, session)
        self['statuslab'] = Label(_('N/A'))
        self['key_red'] = Label(_('Run'))
        self.mlist = []
        self.populateSL()
        self['list'] = MenuList(self.mlist)
        self['list'].onSelectionChanged.append(self.schanged)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], 
         {
	 'red': self.mygo,  
	 'ok': self.mygo,
         'back': self.close
         })
        self.onLayoutFinish.append(self.refr_sel)

    def refr_sel(self):
        self['list'].moveToIndex(1)
        self['list'].moveToIndex(0)

    def populateSL(self):
        self.scriptdesc = {}
        myscripts = os.listdir('/usr/scripts')
        for fil in myscripts:
            if (fil.find('_smartscript.sh') != -1):
                fil2 = fil[:-15]
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
        mysel2 = (('/usr/scripts/' + mysel) + '_smartscript.sh')
        mytitle = ('SmartScript Tool: ' + mysel)
        self.session.open(Console, title=mytitle, cmdlist=[mysel2])
	
	
class DvbSnoop(Screen):
    def __init__(self, session, args = 0):
	self.skin = EGAdvancedStreamInfo_Skin
	Screen.__init__(self, session)
        self.menu = args
        list = []
        list.append((_("PAT Info"), "1"))
	list.append((_("CAT Info"), "2"))
	list.append((_("NIT Info"), "3"))
	#list.append((_("SDT/BAT Info"), "4"))
	list.append((_("EIT/TOT/TDT Info"), "5"))
	list.append((_("ECM Info"), "7"))
	list.append((_("DVB Snoop Help"), "8"))
        self["menu"] = MenuList(list)
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"],{"ok": self.go,"back": self.close,}, -1)
        
    def go(self):
        returnValue = self["menu"].l.getCurrentSelection()[1]
        if returnValue is not None:
           if returnValue is "1":
 	       self.session.open(Console,_("Stream advanced info - PAT"),["/usr/bin/dvbsnoop -n 1 -hideproginfo 0x0000"])
	   elif returnValue is "2":
 	       self.session.open(Console,_("Stream advanced info - CAT"),["/usr/bin/dvbsnoop -n 1 -hideproginfo 0x0001"])
	   elif returnValue is "3":
 	       self.session.open(Console,_("Stream advanced info - NIT"),["/usr/bin/dvbsnoop -n 1 -hideproginfo 0x0010"])
	   elif returnValue is "4":
 	       self.session.open(Console,_("Stream advanced info - SDT/BAT"),["/usr/bin/dvbsnoop -n 1 -hideproginfo 0x0011"])
	   elif returnValue is "5":
 	       self.session.open(Console,_("Stream advanced info - EIT/TOT/TDT"),["/usr/bin/dvbsnoop -n 1 -hideproginfo 0x0012"])
	   elif returnValue is "6":
 	       self.session.open(Console,_("Stream advanced info - PMT"),["/usr/bin/dvbsnoop -if /tmp/pmt.tmp -hideproginfo"])
	   elif returnValue is "7":
 	       self.session.open(Console,_("Stream advanced info - ECM"),["cat /tmp/ecm.info"])
	   elif returnValue is "8":
 	       self.session.open(Console,_("Stream advanced info - Help"),["/usr/bin/dvbsnoop -help"])
 	       
class EGProcessInfo(Screen):
	def __init__(self, session, args = 0):
	
		self.skin = EGProcessInfo_Skin
		Screen.__init__(self, session)
		self.menu = args
		
		self.list = []
				
		self["menu"] = MenuList(self.list)
		
        	self["key_red"] = Button(_("Menu"))
        	self["key_green"] = Button(_("Show details"))
		
		self.onLayoutFinish.append(self.fillList)
		
		self["actions"] = ActionMap(["EGActions"],
		{
			"ok": self.KeyOk,
			"red": self.KeyRed,
			"green": self.KeyGreen,
			"exit": self.Exit,
		}, -1)
	
	def fillList(self):
        	count = 0
        	for line in os.popen('ps', 'r').readlines():
            		count += 1
			x=line.strip().split()
			try:
				pro_str = str(x[0]) + "\t" + x[1] + "\t" + str(x[3]) + "\t" + str(x[4])
			except:
				pro_str = str(x[0]) + "\t" + x[1] + "\t\t" + str(x[3])
			self.list.append((pro_str))
		self["menu"].setList(self.list)
		self["menu"].moveToIndex(1)
		

	def fillList2(self):
		self["menu"].setList(self.list)
		self["menu"].moveToIndex(1)
	
	def KeyOk(self):
		self.showDetails()

	def KeyGreen(self):
		self.showDetails()

	def KeyRed(self):
		val = self["menu"].l.getCurrentSelection()
		val=val.strip().split()
		if val:
			menu = []
			menu.append(("SIGHUP", 0))
			menu.append(("SIGINT", 0))
			menu.append(("SIGQUIT", 0))
			menu.append(("SIGTRAP", 0))
			menu.append(("SIGABRT", 0))
			menu.append(("SIGKILL", 0))
			menu.append(("SIGUSR1", 0))
			menu.append(("SIGALRM", 0))
			menu.append(("SIGTERM", 0))
			menu.append(("SIGCONT", 0))
			menu.append(("SIGSTOP", 0))
			self.session.openWithCallback(self.__menuCallback, ChoiceBox, list=menu, title=_("send signal to this process...") + "\n" + val[3])

	def __menuCallback(self, val):
		if val != None:
			val_2 = self["menu"].l.getCurrentSelection()
			val_2=val_2.strip().split()
			cmd = "killall -" + val[0] + " " + val_2[3]
			runBackCmd(cmd)
			os.system("ps > /tmp/.ps")
			self.__fillList()
			self.fillList2()
			
	def showDetails(self):
		val = self["menu"].l.getCurrentSelection()
		val=val.strip().split()
		if val:
			cmd = "cat /proc/" + str(val[0]) + "/status"
			self.session.open(Console,_("Details"),[cmd])
		
	def Exit(self):
		self.close()
		unload_modules(__name__)
		
class EGKernelInfo(Screen):
	def __init__(self, session, args = 0):
	
		self.skin = EGKernelInfo_Skin
		Screen.__init__(self, session)
		self.menu = args
		
        	self.list = []
        	self['menu'] = MenuList(self.list)
        	self.onLayoutFinish.append(self.fillList)
		
		self["actions"] = ActionMap(["EGActions"],
		{
			"exit": self.Exit,
		}, -1)
	
	def fillList(self):
        	count = 0
        	for x in os.popen('dmesg', 'r').readlines():
            		count += 1
			self.list.append(x)
			
		self["menu"].l.setList(self.list)
		self["menu"].moveToIndex((count - 1))

	def Exit(self):
		self.close()
		unload_modules(__name__)
		
class EGEnigma2ConfigInfo(Screen):
	def __init__(self, session, args = 0):
	
		self.skin = EGKernelInfo_Skin
		Screen.__init__(self, session)
		self.menu = args
		
		self.__fillList()
				
		self["menu"] = MenuList(self.list)

		self.onLayoutFinish.append(self.fillList2)
		
		self["actions"] = ActionMap(["EGActions"],
		{
			"exit": self.Exit,
		}, -1)
	
	def __fillList(self):
		self.list = []
		f = open("/etc/enigma2/settings", "r")
		for line in f.readlines():
			x=line.strip()
			pro_str = str(x)
			self.list.append((pro_str))
		f.close()
		
	def fillList2(self):
		self["menu"].setList(self.list)
		self["menu"].moveToIndex(0)

	def Exit(self):
		self.close()
		unload_modules(__name__)
		
		
class EGNetBrowser(Screen):
	skin = """
	<screen position="center,center" size="800,520" title="Select Network Interface">
	      <widget source="list" render="Listbox" position="10,10" size="780,460" scrollbarMode="showOnDemand" >
	      <convert type="StringList" />
	      </widget>
	      <ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />
	      <ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />
	      <widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	      <widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
	</screen>"""

	def __init__(self, session):
	    Screen.__init__(self, session)

	    self["key_red"] = Label(_("Select"))
	    self["key_yellow"] = Label(_("Close"))

	    self.list = []
	    self["list"] = List(self.list)

	    self["actions"] = ActionMap(["WizardActions", "ColorActions"],
	    {
	    "ok": self.selectInte,
	    "back": self.close,
	    "red": self.selectInte,
	    "yellow": self.close
	    })

	    self.list = [ ]
	    self.adapters = [(iNetwork.getFriendlyAdapterName(x),x) for x in iNetwork.getAdapterList()]
	    for x in self.adapters:
	      res = (x[0], x[1])
	      self.list.append(res)

	    self["list"].list = self.list

	def selectInte(self):
	    mysel = self["list"].getCurrent()
	    if mysel:
		inter = mysel[1]
		self.session.open(NetworkBrowser, inter, "/usr/lib/enigma2/python/Plugins/SystemPlugins/NetworkBrowser")
		