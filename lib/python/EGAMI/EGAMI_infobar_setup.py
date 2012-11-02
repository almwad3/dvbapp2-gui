# -*- coding: utf-8 -*-
from Components.ActionMap import *
from Components.config import *
from Components.ConfigList import *
from Components.UsageConfig import *
from Components.Label import Label
from Components.Sources.Boolean import *
from Components.UsageConfig import *

from Components.Pixmap import Pixmap

from Screens.Screen import Screen

from enigma import eSize, ePoint

from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_SKIN, SCOPE_CURRENT_SKIN

from skin import readSkin, applyAllAttributes
from os import path, walk

from EGAMI.EGAMI_skins import EGDecodingSetup_Skin, EGInfoBarSetup_Skin
from EGAMI.EGAMI_tools import wyszukaj_re
from Plugins.Extensions.EGAMIPermanentClock.plugin import *

config.EGDecoding = ConfigSubsection()
config.EGDecoding.messageNoResources = ConfigYesNo(default=True)
config.EGDecoding.messageTuneFailed = ConfigYesNo(default=True)
config.EGDecoding.messageNoPAT = ConfigYesNo(default=True)
config.EGDecoding.messageNoPATEntry = ConfigYesNo(default=True)
config.EGDecoding.messageNoPMT = ConfigYesNo(default=True)
config.EGDecoding.dsemudmessages = ConfigYesNo(default=True)
config.EGDecoding.messageYesPmt = ConfigYesNo(default=False)
config.EGDecoding.show_ci_messages = ConfigYesNo(default=False)


