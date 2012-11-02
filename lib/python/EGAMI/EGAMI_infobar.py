# -*- coding: utf-8 -*-
from Components.ActionMap import ActionMap, HelpableActionMap, NumberActionMap
from Components.BlinkingPixmap import BlinkingPixmapConditional
from Components.Label import Label
from Components.Pixmap import Pixmap, PixmapConditional
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Sources.Clock import Clock
from Components.Sources.CurrentService import CurrentService
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.PluginComponent import plugins 
from Components.config import *
from Components.PluginList import * 
from Components.Sources.List import List 
from Plugins.Plugin import PluginDescriptor 
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.InfoBarGenerics import InfoBarSubserviceSelection, SimpleServicelist, InfoBarAudioSelection
from Screens.Menu import MainMenu, mdom
from Screens.HelpMenu import HelpableScreen
from Screens.EpgSelection import EPGSelection
from Screens.EventView import EventViewEPGSelect, EventViewSimple
from Screens.ChannelSelection import ChannelSelection, BouquetSelector
from ServiceReference import ServiceReference
from time import strftime, localtime, time
from Tools import Notifications
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, defaultPaths
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.BoundFunction import boundFunction
import os
import sys
import traceback
import StringIO
import xml.dom.minidom
import md5
import re, string
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceCenter, eServiceReference, eListboxPythonMultiContent, eListbox, gFont, eDVBServicePMTHandler, eSize, ePoint, eEPGCache

from EGAMI.EGAMI_infobar_setup import *
from EGAMI.EGAMI_skins import EGPermanentClock_Skin, EGGreenPanel_Skin, EGExtrasMenu_Skin
from EGAMI.EGAMI_tools import *
from Tools.HardwareInfo import HardwareInfo

