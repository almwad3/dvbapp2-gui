from Screens.Screen import Screen
from Components.SystemInfo import SystemInfo
from Components.ConfigList import ConfigListScreen
from Components.config import config, configfile, getConfigListEntry, ConfigBoolean, ConfigNothing, ConfigSlider
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Sources.Boolean import Boolean
from Components.ServiceEventTracker import ServiceEventTracker
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import iPlayableService, iServiceInformation, eTimer
from os import path

from Components.AVSwitch import iAVSwitch

resolutionlabel = None

class VideoSetup(Screen, ConfigListScreen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = ["Setup" ]
		self.setup_title = _("A/V settings")
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self["VKeyIcon"] = Boolean(False)
		self['footnote'] = Label()

		self.hw = iAVSwitch
		self.onChangedEntry = [ ]

		# handle hotplug by re-creating setup
		self.onShow.append(self.startHotplug)
		self.onHide.append(self.stopHotplug)

		self.list = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)

		from Components.ActionMap import ActionMap
		self["actions"] = ActionMap(["SetupActions", "MenuActions"],
			{
				"cancel": self.keyCancel,
				"save": self.apply,
				"menu": self.closeRecursive,
			}, -2)

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["description"] = Label("")

		self.createSetup()
		self.grabLastGoodMode()
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.setup_title)

	def startHotplug(self):
		self.hw.on_hotplug.append(self.createSetup)

	def stopHotplug(self):
		self.hw.on_hotplug.remove(self.createSetup)

	def createSetup(self):
		level = config.usage.setup_level.index

		self.list = [
			getConfigListEntry(_("Video output"), config.av.videoport, _("Configures which video output connector will be used."))
		]
		if config.av.videoport.getValue() in ('HDMI', 'YPbPr', 'Scart-YPbPr') and not path.exists(resolveFilename(SCOPE_PLUGINS)+'SystemPlugins/AutoResolution'):
			self.list.append(getConfigListEntry(_("Automatic resolution"), config.av.autores,_("If enabled the output resolution of the box will try to match the resolution of the video contents resolution")))
			if config.av.autores.getValue() in ('all', 'hd'):
				self.list.append(getConfigListEntry(_("Automatic resolution label"), config.av.autores_label_timeout,_("Allows you to adjust the amount of time the resolution infomation display on screen.")))
				self.list.append(getConfigListEntry(_("Allow 25Hz/30Hz"), config.av.autores_all_res,_("With this option enabled these refresh rates will be used. (please note not all TV's support these rates).")))

		# if we have modes for this port:
		if (config.av.videoport.getValue() in config.av.videomode and config.av.autores.getValue() == 'disabled') or config.av.videoport.getValue() == 'Scart':
			# add mode- and rate-selection:
			self.list.append(getConfigListEntry(pgettext("Video output mode", "Mode"), config.av.videomode[config.av.videoport.getValue()], _("This option configures the video output mode (or resolution).")))
			if config.av.videomode[config.av.videoport.getValue()].getValue() == 'PC':
				self.list.append(getConfigListEntry(_("Resolution"), config.av.videorate[config.av.videomode[config.av.videoport.getValue()].getValue()], _("This option configures the screen resolution in PC output mode.")))
			elif config.av.videoport.getValue() != 'Scart':
				self.list.append(getConfigListEntry(_("Refresh rate"), config.av.videorate[config.av.videomode[config.av.videoport.getValue()].getValue()], _("Configure the refresh rate of the screen.")))

		port = config.av.videoport.getValue()
		if port not in config.av.videomode:
			mode = None
		else:
			mode = config.av.videomode[port].getValue()

		# some modes (720p, 1080i) are always widescreen. Don't let the user select something here, "auto" is not what he wants.
		force_wide = self.hw.isWidescreenMode(port, mode)

		# if not force_wide:
		# 	self.list.append(getConfigListEntry(_("Aspect ratio"), config.av.aspect, _("Configure the aspect ratio of the screen.")))

		if force_wide or config.av.aspect.getValue() in ("16:9", "16:10"):
			self.list.extend((
				getConfigListEntry(_("Display 4:3 content as"), config.av.policy_43, _("When the content has an aspect ratio of 4:3, choose whether to scale/stretch the picture.")),
				getConfigListEntry(_("Display >16:9 content as"), config.av.policy_169, _("When the content has an aspect ratio of 16:9, choose whether to scale/stretch the picture."))
			))
		elif config.av.aspect.getValue() == "4:3":
			self.list.append(getConfigListEntry(_("Display 16:9 content as"), config.av.policy_169, _("When the content has an aspect ratio of 16:9, choose whether to scale/stretch the picture.")))