class EGDecodingSetup(ConfigListScreen, Screen):
    __module__ = __name__
    def __init__(self, session, args = 0):
	self.skin = EGDecodingSetup_Skin
	Screen.__init__(self, session)
		
        list = []
	#list.append(getConfigListEntry(__('Enable pmtX.tmp -> X-1..9'), config.EGDecoding.messageYesPmt))
	list.append(getConfigListEntry(_('Show Egami informations?'), config.EGDecoding.dsemudmessages))
	list.append(getConfigListEntry(_('Show No free tuner info?'), config.EGDecoding.messageNoResources))
	list.append(getConfigListEntry(_('Show Tune failed info?'), config.EGDecoding.messageTuneFailed))
	list.append(getConfigListEntry(_('Show No data on transponder info?'), config.EGDecoding.messageNoPAT))
	list.append(getConfigListEntry(_('Show Service not found info?'), config.EGDecoding.messageNoPATEntry))
	list.append(getConfigListEntry(_('Show Service invalid info?'), config.EGDecoding.messageNoPMT))
	list.append(getConfigListEntry(_('Show CI Messages?'), config.EGDecoding.show_ci_messages))

        self["key_red"] = Label(_("Save"))
        self["key_green"] = Label(_("Exit"))
        	
        ConfigListScreen.__init__(self, list)
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions'], {'red': self.saveAndExit, 'green' : self.dontSaveAndExit,
         'cancel': self.dontSaveAndExit}, -1)

    def saveAndExit(self):
	if config.EGDecoding.dsemudmessages.value is not False:
		os.system("rm -rf /var/etc/.no_osd_messages")
	elif config.EGDecoding.dsemudmessages.value is not True:
		os.system("touch /var/etc/.no_osd_messages")
		
	if config.EGDecoding.messageYesPmt.value is not False:
		os.system("rm -rf /var/etc/.no_pmt_tmp")
	elif config.EGDecoding.messageYesPmt.value is not True:
		os.system("touch /var/etc/.no_pmt_tmp")
		
        for x in self['config'].list:
            x[1].save()

	config.EGDecoding.save()
	
        self.close()

    def dontSaveAndExit(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()
        
config.infobar = ConfigSubsection()
config.infobar.piconEnabled = ConfigYesNo(default=True)
config.infobar.piconType = ConfigSelection(choices={ 'Name': _('Name'), 'Reference': _('Reference')}, default='Reference')
config.infobar.piconDirectory = ConfigSelection(choices={ 'flash': _('/etc/picon/'),
 'cf': _('/media/cf/'),
 'usb': _('/media/usb/'),
 'hdd': _('/media/hdd/')}, default='hdd')
config.infobar.piconDirectoryName = ConfigText(default = "picon", fixed_size = False)
config.infobar.permanentClockPosition = ConfigSelection(choices=["<>"], default="<>")

class EGInfoBarSetup(Screen, ConfigListScreen):
	def __init__(self, session):
	    
	    self.skin = EGInfoBarSetup_Skin
	    
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

	    self.list.append(getConfigListEntry(_("Infobar timeout"), config.usage.infobar_timeout))
	    self.list.append(getConfigListEntry(_("Show permanental clock"), config.plugins.PermanentClock.enabled))
	    self.list.append(getConfigListEntry(_('    Set clock position'), config.infobar.permanentClockPosition))
	    self.list.append(getConfigListEntry(_("Show second infobar"), config.usage.show_second_infobar))
	    self.list.append(getConfigListEntry(_("Show event-progress in channel selection"), config.usage.show_event_progress_in_servicelist))
	    self.list.append(getConfigListEntry(_("Show channel numbers in channel selection"), config.usage.show_channel_numbers_in_servicelist))
	    self.list.append(getConfigListEntry(_("Show infobar on channel change"), config.usage.show_infobar_on_zap))
	    self.list.append(getConfigListEntry(_("Show infobar on skip forward/backward"), config.usage.show_infobar_on_skip))
	    self.list.append(getConfigListEntry(_("Show infobar on event change"), config.usage.show_infobar_on_event_change))
	    self.list.append(getConfigListEntry(_("Hide zap errors"), config.usage.hide_zap_errors))
	    self.list.append(getConfigListEntry(_("Hide CI messages"), config.usage.hide_ci_messages))
	    self.list.append(getConfigListEntry(_("Show crypto info in infobar"), config.usage.show_cryptoinfo))
	    self.list.append(getConfigListEntry(_("Swap SNR in db with SNR in percentage on OSD"), config.usage.swap_snr_on_osd))
	    self.list.append(getConfigListEntry(_("Show EIT now/next in infobar"), config.usage.show_eit_nownext))
	    self.list.append(getConfigListEntry(_('Use Picon:'), config.infobar.piconEnabled))
	    #if config.infobar.piconEnabled.value == True:
	    self.list.append(getConfigListEntry(_('    Picon Type:'), config.infobar.piconType))
	    self.list.append(getConfigListEntry(_('    Directory:'), config.infobar.piconDirectory))
	    self.list.append(getConfigListEntry(_('    Directory Name:'), config.infobar.piconDirectoryName))

	    self["config"].list = self.list
	    self["config"].l.setList(self.list)

	def keyLeft(self):
	    ConfigListScreen.keyLeft(self)
	    self.handleKeysLeftAndRight()

	def keyRight(self):
	    ConfigListScreen.keyRight(self)
	    self.handleKeysLeftAndRight()

	def handleKeysLeftAndRight(self):
	    sel = self["config"].getCurrent()[1]
	    if sel == config.infobar.permanentClockPosition:
			pClock.dialog.hide()
			self.session.openWithCallback(self.positionerCallback, PermanentClockPositioner)

	def positionerCallback(self, callback=None):
		pClock.showHide()
		
	def keySave(self):
	    for x in self["config"].list:
		x[1].save()
	
	    if pClock.dialog is None:
		    pClock.gotSession(self.session)
	    if config.plugins.PermanentClock.enabled.value == True:
	      pClock.showHide()
	    if config.plugins.PermanentClock.enabled.value == False:
	      pClock.showHide()
	      
	    self.close()

	def keyCancel(self):
	    for x in self["config"].list:
		x[1].cancel()
	    self.close()


config.plugins.positioner = ConfigSubsection()
config.plugins.positioner.permanentClockPositionX = ConfigInteger(default=50)
config.plugins.positioner.permanentClockPositionY = ConfigInteger(default=50)

class EGPermanentClock_Positioner(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session

		self.skin = """
		<screen position="610,30" size="100,34" flags="wfNoBorder" backgroundColor="#55000000">
			<widget name="label" position="0,0" size="100,34" font="LCD;24" foregroundColor="#d0d0d0" valign="center" halign="center" transparent="1" />
		</screen>"""

		self["actions"] = ActionMap(["EGActions"],
		{
			"left": self.left,
			"up": self.up,
			"right": self.right,
			"down": self.down,
			"ok": self.ok,
			"exit": self.cancel
		}, -1)
		self['label'] = Label(_('CLOCK'))
		self.onLayoutFinish.append(self.movePosition)
		 
	def movePosition(self):
		config.infobar.permanentClock.value = False
		self.instance.move(ePoint(config.plugins.positioner.permanentClockPositionX.value, config.plugins.positioner.permanentClockPositionY.value))
		self['label'].setText(_("CLOCK"))

	def left(self):
		config.plugins.positioner.permanentClockPositionX.value = (config.plugins.positioner.permanentClockPositionX.value - 3)
		self.movePosition()

	def up(self):
		config.plugins.positioner.permanentClockPositionY.value = (config.plugins.positioner.permanentClockPositionY.value - 3)
		self.movePosition()

	def right(self):
		config.plugins.positioner.permanentClockPositionX.value = (config.plugins.positioner.permanentClockPositionX.value + 3)
		self.movePosition()

	def down(self):
		config.plugins.positioner.permanentClockPositionY.value = (config.plugins.positioner.permanentClockPositionY.value + 3)
		self.movePosition()

	def ok(self):
		config.infobar.permanentClock.value = True
		config.plugins.positioner.permanentClockPositionX.save()
		config.plugins.positioner.permanentClockPositionY.save()
		self.close()
		
	def cancel(self):
		config.infobar.permanentClock.value = True
		config.plugins.positioner.permanentClockPositionX.cancel()
		config.plugins.positioner.permanentClockPositionY.cancel()
        	self.close(False)


config.plugins.positioner.InfobarPositionX = ConfigInteger(default=0)
config.plugins.positioner.InfobarPositionY = ConfigInteger(default=4)

class EGInfobar_Positioner(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = "InfoBar"

		self["actions"] = ActionMap(["EGActions"],
		{
			"left": self.left,
			"up": self.up,
			"right": self.right,
			"down": self.down,
			"ok": self.ok,
			"exit": self.cancel
		}, -1)
		self.labels= [
				"beta_no", "beta_emm", "beta_ecm",
				"seca_no", "seca_emm", "seca_ecm",
				"irdeto_no", "irdeto_emm", "irdeto_ecm",
				"cw_no", "cw_emm", "cw_ecm",
				"nagra_no", "nagra_emm", "nagra_ecm", 
				"nds_no", "nds_emm", "nds_ecm",
				"via_no", "via_emm", "via_ecm", "conax_no",
				"conax_emm", "conax_ecm",
				"DecodeFta" , "DecodeCard", "DecodeEmu", "DecodeNet", "EmuName", "ExpertCaidPrvid", "ExpertEmuInfo", "session.CurrentService",
				"Event_Now", "Event_Next", "FrontendInfo", "RecordingPossible", "ShowRecordOnRed", "TimeshiftPossible", "ShowTimeshiftOnYellow",
				"ShowAudioOnYellow", "ExtensionsAvailable"
				]
					
		for x in self.labels:
			self[x] = Boolean(fixed=1)
			
		self.onLayoutFinish.append(self.movePosition)
		 
	def movePosition(self):
		self.instance.move(ePoint(config.plugins.positioner.InfobarPositionX.value, config.plugins.positioner.InfobarPositionY.value))

	def left(self):
		config.plugins.positioner.InfobarPositionX.value = (config.plugins.positioner.InfobarPositionX.value - 3)
		self.movePosition()

	def up(self):
		config.plugins.positioner.InfobarPositionY.value = (config.plugins.positioner.InfobarPositionY.value - 3)
		self.movePosition()

	def right(self):
		config.plugins.positioner.InfobarPositionX.value = (config.plugins.positioner.InfobarPositionX.value + 3)
		self.movePosition()

	def down(self):
		config.plugins.positioner.InfobarPositionY.value = (config.plugins.positioner.InfobarPositionY.value + 3)
		self.movePosition()

	def ok(self):
		config.plugins.positioner.InfobarPositionX.save()
		config.plugins.positioner.InfobarPositionY.save()
		self.close()
		
	def cancel(self):
		config.plugins.positioner.InfobarPositionX.save()
		config.plugins.positioner.InfobarPositionY.save()
        	self.close(False)
		
config.plugins.positioner.InfobarLitePositionX = ConfigInteger(default=0)
config.plugins.positioner.InfobarLitePositionY = ConfigInteger(default=58)

class EGInfobarLite_Positioner(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skinName = "EGZapInfoBar"

		self["actions"] = ActionMap(["EGActions"],
		{
			"left": self.left,
			"up": self.up,
			"right": self.right,
			"down": self.down,
			"ok": self.ok,
			"exit": self.cancel
		}, -1)
		self.labels= [
				"beta_no", "beta_emm", "beta_ecm",
				"seca_no", "seca_emm", "seca_ecm",
				"irdeto_no", "irdeto_emm", "irdeto_ecm",
				"cw_no", "cw_emm", "cw_ecm",
				"nagra_no", "nagra_emm", "nagra_ecm", 
				"nds_no", "nds_emm", "nds_ecm",
				"via_no", "via_emm", "via_ecm", "conax_no",
				"conax_emm", "conax_ecm",
				"DecodeFta" , "DecodeCard", "DecodeEmu", "DecodeNet", "EmuName", "ExpertCaidPrvid", "ExpertEmuInfo", "session.CurrentService",
				"Event_Now", "Event_Next", "FrontendInfo", "RecordingPossible", "ShowRecordOnRed", "TimeshiftPossible", "ShowTimeshiftOnYellow",
				"ShowAudioOnYellow", "ExtensionsAvailable"
				]
					
		for x in self.labels:
			self[x] = Boolean(fixed=1)
		self.onLayoutFinish.append(self.movePosition)
		 
	def movePosition(self):
		self.instance.move(ePoint(config.plugins.positioner.InfobarLitePositionX.value, config.plugins.positioner.InfobarLitePositionY.value))

	def left(self):
		config.plugins.positioner.InfobarLitePositionX.value = (config.plugins.positioner.InfobarLitePositionX.value - 3)
		self.movePosition()

	def up(self):
		config.plugins.positioner.InfobarLitePositionY.value = (config.plugins.positioner.InfobarLitePositionY.value - 3)
		self.movePosition()

	def right(self):
		config.plugins.positioner.InfobarLitePositionX.value = (config.plugins.positioner.InfobarLitePositionX.value + 3)
		self.movePosition()

	def down(self):
		config.plugins.positioner.InfobarLitePositionY.value = (config.plugins.positioner.InfobarLitePositionY.value + 3)
		self.movePosition()

	def ok(self):
		config.plugins.positioner.InfobarLitePositionX.save()
		config.plugins.positioner.InfobarLitePositionY.save()
		self.close()
		
	def cancel(self):
		config.plugins.positioner.InfobarLitePositionX.save()
		config.plugins.positioner.InfobarLitePositionY.save()
        	self.close(False)


class EGInfoBarPositionerSetup(Screen):
        __module__ = __name__

	def __init__(self, session, args = None):
		self.skin = EGInfoBarPositionerSetup_Skin
		
		Screen.__init__(self, session)

		self.previewPath = ""
		self["skin_preview"] = Pixmap()
		self["skin_info"]= Label(_(' '))
		self["skin_info2"]= Label(_('Skin Informations:'))
		
		self["key_red"] = Label(_("Save"))
		self["key_green"] = Label(_("Full Bar"))
		self["key_yellow"] = Label(_("Lite Bar"))
		
		self["actions"] = NumberActionMap(["EGActions"],
		{
			"back": self.close,
			"red": self.close,
			"green": self.fullBar,
			"yellow": self.liteBar,
			"exit": self.cancel,
			"ok": self.cancel
		}, -1)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.loadPreview()


	def liteBar(self):	
		if wyszukaj_re("EGZapInfoBar"):
			self.session.open(EGInfobarLite_Positioner)
		else:
			self.session.open(MessageBox, _("Sorry, this skin doesn't use EGZapInfoBar"), MessageBox.TYPE_INFO, timeout=5)
					
	def fullBar(self):
		if wyszukaj_re("InfoBar"):
			self.session.open(EGInfobar_Positioner)
		else:
			self.session.open(MessageBox, _("Sorry, this skin doesn't use InfoBar"), MessageBox.TYPE_INFO, timeout=5)

	def loadPreview(self):
		infopath = resolveFilename(SCOPE_CURRENT_SKIN) + "skin.info"
		pngpath = resolveFilename(SCOPE_CURRENT_SKIN) + "prev.png"
		
		self.previewPath = pngpath

		self["skin_preview"].instance.setPixmapFromFile(self.previewPath)
		
 		if fileExists(infopath):
			skininfo_file = file(infopath, 'r')
            		skininfo_file_read = skininfo_file.read()
            		skininfo_file.close()	
			self['skin_info'].setText(skininfo_file_read)
		else:
			self['skin_info'].setText("Sorry, no skin info")

	def cancel(self):
        	self.close(False)