class EGInfoBarEPG:
	""" EPG - Opens an EPG list when the showEPGList action fires """
	def __init__(self):
		self.__event_tracker = ServiceEventTracker(screen=self, eventmap=
			{
				iPlayableService.evUpdatedEventInfo: self.__evEventInfoChanged,
			})

		self.is_now_next = False
		self.dlg_stack = [ ]
		self.bouquetSel = None
		self.eventView = None


		self.hw_type = HardwareInfo().get_device_name()
		if self.hw_type == 'dm8000':
			self["EPGActions"] = HelpableActionMap(self, "EGInfobarEPGActions",
			{
				"showEventInfo": (self.openEventView, _("show EPG...")),
				"showEventInfoPlugin": (self.showEventInfoPlugins, _("show single service EPG...")),
				"showInfobarOrEpgWhenInfobarAlreadyVisible": self.showEventInfoWhenNotVisible,
				"showSingleServiceEPG": (self.openSingleServiceEPG, _("show single service EPG...")),
			})
		else:
			self["EPGActions"] = HelpableActionMap(self, "InfobarEPGActions",
			{
				"showEventInfo": (self.openEventView, _("show EPG...")),
				"showEventInfoPlugin": (self.showEventInfoPlugins, _("show single service EPG...")),
				"showInfobarOrEpgWhenInfobarAlreadyVisible": self.showEventInfoWhenNotVisible,
				"showSingleServiceEPG": (self.openSingleServiceEPG, _("show single service EPG...")),

			})

	
	def showEventInfoWhenNotVisible(self):
		if self.shown:
			self.openEventView()
		else:
			self.toggleShow()
			return 1

	def zapToService(self, service):
		if not service is None:
			if self.servicelist.getRoot() != self.epg_bouquet: #already in correct bouquet?
				self.servicelist.clearPath()
				if self.servicelist.bouquet_root != self.epg_bouquet:
					self.servicelist.enterPath(self.servicelist.bouquet_root)
				self.servicelist.enterPath(self.epg_bouquet)
			self.servicelist.setCurrentSelection(service) #select the service in servicelist
			self.servicelist.zap()

	def getBouquetServices(self, bouquet):
		services = [ ]
		servicelist = eServiceCenter.getInstance().list(bouquet)
		if not servicelist is None:
			while True:
				service = servicelist.getNext()
				if not service.valid(): #check if end of list
					break
				if service.flags & (eServiceReference.isDirectory | eServiceReference.isMarker): #ignore non playable services
					continue
				services.append(ServiceReference(service))
		return services

	def openBouquetEPG(self, bouquet, withCallback=True):
		services = self.getBouquetServices(bouquet)
		if services:
			self.epg_bouquet = bouquet
			if withCallback:
				self.dlg_stack.append(self.session.openWithCallback(self.closed, EPGSelection, services, self.zapToService, None, self.changeBouquetCB))
			else:
				self.session.open(EPGSelection, services, self.zapToService, None, self.changeBouquetCB)

	def changeBouquetCB(self, direction, epg):
		if self.bouquetSel:
			if direction > 0:
				self.bouquetSel.down()
			else:
				self.bouquetSel.up()
			bouquet = self.bouquetSel.getCurrent()
			services = self.getBouquetServices(bouquet)
			if services:
				self.epg_bouquet = bouquet
				epg.setServices(services)

	def closed(self, ret=False):
		closedScreen = self.dlg_stack.pop()
		if self.bouquetSel and closedScreen == self.bouquetSel:
			self.bouquetSel = None
		elif self.eventView and closedScreen == self.eventView:
			self.eventView = None
		if ret:
			dlgs=len(self.dlg_stack)
			if dlgs > 0:
				self.dlg_stack[dlgs-1].close(dlgs > 1)

	def openMultiServiceEPG(self, withCallback=True):
		bouquets = self.servicelist.getBouquetList()
		if bouquets is None:
			cnt = 0
		else:
			cnt = len(bouquets)
		if cnt > 1: # show bouquet list
			if withCallback:
				self.bouquetSel = self.session.openWithCallback(self.closed, BouquetSelector, bouquets, self.openBouquetEPG, enableWrapAround=True)
				self.dlg_stack.append(self.bouquetSel)
			else:
				self.bouquetSel = self.session.open(BouquetSelector, bouquets, self.openBouquetEPG, enableWrapAround=True)
		elif cnt == 1:
			self.openBouquetEPG(bouquets[0][1], withCallback)

	def changeServiceCB(self, direction, epg):
		if self.serviceSel:
			if direction > 0:
				self.serviceSel.nextService()
			else:
				self.serviceSel.prevService()
			epg.setService(self.serviceSel.currentService())

	def SingleServiceEPGClosed(self, ret=False):
		self.serviceSel = None

	def openSingleServiceEPG(self):
		ref=self.session.nav.getCurrentlyPlayingServiceReference()
		if ref:
			if self.servicelist.getMutableList() is not None: # bouquet in channellist
				current_path = self.servicelist.getRoot()
				services = self.getBouquetServices(current_path)
				self.serviceSel = SimpleServicelist(services)
				if self.serviceSel.selectService(ref):
					self.session.openWithCallback(self.SingleServiceEPGClosed, EPGSelection, ref, serviceChangeCB = self.changeServiceCB)
				else:
					self.session.openWithCallback(self.SingleServiceEPGClosed, EPGSelection, ref)
			else:
				self.session.open(EPGSelection, ref)

	def showEventInfoPlugins(self):
		#for plugin in plugins.getPlugins([PluginDescriptor.WHERE_PLUGINMENU ,PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_EVENTINFO]):
		 #   if plugin.name == _("Cool Info Guide"):
		  #    self.runPlugin(plugin)
		   #   break
		    #else:   
		      list = [(p.name, boundFunction(self.runPlugin, p)) for p in plugins.getPlugins(where = PluginDescriptor.WHERE_EVENTINFO)]

		      if list:
			      list.append((_("show single service EPG..."), self.openSingleServiceEPG))
			      self.session.openWithCallback(self.EventInfoPluginChosen, ChoiceBox, title=_("Please choose an extension..."), list = list, skin_name = "EPGExtensionsList")
		      else:
			      self.openSingleServiceEPG()

	def runPlugin(self, plugin):
		plugin(session = self.session, servicelist = self.servicelist)
		
	def EventInfoPluginChosen(self, answer):
		if answer is not None:
			answer[1]()

	def openSimilarList(self, eventid, refstr):
		self.session.open(EPGSelection, refstr, None, eventid)

	def getNowNext(self):
		epglist = [ ]
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		ptr = info and info.getEvent(0)
		if ptr:
			epglist.append(ptr)
		ptr = info and info.getEvent(1)
		if ptr:
			epglist.append(ptr)
		self.epglist = epglist

	def __evEventInfoChanged(self):
		if self.is_now_next and len(self.dlg_stack) == 1:
			self.getNowNext()
			assert self.eventView
			if self.epglist:
				self.eventView.setEvent(self.epglist[0])

	def openEventView(self):
		ref = self.session.nav.getCurrentlyPlayingServiceReference()
		self.getNowNext()
		epglist = self.epglist
		if not epglist:
			self.is_now_next = False
			epg = eEPGCache.getInstance()
			ptr = ref and ref.valid() and epg.lookupEventTime(ref, -1)
			if ptr:
				epglist.append(ptr)
				ptr = epg.lookupEventTime(ref, ptr.getBeginTime(), +1)
				if ptr:
					epglist.append(ptr)
		else:
			self.is_now_next = True
		if epglist:
			self.eventView = self.session.openWithCallback(self.closed, EventViewEPGSelect, self.epglist[0], ServiceReference(ref), self.eventViewCallback, self.openSingleServiceEPG, self.openMultiServiceEPG, self.openSimilarList)
			self.dlg_stack.append(self.eventView)
		else:
			print "no epg for the service avail.. so we show multiepg instead of eventinfo"
			self.openMultiServiceEPG(False)

	def eventViewCallback(self, setEvent, setService, val): #used for now/next displaying
		epglist = self.epglist
		if len(epglist) > 1:
			tmp = epglist[0]
			epglist[0]=epglist[1]
			epglist[1]=tmp
			setEvent(epglist[0])