#		if config.av.videoport.getValue() == "HDMI":
#			self.list.append(getConfigListEntry(_("Allow unsupported modes"), config.av.edid_override))
		if config.av.videoport.getValue() == "Scart":
			self.list.append(getConfigListEntry(_("Color format"), config.av.colorformat, _("Configure which color format should be used on the SCART output.")))
			if level >= 1:
				self.list.append(getConfigListEntry(_("WSS on 4:3"), config.av.wss, _("When enabled, content with an aspect ratio of 4:3 will be stretched to fit the screen.")))
				if SystemInfo["ScartSwitch"]:
					self.list.append(getConfigListEntry(_("Auto scart switching"), config.av.vcrswitch, _("When enabled, your receiver will detect activity on the VCR SCART input.")))

		if level >= 1:
			if SystemInfo["CanDownmixAC3"]:
				self.list.append(getConfigListEntry(_("Digital downmix"), config.av.downmix_ac3, _("Choose whether multi channel sound tracks should be downmixed to stereo.")))
			self.list.extend((
				getConfigListEntry(_("General AC3 delay"), config.av.generalAC3delay, _("This option configures the general audio delay of Dolby Digital sound tracks.")),
				getConfigListEntry(_("General PCM delay"), config.av.generalPCMdelay, _("This option configures the general audio delay of stereo sound tracks."))
			))

			if SystemInfo["Can3DSurround"]:
				self.list.append(getConfigListEntry(_("3D Surround"), config.av.surround_3d,_("This option configures you can enable 3D Surround Sound.")))

			if SystemInfo["Canedidchecking"]:
				self.list.append(getConfigListEntry(_("Bypass HDMI EDID Check"), config.av.bypass_edid_checking,_("This option configures you can Bypass HDMI EDID check")))

#		if not isinstance(config.av.scaler_sharpness, ConfigNothing):
#			self.list.append(getConfigListEntry(_("Scaler sharpness"), config.av.scaler_sharpness, _("This option configures the picture sharpness.")))

		self["config"].list = self.list
		self["config"].l.setList(self.list)
		if config.usage.sort_settings.getValue():
			self["config"].list.sort()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.createSetup()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createSetup()

	def confirm(self, confirmed):
		if not confirmed:
			config.av.videoport.setValue(self.last_good[0])
			config.av.videomode[self.last_good[0]].setValue(self.last_good[1])
			config.av.videorate[self.last_good[1]].setValue(self.last_good[2])
			self.hw.setMode(*self.last_good)
		else:
			self.keySave()

	def grabLastGoodMode(self):
		port = config.av.videoport.getValue()
		mode = config.av.videomode[port].getValue()
		rate = config.av.videorate[mode].getValue()
		self.last_good = (port, mode, rate)

	def saveAll(self):
		if config.av.videoport.getValue() == 'Scart':
			config.av.autores.setValue('disabled')
		for x in self["config"].list:
			x[1].save()
		configfile.save()

	def apply(self):
		port = config.av.videoport.getValue()
		mode = config.av.videomode[port].getValue()
		rate = config.av.videorate[mode].getValue()
		if (port, mode, rate) != self.last_good:
			self.hw.setMode(port, mode, rate)
			from Screens.MessageBox import MessageBox
			self.session.openWithCallback(self.confirm, MessageBox, _("Is this video mode ok?"), MessageBox.TYPE_YESNO, timeout = 20, default = False)
		else:
			self.keySave()

	# for summary:
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())

	def getCurrentDescription(self):
		return self["config"].getCurrent() and len(self["config"].getCurrent()) > 2 and self["config"].getCurrent()[2] or ""

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

