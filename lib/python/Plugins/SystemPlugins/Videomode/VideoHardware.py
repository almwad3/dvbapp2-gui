from enigma import eTimer
from Components.config import config, ConfigSelection, ConfigSubDict, ConfigYesNo
from Components.About import about

from Tools.CList import CList
from Tools.HardwareInfo import HardwareInfo
from os import path
from enigma import getBoxType

# The "VideoHardware" is the interface to /proc/stb/video.
# It generates hotplug events, and gives you the list of
# available and preferred modes, as well as handling the currently
# selected mode. No other strict checking is done.
class VideoHardware:
	rates = { } # high-level, use selectable modes.

	modes = { }  # a list of (high-level) modes for a certain port.

	rates["PAL"] =			{ "50Hz":	{ 50: "pal" },
								"60Hz":		{ 60: "pal60" },
								"multi":	{ 50: "pal", 60: "pal60" } }

	rates["NTSC"] =			{ "60Hz": 	{ 60: "ntsc" } }

	rates["Multi"] =		{ "multi": 	{ 50: "pal", 60: "ntsc" } }

	rates["480i"] =			{ "60Hz": 	{ 60: "480i" } }

	rates["576i"] =			{ "50Hz": 	{ 50: "576i" } }

	rates["480p"] =			{ "60Hz": 	{ 60: "480p" } }

	rates["576p"] =			{ "50Hz": 	{ 50: "576p" } }

	if about.getChipSetString().find('7335') != -1 or about.getChipSetString().find('7358') != -1 or about.getChipSetString().find('7356') != -1 or about.getChipSetString().find('7405') != -1 or about.getChipSetString().find('7424') != -1:
		rates["720p"] =		{ "24Hz": 		{ 24: "720p24" },
								"25Hz": 	{ 25: "720p25" },
								"30Hz": 	{ 30: "720p30" },
								"50Hz": 	{ 50: "720p50" },
								"60Hz": 	{ 60: "720p" },
								"multi": 	{ 50: "720p50", 60: "720p" } }
	else:
		rates["720p"] =		{ "50Hz": 	{ 50: "720p50" },
								"60Hz": 	{ 60: "720p" },
								"multi": 	{ 50: "720p50", 60: "720p" } }

	rates["1080i"] =		{ "50Hz":	{ 50: "1080i50" },
								"60Hz":		{ 60: "1080i" },
								"multi":	{ 50: "1080i50", 60: "1080i" } }