from Screens.PictureInPicture import PictureInPicture
from Screens.PiPSetup import PiPSetup

class EGInfoBarAudioSelection(InfoBarAudioSelection):
	def __init__(self):
		self["AudioSelectionAction"] = HelpableActionMap(self, "InfobarAudioSelectionActions",
			{
				"audioSelection": (self.audioSelection, _("Audio Options...")),
				"showSubtitles": (self.openSubtitles, _("show subtitles...")),
				"showSleepTimer": (self.openSleepTimer, _("show sleepTimer...")),
			})
			
	def audioSelection(self):
		from Screens.AudioSelection import AudioSelection
		self.session.openWithCallback(self.audioSelected, AudioSelection, infobar=self)
		
	def audioSelected(self, ret=None):
		print "[infobar::audioSelected]", ret

	def openSleepTimer(self):
	      from Screens.SleepTimerEdit import SleepTimerEdit
	      self.session.open(SleepTimerEdit)
	      
	def openSubtitles(self):
	      from Screens.AudioSelection import SubtitleSelection
	      self.session.openWithCallback(self.audioSelected, SubtitleSelection, infobar=self)

		 
#		<!-- Emu Name -->
#		<widget name ="EmuName" position="757,671" size="442,22" halign="center" font="Regular;20" transparent="1" backgroundColor="#102e59" foregroundColor="#1A58A6" zPosition="3"/>
#			
#		<!-- Prv Ca ID -->
#		<widget name ="ExpertCaidPrvid" position="80,657" size="670,18" halign="center" font="Regular;15" transparent="1" backgroundColor="#102e59" foregroundColor="#cccccc" />
#		
#		<!-- NetCardInfo info -->		
#		<widget name ="ExpertEmuInfo" position="80,675" size="670,18" halign="center" font="Regular;15" transparent="1" backgroundColor="#102e59" foregroundColor="#cccccc" />
#		
#		<!-- Decode Source -->
#		<widget name ="DecodeCard" position="757,644" size="36,18" halign="center" font="Regular;16" backgroundColor="#31000000" foregroundColor="#DF9629" valign="center" zPosition="3" />
#		<widget name ="DecodeEmu" position="757,644" size="36,18" halign="center" font="Regular;16" backgroundColor="#31000000" foregroundColor="#1A58A6" valign="center" zPosition="3"/>
#		<widget name ="DecodeNet" position="757,644" size="36,18" halign="center" font="Regular;16" backgroundColor="#31000000" foregroundColor="#C21A1A" valign="center" zPosition="3"/>
#		<widget name ="DecodeFta" position="757,644" size="36,18" halign="center" font="Regular;16" backgroundColor="#31000000" foregroundColor="#DF9629" valign="center" zPosition="3"/>
#		<!--  HD LOGO and SD LOGO -->
#		<widget source="session.CurrentService" render="Pixmap" pixmap="iRUDREAM/icons/i_sd.png" position="1042,556" size="48,48" zPosition="1" alphatest="on">
#			<convert type="ServiceInfo">VideoWidth</convert>
#			<convert type="ValueRange">0,720</convert>
#			<convert type="ConditionalShowHide" />
#		</widget>
#		<widget source="session.CurrentService" render="Pixmap" pixmap="iRUDREAM/icons/i_hd.png" position="1042,556" size="48,48" zPosition="1" alphatest="on">
#			<convert type="ServiceInfo">VideoWidth</convert>
#			<convert type="ValueRange">721,1980</convert>
#			<convert type="ConditionalShowHide" />
#		</widget>
		