class AutoVideoModeLabel(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)

		self["content"] = Label()
		self["restxt"] = Label()

		self.hideTimer = eTimer()
		self.hideTimer.callback.append(self.hide)

		self.onShow.append(self.hide_me)

	def hide_me(self):
		idx = config.av.autores_label_timeout.index
		if idx:
			idx = idx+4
			self.hideTimer.start(idx*1000, True)

class AutoVideoMode(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.__event_tracker = ServiceEventTracker(screen=self, eventmap=
			{
				iPlayableService.evVideoSizeChanged: self.VideoChanged,
				iPlayableService.evVideoProgressiveChanged: self.VideoChanged,
				iPlayableService.evVideoFramerateChanged: self.VideoChanged,
				iPlayableService.evBuffering: self.BufferInfo,
			})

		self.delay = False
		self.bufferfull = True
		self.detecttimer = eTimer()
		self.detecttimer.callback.append(self.VideoChangeDetect)

	def BufferInfo(self):
		bufferInfo = self.session.nav.getCurrentService().streamed().getBufferCharge()
		if bufferInfo[0] > 98:
			self.bufferfull = True
			self.VideoChanged()
		else:
			self.bufferfull = False

	def VideoChanged(self):
		print 'REF:',self.session.nav.getCurrentlyPlayingServiceReference().toString()
		print 'IS STREAM:',self.session.nav.getCurrentlyPlayingServiceReference().toString().startswith('4097:')
		if self.session.nav.getCurrentlyPlayingServiceReference() and not self.session.nav.getCurrentlyPlayingServiceReference().toString().startswith('4097:'):
			delay = 400
		else:
			delay = 800
		if not self.detecttimer.isActive() and not self.delay:
			print 'TEST 1:',delay
			self.delay = True
			self.detecttimer.start(delay)
		else:
			print 'TEST2:',delay
			self.delay = True
			self.detecttimer.stop()
			self.detecttimer.start(delay)

	def VideoChangeDetect(self):
		config_port = config.av.videoport.getValue()
		config_mode = str(config.av.videomode[config_port].getValue()).replace('\n','')
		config_res = str(config.av.videomode[config_port].getValue()[:-1]).replace('\n','')
		config_pol = str(config.av.videomode[config_port].getValue()[-1:]).replace('\n','')
		config_rate = str(config.av.videorate[config_mode].getValue()).replace('Hz','').replace('\n','')

		print 'config port:',config_port
		print 'config mode:',config_mode
		print 'config res:',config_res
		print 'config pol:',config_pol
		print 'config rate:',config_rate
		print ' '

		f = open("/proc/stb/video/videomode")
		current_mode = f.read()[:-1].replace('\n','')
		f.close()
		if current_mode.upper() in ('PAL', 'NTSC'):
			current_mode = current_mode.upper()

		current_pol = ''
		if current_mode.find('i') != -1:
			current_pol = 'i'
		elif current_mode.find('p') != -1:
			current_pol = 'p'
		current_res = current_pol and current_mode.split(current_pol)[0].replace('\n','') or ""
		current_rate = current_pol and current_mode.split(current_pol)[0].replace('\n','') and current_mode.split(current_pol)[1].replace('\n','') or ""

		print 'current mode:',current_mode
		print 'current res:',current_res
		print 'current pol:',current_pol
		print 'current rate:',current_rate
		print ' '


		video_height = None
		video_width = None
		video_pol = None
		video_rate = None
		if path.exists("/proc/stb/vmpeg/0/yres"):
			f = open("/proc/stb/vmpeg/0/yres", "r")
			video_height = int(f.read(),16)
			f.close()
		if path.exists("/proc/stb/vmpeg/0/xres"):
			f = open("/proc/stb/vmpeg/0/xres", "r")
			video_width = int(f.read(),16)
			f.close()
		if path.exists("/proc/stb/vmpeg/0/progressive"):
			f = open("/proc/stb/vmpeg/0/progressive", "r")
			video_pol = "p" if int(f.read(),16) else "i"
			f.close()
		if path.exists("/proc/stb/vmpeg/0/framerate"):
			f = open("/proc/stb/vmpeg/0/framerate", "r")
			video_rate = int(f.read())
			f.close()

		if not video_height or not video_width or not video_pol or not video_rate:
			service = self.session.nav.getCurrentService()
			if service is not None:
				info = service.info()
			else:
				info = None

			if info:
				video_height = int(info.getInfo(iServiceInformation.sVideoHeight))
				video_width = int(info.getInfo(iServiceInformation.sVideoWidth))
				video_pol = ("i", "p")[info.getInfo(iServiceInformation.sProgressive)]
				video_rate = int(info.getInfo(iServiceInformation.sFrameRate))

		if video_height and video_width and video_pol and video_rate:
			print 'video height:',video_height
			print 'video width:',video_width
			print 'video pol:',video_pol
			print 'video rate:',video_rate
			print ' '

			resolutionlabel["content"].setText(_("Video content: %ix%i%s %iHz") % (video_width, video_height, video_pol, (video_rate + 500) / 1000))

			if video_height != -1:
				if video_height > 720:
					new_res = "1080"
				elif video_height > 576 and video_height <= 720:
					new_res = "720"
				elif video_height > 480 and video_height <= 576:
					new_res = "576"
				else:
					new_res = "480"
			else:
				new_res = config_res

			if video_rate != -1:
				if video_rate == 23976:
					new_rate = 24000
				elif video_rate == 29970 and config.av.autores_all_res.getValue() and video_pol == 'p':
					new_rate = 30000
				elif video_rate == 25000 and (not config.av.autores_all_res.getValue() or video_pol == 'i'):
					new_rate = 50000
				elif video_rate == 59940 or (video_rate == 29970 and (not config.av.autores_all_res.getValue() or video_pol == 'i')):
					new_rate = 60000
				else:
					new_rate = video_rate
				new_rate = str((new_rate + 500) / 1000)
			else:
				new_rate = config_rate

			if video_pol != -1:
				new_pol = str(video_pol)
			else:
				new_pol = config_pol

			print 'new res:',new_res
			print 'new pol:',new_pol
			print 'new rate:',new_rate

			print 'config.av.autores:',config.av.autores.getValue()
			write_mode = None
			new_mode = None
			if config_mode in ('PAL', 'NTSC'):
				write_mode = config_mode
			elif config.av.autores.getValue() == 'all' or (config.av.autores.getValue() == 'hd' and int(new_res) >= 720):
				if new_res+new_pol+new_rate in iAVSwitch.modes_available:
					new_mode = new_res+new_pol+new_rate
				elif new_res+new_pol in iAVSwitch.modes_available:
					new_mode = new_res+new_pol
				else:
					write_mode = config_mode+current_rate

				print 'new mode:',new_mode

				write_mode = new_mode
			elif config.av.autores.getValue() == 'hd' and int(new_res) <= 576:
				write_mode = config_res+current_pol+current_rate
			else:
				if path.exists('/proc/stb/video/videomode_%shz' % new_rate) and config_rate == 'multi':
					f = open("/proc/stb/video/videomode_%shz" % new_rate, "r")
					multi_videomode = f.read().replace('\n','')
					print 'multi_videomode:',multi_videomode
					f.close()
					if multi_videomode and (current_mode != multi_videomode):
						write_mode = multi_videomode
					else:
						write_mode = config_mode+current_rate

				print 'new mode:',write_mode

			print ' '
			print 'CURRENT MODE:',current_mode
			print 'NEW MODE:',write_mode
			print ' '
			if write_mode and current_mode != write_mode and self.bufferfull:
				resolutionlabel["restxt"].setText(_("Video mode: %s") % write_mode)
				if config.av.autores_label_timeout.getValue() != '0':
					resolutionlabel.show()
				print "[VideoMode] setMode - port: %s, mode: %s" % (config_port, write_mode)
				f = open("/proc/stb/video/videomode", "w")
				f.write(write_mode)
				f.close()

		iAVSwitch.setAspect(config.av.aspect)
		iAVSwitch.setWss(config.av.wss)
		iAVSwitch.setPolicy43(config.av.policy_43)
		iAVSwitch.setPolicy169(config.av.policy_169)

		self.delay = False
		self.detecttimer.stop()

def autostart(session):
	if not path.exists(resolveFilename(SCOPE_PLUGINS)+'SystemPlugins/AutoResolution'):
		if resolutionlabel is None:
			global resolutionlabel
			resolutionlabel = session.instantiateDialog(AutoVideoModeLabel)
		AutoVideoMode(session)