# 	if about.getChipSetString().find('7405') != -1 or about.getChipSetString().find('7335') != -1:
# 		rates["1080p"] =	{ "24Hz":		{ 24: "1080p24" },
# 								"25Hz":		{ 25: "1080p25" },
# 								"30Hz":		{ 30: "1080p30" }}
# 	elif about.getChipSetString().find('7358') != -1 or about.getChipSetString().find('7356') != -1:
# 		rates["1080p"] =	{ 	"24Hz":		{ 24: "1080p24" },
# 								"25Hz":		{ 25: "1080p25" },
# 								"30Hz":		{ 30: "1080p30" },
# 								"50Hz":		{ 50: "1080p50" },
# 								"60Hz":		{ 60: "1080p" },
# 								"multi":	{ 50: "1080p50", 60: "1080p" }}
	if about.getChipSetString().find('7358') != -1 or about.getChipSetString().find('7356') != -1 or about.getChipSetString().find('7424') != -1:
		rates["1080p"] =	{ 	"50Hz":		{ 50: "1080p50" },
								"60Hz":		{ 60: "1080p" },
								"multi":	{ 50: "1080p50", 60: "1080p" }}

	rates["PC"] = {
		"1024x768": { 60: "1024x768" }, # not possible on DM7025
		"800x600" : { 60: "800x600" },  # also not possible
		"720x480" : { 60: "720x480" },
		"720x576" : { 60: "720x576" },
		"1280x720": { 60: "1280x720" },
		"1280x720 multi": { 50: "1280x720_50", 60: "1280x720" },
		"1920x1080": { 60: "1920x1080"},
		"1920x1080 multi": { 50: "1920x1080", 60: "1920x1080_50" },
		"1280x1024" : { 60: "1280x1024"},
		"1366x768" : { 60: "1366x768"},
		"1366x768 multi" : { 50: "1366x768", 60: "1366x768_50" },
		"1280x768": { 60: "1280x768" },
		"640x480" : { 60: "640x480" }
	}

	modes["Scart"] = ["PAL", "NTSC", "Multi"]
	modes["DVI-PC"] = ["PC"]

	if about.getChipSetString().find('7358') != -1 or about.getChipSetString().find('7356') != -1 or about.getChipSetString().find('7424') != -1:
		modes["YPbPr"] = ["720p", "1080i", "1080p", "576p", "480p", "576i", "480i"]
		modes["DVI"] = ["720p", "1080i", "1080p", "576p", "480p", "576i", "480i"]
		widescreen_modes = set(["720p", "1080i", "1080p"])
	else:
		modes["YPbPr"] = ["720p", "1080i", "576p", "480p", "576i", "480i"]
		modes["DVI"] = ["720p", "1080i", "576p", "480p", "576i", "480i"]
		widescreen_modes = set(["720p", "1080i"])

	if getBoxType().startswith('vu'):
		if about.getChipSetString().find('7358') != -1 or about.getChipSetString().find('7356') != -1 or about.getChipSetString().find('7424') != -1:
			modes["Scart-YPbPr"] = ["720p", "1080i", "1080p", "576p", "480p", "576i", "480i"]
		else:
			modes["Scart-YPbPr"] = ["720p", "1080i", "576p", "480p", "576i", "480i"]

	def getOutputAspect(self):
		ret = (16,9)
		port = config.av.videoport.getValue()
		if port not in config.av.videomode:
			print "current port not available in getOutputAspect!!! force 16:9"
		else:
			mode = config.av.videomode[port].getValue()
			force_widescreen = self.isWidescreenMode(port, mode)
			is_widescreen = force_widescreen or config.av.aspect.getValue() in ("16_9", "16_10")
			is_auto = config.av.aspect.getValue() == "auto"
			if is_widescreen:
				if force_widescreen:
					pass
				else:
					aspect = {"16_9": "16:9", "16_10": "16:10"}[config.av.aspect.getValue()]
					if aspect == "16:10":
						ret = (16,10)
			elif is_auto:
				try:
					aspect_str = open("/proc/stb/vmpeg/0/aspect", "r").read()
					if aspect_str == "1": # 4:3
						ret = (4,3)
				except IOError:
					pass
			else:  # 4:3
				ret = (4,3)
		return ret

	def __init__(self):
		self.last_modes_preferred =  [ ]
		self.on_hotplug = CList()
		self.current_mode = None
		self.current_port = None

		self.readAvailableModes()

		if self.modes.has_key("DVI-PC") and not self.getModeList("DVI-PC"):
			print "remove DVI-PC because of not existing modes"
			del self.modes["DVI-PC"]
		if getBoxType() == 'et4x00' or getBoxType() == 'xp1000' or getBoxType() == 'tm2t' or getBoxType() == 'tmsingle' or getBoxType() == 'odimm7' or getBoxType() == 'vusolo2' or getBoxType() == 'tmnano':
			del self.modes["YPbPr"]
		if getBoxType() == 'gbquad' or getBoxType() == 'et5x00' or getBoxType() == 'ixussone' or getBoxType() == 'et6x00' or getBoxType() == 'tmnano':
			del self.modes["Scart"]

		self.createConfig()
		self.readPreferredModes()


		# take over old AVSwitch component :)
		from Components.AVSwitch import AVSwitch
		config.av.aspectratio.notifiers = [ ]
		config.av.tvsystem.notifiers = [ ]
		config.av.wss.notifiers = [ ]
		AVSwitch.getOutputAspect = self.getOutputAspect

		config.av.aspect.addNotifier(self.updateAspect)
		config.av.wss.addNotifier(self.updateWss)
		config.av.policy_43.addNotifier(self.updatePolicy43)
		config.av.policy_169.addNotifier(self.updatePolicy169)

	def readAvailableModes(self):
		try:
			f = open("/proc/stb/video/videomode_choices")
			modes = f.read()[:-1]
			f.close()
		except IOError:
			print "couldn't read available videomodes."
			self.modes_available = [ ]
			return
		self.modes_available = modes.split(' ')

	def readPreferredModes(self):
		try:
			f = open("/proc/stb/video/videomode_preferred")
			modes = f.read()[:-1]
			f.close()
			self.modes_preferred = modes.split(' ')
		except IOError:
			print "reading preferred modes failed, using all modes"
			self.modes_preferred = self.modes_available

		if self.modes_preferred != self.last_modes_preferred:
			self.last_modes_preferred = self.modes_preferred
			print "hotplug on dvi"
			self.on_hotplug("DVI") # must be DVI

	# check if a high-level mode with a given rate is available.
	def isModeAvailable(self, port, mode, rate):
		rate = self.rates[mode][rate]
		for mode in rate.values():
			if mode not in self.modes_available:
				return False
		return True

	def isWidescreenMode(self, port, mode):
		return mode in self.widescreen_modes

	def setMode(self, port, mode, rate, force = None):
		print "setMode - port:", port, "mode:", mode, "rate:", rate

		config.av.videoport.setValue(port)		# [iq]

		# we can ignore "port"
		self.current_mode = mode
		self.current_port = port
		modes = self.rates[mode][rate]

		mode_50 = modes.get(50)
		mode_60 = modes.get(60)
		if mode_50 is None or force == 60:
			mode_50 = mode_60
		if mode_60 is None or force == 50:
			mode_60 = mode_50

		mode_etc = None
		try:
			f = open("/proc/stb/video/videomode_50hz", "w")
			f.write(mode_50)
			f.close()
			f = open("/proc/stb/video/videomode_60hz", "w")
			f.write(mode_60)
			f.close()
		except:
			try:
				mode_etc = modes.get(int(rate[:2]))
				f = open("/proc/stb/video/videomode", "w")
				f.write(mode_etc)
				f.close()
				# not support 50Hz, 60Hz for 1080p
			except:
				try:
					# fallback if no possibility to setup 50/60 hz mode
					f = open("/proc/stb/video/videomode", "w")
					f.write(mode_50)
					f.close()
				except IOError:
					print "setting videomode failed."

		# self.updateAspect(None)

	def saveMode(self, port, mode, rate):
		print "saveMode", port, mode, rate
		config.av.videoport.setValue(port)
		config.av.videoport.save()
		if port in config.av.videomode:
			config.av.videomode[port].setValue(mode)
			config.av.videomode[port].save()
		if mode in config.av.videorate:
			config.av.videorate[mode].setValue(rate)
			config.av.videorate[mode].save()

	def isPortAvailable(self, port):
		# fixme
		return True

	def isPortUsed(self, port):
		if port == "DVI":
			self.readPreferredModes()
			return len(self.modes_preferred) != 0
		else:
			return True

	def getPortList(self):
		return [port for port in self.modes if self.isPortAvailable(port)]

	# get a list with all modes, with all rates, for a given port.
	def getModeList(self, port):
		print "getModeList for port", port
		res = [ ]
		for mode in self.modes[port]:
			# list all rates which are completely valid
			rates = [rate for rate in self.rates[mode] if self.isModeAvailable(port, mode, rate)]

			# if at least one rate is ok, add this mode
			if len(rates):
				res.append( (mode, rates) )
		return res

	def createConfig(self, *args):
		hw_type = HardwareInfo().get_device_name()
		has_hdmi = HardwareInfo().has_hdmi()
		lst = []

		config.av.videomode = ConfigSubDict()
		config.av.videorate = ConfigSubDict()

		# create list of output ports
		portlist = self.getPortList()
		for port in portlist:
			descr = port
			if descr == 'DVI' and has_hdmi:
				descr = 'HDMI'
			elif descr == 'DVI-PC' and has_hdmi:
				descr = 'HDMI-PC'
			lst.append((port, descr))

			# create list of available modes
			modes = self.getModeList(port)
			if len(modes):
				config.av.videomode[port] = ConfigSelection(choices = [mode for (mode, rates) in modes])
			for (mode, rates) in modes:
				config.av.videorate[mode] = ConfigSelection(choices = rates)
		config.av.videoport = ConfigSelection(choices = lst)

		def setColorFormatAsPort(configElement):
			if configElement.getValue() == "YPbPr" or configElement.getValue() == "Scart-YPbPr":
				config.av.colorformat.setValue("yuv")
		config.av.videoport.addNotifier(setColorFormatAsPort)

	def setConfiguredMode(self):
		port = config.av.videoport.getValue()
		if port not in config.av.videomode:
			print "current port not available, not setting videomode"
			return

		mode = config.av.videomode[port].getValue()

		if mode not in config.av.videorate:
			print "current mode not available, not setting videomode"
			return

		rate = config.av.videorate[mode].getValue()
		self.setMode(port, mode, rate)

	def updateAspect(self, cfgelement):
		print "-> setting aspect: %s" % cfgelement.value
		f = open("/proc/stb/video/aspect", "w")
		f.write(cfgelement.value)
		f.close()

	def updateWss(self, cfgelement):
		if not cfgelement.value:
			wss = "auto(4:3_off)"
		else:
			wss = "auto"
		print "-> setting wss: %s" % wss
		f = open("/proc/stb/denc/0/wss", "w")
		f.write(wss)
		f.close()

	def updatePolicy43(self, cfgelement):
		print "-> setting policy: %s" % cfgelement.value
		f = open("/proc/stb/video/policy", "w")
		f.write(cfgelement.value)
		f.close()

	def updatePolicy169(self, cfgelement):
		if path.exists("/proc/stb/video/policy2"):
			print "-> setting policy2: %s" % cfgelement.value
			f = open("/proc/stb/video/policy2", "w")
			f.write(cfgelement.value)
			f.close()

config.av.edid_override = ConfigYesNo(default = False)
video_hw = VideoHardware()
video_hw.setConfiguredMode()