class EGInfoBar:
    	def __init__(self):
		self.systemCod = [
				"beta_no", "beta_emm", "beta_ecm",
				"seca_no", "seca_emm", "seca_ecm",
				"irdeto_no", "irdeto_emm", "irdeto_ecm",
				"cw_no", "cw_emm", "cw_ecm",
				"nagra_no", "nagra_emm", "nagra_ecm", 
				"nds_no", "nds_emm", "nds_ecm",
				"via_no", "via_emm", "via_ecm", "conax_no",
				"conax_emm", "conax_ecm",
				"DecodeFta" , "DecodeCard", "DecodeEmu", "DecodeNet"
				]
		
		self.systemCaids = {
				"06" : "irdeto", "01" : "seca", "18" : "nagra",
				"05" : "via", "0B" : "conax", "17" : "beta",
				"0D" : "cw", "4A" : "irdeto", "09" : "nds"
				}
		
		for x in self.systemCod:
			self[x] = Label()
		
		self["ExpertEmuInfo"] = Label()
		self["ExpertCaidPrvid"] = Label()
		self["EmuName"] = Label()
		
		self.count = 0
		self.ecm_timer = eTimer()
		self.ecm_timer.timeout.get().append(self.updateEmuInfo)
		self.emm_timer = eTimer()
		self.emm_timer.timeout.get().append(self.updateEMMInfo)
		
		self.event_tracker = ServiceEventTracker(screen=self, eventmap=
			{
				iPlayableService.evStart: self.evStart,
				iPlayableService.evTunedIn: self.evTunedIn,
			})

	def evStart(self):
		if self.emm_timer.isActive():
			self.emm_timer.stop()
		if self.ecm_timer.isActive():
			self.ecm_timer.stop()
		self.count = 0
		self.displayClean()	
		
	def evTunedIn(self):
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		#if self.instance.isVisible():
		if info is not None:
				self.emm_timer.start(1500)
				self.ecm_timer.start(2500)
	
	def updateEMMInfo(self):
		self.emm_timer.stop()
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		if self.instance.isVisible():
			if info is not None:
				self.showEMM(info.getInfoObject(iServiceInformation.sCAIDs))
	
	def updateEmuInfo(self):
		service = self.session.nav.getCurrentService()
		info = service and service.info()
		if info is not None:
			if info.getInfo(iServiceInformation.sIsCrypted):
				if self.count < 4:
					self.count = self.count + 1
				else:
					self.ecm_timer.changeInterval(2000)
				info = parse_ecm()
				if info != 0:
					caid = info[0]
					pid = info[1]
					provid = info[2]
					ecmtime = info[3]
					source = info[4]
					addr = info[5]
					port = info[6]
					hops = info[7]
					
					if(config.infobar.prvcaid.value == True):
						self["ExpertCaidPrvid"].setText((("CaID: " + norm_hex(caid)) + " PrvID: " + norm_hex(provid) + " Pid: " + pid))
					if(config.infobar.emuname.value == True):
						self["EmuName"].setText(readEmuName())
						
					self["DecodeFta"].hide()
					self["DecodeCard"].hide()
					self["DecodeEmu"].hide()
					self["DecodeNet"].hide()
					if(config.infobar.emusrc.value == True):
						if source == 0:
							self["DecodeFta"].show()
							self["DecodeFta"].setText("FTA")
						elif source == 1:
							self["DecodeEmu"].show()
							self["DecodeEmu"].setText("EMU")
							if(config.infobar.netcard.value == True):
								self["ExpertEmuInfo"].setText("Source: Internal EcmTime: " + str(ecmtime) + "ms Hops:" + str(hops))
						elif source == 2: ## CCCAM
							if addr !='':
								if (addr.find('127.0.0.1') or addr.find('localhost')) >= 0:
									self["DecodeCard"].setText("CARD")
									self["DecodeCard"].show()
									if(config.infobar.netcard.value == True):
										self["ExpertEmuInfo"].setText("Source: Internal EcmTime: " + str(ecmtime) + "ms Hops:" + str(hops))
								else:		
									self["DecodeNet"].show()
									self["DecodeNet"].setText("NET")
									if(config.infobar.netcard.value == True):
										self["ExpertEmuInfo"].setText((("Source: " + addr) + " " + port) + " EcmTime: " + str(ecmtime) + "ms Hops:" + str(hops))
							else:
								self["DecodeNet"].show()
								self["DecodeNet"].setText("NET")
								if(config.infobar.netcard.value == True):
									self["ExpertEmuInfo"].setText((("Source: " + addr) + " " + port) + " EcmTime: " + str(ecmtime) + "ms Hops:" + str(hops))
						elif source == 4:
							self["DecodeCard"].show()
							self["DecodeCard"].setText("CARD")
							if(config.infobar.netcard.value == True):
								self["ExpertEmuInfo"].setText("Source: /dev/sci0 EcmTime: " + str(ecmtime) + "ms Hops:" + str(hops))
						elif source == 5:
							self["DecodeCard"].show()
							self["DecodeCard"].setText("CARD")
							if(config.infobar.netcard.value == True):
								self["ExpertEmuInfo"].setText("Source: /dev/sci1 EcmTime: " + str(ecmtime) + "ms Hops:" + str(hops))
						elif source == 6: #GBox MgCamd
							if addr !='':
								if (addr.find('127.0.0.1') or addr.find('localhost')) >= 0:
									self["DecodeCard"].setText("CARD")
									self["DecodeCard"].show()
									if(config.infobar.netcard.value == True):
										self["ExpertEmuInfo"].setText("Source: Internal EcmTime: " + str(ecmtime))
								else:		
									self["DecodeNet"].show()
									self["DecodeNet"].setText("NET")
									if(config.infobar.netcard.value == True):
										self["ExpertEmuInfo"].setText((("Source: " + addr) + " " + port) + " EcmTime: " + str(ecmtime))
							else:
								self["DecodeNet"].show()
								self["DecodeNet"].setText("NET")
								if(config.infobar.netcard.value == True):
									self["ExpertEmuInfo"].setText((("Source: " + addr) + " " + port) + " EcmTime: " + str(ecmtime))
						elif source == 7: # GBox
							self["DecodeCard"].show()
							self["DecodeCard"].setText("CARD")
							if(config.infobar.netcard.value == True):
								self["ExpertEmuInfo"].setText("Source: /dev/sci0 EcmTime: " + str(ecmtime))
						elif source == 8: #GBox
							self["DecodeCard"].show()
							self["DecodeCard"].setText("CARD")
							if(config.infobar.netcard.value == True):
								self["ExpertEmuInfo"].setText("Source: /dev/sci1 EcmTime: " + str(ecmtime))
					else:
						self["DecodeFta"].hide()
						self["DecodeCard"].hide()
						self["DecodeEmu"].hide()
						self["DecodeNet"].hide()
						
					if caid !='':
						self.showECM(caid)
				
				if(config.infobar.cavi.value == False):
						for x in self.systemCod:
							self[x].hide()
							if x.find('_no') >= 0:
								self[x].hide()
							if x.find('_ecm') >= 0:
								self[x].hide()
							if x.find('_emm') >= 0:
								self[x].hide()

			else:
				self["ExpertEmuInfo"].setText("")
				self["ExpertCaidPrvid"].setText("")
				self["DecodeFta"].setText("FTA")
				self["DecodeFta"].show()
								
	def showECM(self, caid):
		caid = caid.lower()
		if caid.__contains__("x"):
			idx = caid.index("x")
			caid = caid[idx+1:]
			if len(caid) == 3:
				caid = "0%s" % caid
			caid = caid[:2]
			caid = caid.upper()
			if self.systemCaids.has_key(caid):
				system = self.systemCaids.get(caid)
				self[system + "_emm"].hide()
				self[system + "_ecm"].show()
	
	def int2hex(self, int):
		return "%x" % int
	
	def showEMM(self, caids):
		if caids:
			if len(caids) > 0:
				for caid in caids:
					caid = self.int2hex(caid)
					if len(caid) == 3:
						caid = "0%s" % caid
					caid = caid[:2]
					caid = caid.upper()
					if self.systemCaids.has_key(caid):
						system = self.systemCaids.get(caid)
						self[system + "_no"].hide()
						self[system + "_emm"].show()
	
	def displayClean(self):
		self["EmuName"].setText("")
		self["ExpertEmuInfo"].setText("")
		self["ExpertCaidPrvid"].setText("")
		for x in self.systemCod:
			self[x].hide()
			if x.find('_no') >= 0:
				self[x].show()

