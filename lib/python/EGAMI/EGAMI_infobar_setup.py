# -*- coding: utf-8 -*-
from Components.ActionMap import *
from Components.config import *
from Components.ConfigList import *
from Components.UsageConfig import *
from Components.Label import Label
from Components.UsageConfig import *

from Screens.Screen import Screen

import os

from EGAMI.EGAMI_skins import EGDecodingSetup_Skin, EGInfoBarSetup_Skin

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
	Screen.__init__(self, session)
	self.skinName = ["Setup"]
		
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
	    Screen.__init__(self, session)
	    self.skinName = ["Setup"]
	    
	    self.list = []
	    
	    ConfigListScreen.__init__(self, self.list)
	    
	    self["key_red"] = Label(_("Save"))
	    self["key_green"] = Label(_("Exit"))

	    self["actions"] = ActionMap(["WizardActions", "ColorActions"],
	    {
	    "red": self.keySave,
	    "back": self.keyCancel,
	    "green": self.keyCancel,
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