class EGZapInfoBar(InfoBarBase,Screen):
    def __init__(self, session):
        Screen.__init__(self, session)

class EGInfoBarShowHide:

    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3

    def __init__(self):
	self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.toggleShow,
         "hide": self.realHide}, 1)
        
	self._EGInfoBarShowHide__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self._EGInfoBarShowHide__serviceStarted,
         iPlayableService.evUpdatedEventInfo: self._EGInfoBarShowHide__eventInfoChanged})
        
	self._EGInfoBarShowHide__state = self.STATE_SHOWN
        self._EGInfoBarShowHide__locked = 0
        
	self.onExecBegin.append (self.doShow)
        
	self.hideTimer = eTimer()
        self.hideTimer.timeout.get().append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        
	self.onShow.append(self._EGInfoBarShowHide__onShow)
        self.onHide.append(self._EGInfoBarShowHide__onHide)
        
	self.current_begin_time = 0
        self.useZap = False
        
	try:
            self.zapDialog = self.session.instantiateDialog(EGZapInfoBar)
        except:
            self.zapDialog = None
	
	self.permanentClockDialod = self.session.instantiateDialog(EGPermanentClock)


    def __eventInfoChanged(self):
        if self.execing:
            service = self.session.nav.getCurrentService()
            old_begin_time = self.current_begin_time
            info = (service and service.info())
            ptr = (info and info.getEvent(0))
            self.current_begin_time = ((ptr and ptr.getBeginTime()) or 0)
            if config.usage.show_infobar_on_event_change.value:
                if (old_begin_time and (old_begin_time != self.current_begin_time)):
                    self.doShow()



    def __serviceStarted(self):
        if self.execing:
            self.current_begin_time = 0
            if config.usage.show_infobar_on_zap.value:
                self.doShow()



    def __onShow(self):
        self._EGInfoBarShowHide__state = self.STATE_SHOWN
        self.startHideTimer()



    def __onHide(self):
        self._EGInfoBarShowHide__state = self.STATE_HIDDEN
        if (self.zapDialog is not None):
            self.zapDialog.hide()

	
    def startHideTimer(self):
        if ((self._EGInfoBarShowHide__state == self.STATE_SHOWN) and (not self._EGInfoBarShowHide__locked)):
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start((idx * 1000), True)



    def doShow(self):
        self.realShow()
        self.startHideTimer()



    def hide(self):
        if (self.zapDialog is not None):
            self.zapDialog.hide()
        Screen.hide(self)



    def realHide(self):
        self.hide()
        self.useZap = True
        self._EGInfoBarShowHide__state = self.STATE_HIDDEN



    def realShow(self):
        if (config.infobar.liteskin.value == True):
            if (self.zapDialog is not None):
                if self.useZap:
		    #print "--------------------------------------------realShow: useZap IF"
		    self.hide()
		    #self.movePositionInfobarLite()
		    self.zapDialog.show()
                else:
		    #print "--------------------------------------------realShow: useZap ELSE"
                    self.show()
                    self.zapDialog.hide()
                    #self.movePositionInfobar()
            else:
		#print "-------------------------------------------------realShow: useZap ELSE 2"
                self.show()
                #self.movePositionInfobarLite()
        else:
            #print "------------------------------------------------------realShow: LITE == FALSE"
            self.show()
            #self.movePositionInfobar()
        self._EGInfoBarShowHide__state = self.STATE_SHOWN



    def doTimerHide(self):
        self.hideTimer.stop()
        if (self._EGInfoBarShowHide__state == self.STATE_SHOWN):
            self.realHide()



    def toggleShow(self):
        if ((config.infobar.liteskin.value == True) and (self.zapDialog is not None)):
            if (self._EGInfoBarShowHide__state == self.STATE_SHOWN):
                if self.useZap:
                    self.useZap = False
                    self.realShow ()
                    self.startHideTimer()
                else:
                    self.realHide()
                    self.hideTimer.stop()
            elif (self._EGInfoBarShowHide__state == self.STATE_HIDDEN ):
                self.realShow()
                self.startHideTimer()
        elif (self._EGInfoBarShowHide__state == self.STATE_SHOWN):
            self.realHide()
            self.hideTimer.stop()
        elif (self._EGInfoBarShowHide__state == self.STATE_HIDDEN):
            self.realShow()
            self.startHideTimer()



    def lockShow(self):
        self._EGInfoBarShowHide__locked = (self._EGInfoBarShowHide__locked + 1)
        if self.execing:
            self.doShow()
            self.hideTimer.stop()



    def unlockShow(self):
        self._EGInfoBarShowHide__locked = (self._EGInfoBarShowHide__locked - 1)
        if self.execing :
            self.startHideTimer()

class EGInfoBarServiceErrorPopupSupport:

    def __init__(self):
        self._EGInfoBarServiceErrorPopupSupport__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evTuneFailed: self._EGInfoBarServiceErrorPopupSupport__tuneFailed,
         iPlayableService.evStart: self._EGInfoBarServiceErrorPopupSupport__serviceStarted})
        self._EGInfoBarServiceErrorPopupSupport__serviceStarted()



    def __serviceStarted(self):
        self.last_error = None
        Notifications.RemovePopup(id="ZapError")



    def __tuneFailed(self):
        service = self.session.nav.getCurrentService()
        info = (service and service.info ())
        error = (info and info.getInfo(iServiceInformation.sDVBState))
        if (error == self.last_error):
            error = None
        else:
            self.last_error = error
        errors = { eDVBServicePMTHandler.eventNoResources: _("No free tuner!"),
         eDVBServicePMTHandler.eventTuneFailed: _("Tune failed!"),
         eDVBServicePMTHandler.eventNoPAT: _("No data on transponder!\n(Timeout reading PAT)"),
         eDVBServicePMTHandler.eventNoPATEntry: _("Service not found!\n(SID not found in PAT)"),
         eDVBServicePMTHandler.eventNoPMT: _("Service invalid!\n(Timeout reading PMT)"),
         eDVBServicePMTHandler.eventNewProgramInfo: None,
         eDVBServicePMTHandler.eventTuned: None,
         eDVBServicePMTHandler.eventSOF: None,
         eDVBServicePMTHandler.eventEOF: None}
        if (error is not None):
            if ((error == eDVBServicePMTHandler.eventNoResources) and (config.EGDecoding.messageNoResources.value == False)):
                return
            elif ((error == eDVBServicePMTHandler.eventTuneFailed ) and (config.EGDecoding.messageTuneFailed.value == False)):
                return
            elif ((error == eDVBServicePMTHandler.eventNoPAT) and (config.EGDecoding.messageNoPAT.value == False)):
                return
            elif ((error == eDVBServicePMTHandler.eventNoPATEntry) and (config.EGDecoding.messageNoPATEntry.value == False)):
                return
            elif ((error == eDVBServicePMTHandler.eventNoPMT) and (config.EGDecoding.messageNoPMT.value == False)):
                return
        error = errors.get(error)
        if (error is not None):
            Notifications.AddPopup (text=error, type=MessageBox.TYPE_ERROR, timeout=5, id="ZapError")
        else:
            Notifications.RemovePopup(id="ZapError")



class EGPermanentClock(Screen):
    def __init__(self, session):

	self.skin = EGPermanentClock_Skin
	Screen.__init__(self, session)
        self.isShown = False
        self.checkTimer = eTimer()
        self.checkTimer.timeout.get().append(self.checkShowHide )
        self.checkTimer.start(1000, False)

    def movePosition(self):
	self.instance.move(ePoint(config.plugins.positioner.permanentClockPositionX.value, config.plugins.positioner.permanentClockPositionY.value))

    def checkShowHide(self):
        if (config.infobar.permanentClock.value == True):
		self.movePosition()
        	self.show()
        	self.isShown = True
        elif (self.isShown == True):
                self.hide()
                self.isShown = False
        else:
	      self.hide()
