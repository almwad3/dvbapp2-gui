from Screens.MessageBox import MessageBox
from Screens.PluginBrowser import *
from enigma import loadPNG, eSize, ePoint, eSlider, eTimer, RT_HALIGN_RIGHT, fontRenderClass, eConsoleAppContainer
from Screens.Screen import Screen
from Screens.PluginBrowser import PluginDownloadBrowser
from Components.GUIComponent import *
from Components.HTMLComponent import *
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Components.config import *
from Components.ConfigList import *
from Components.FileList import * 
from Components.Sources.List import List 
from Components.Label import Label 
from Components.MenuList import MenuList 
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest 
from Components.Pixmap import Pixmap 
from Components.PluginComponent import plugins 
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, fileExists
from Tools.LoadPixmap import LoadPixmap
import os
import sys
import traceback
import StringIO

from EGAMI.EGAMI_tools import wyszukaj_re, unload_modules
from EGAMI.EGAMI_skins import EGAddonInfo_Skin, EG_InternetAddons_Skin, EGAddonRemove_Skin, AddonManager_Skin, EG_Manual_installation_Skin, EGAddonMenu_Skin
	
from xml.dom import EMPTY_NAMESPACE 
import xml.dom.minidom 

from Plugins.Plugin import PluginDescriptor

fp = None

class BoundFunction():
    __module__ = __name__

    def __init__(self, fnc, *args):
        self.fnc = fnc
        self.args = args

    def __call__(self):
        self.fnc(*self.args)

def odinstalacyjnyPlik(ipkgResult, menuName):
	if (not os.path.exists('/usr/uninstall/')):
		os.system('mkdir /usr/uninstall/')
	while 1:
		currentLine = ipkgResult.readline()
		if (currentLine == ''):
			break
		foundPacketNamePos = currentLine.find('Installing ')
		if (foundPacketNamePos is not -1):
			name = currentLine[(foundPacketNamePos + 11):]
			nextSpace = name.find(' (')
			name = name[:nextSpace]
			os.system(('mkdir /usr/uninstall/' + name))
			fp = open(((('/usr/uninstall/' + name) + '/' + name) ), 'w')
			fp.write(menuName)
			fp.close()
			return None

def EGAddonEntry(name, desc, author, version, size, info_txt, info_pic, function):
	res = [(name, function, info_txt, info_pic)]
	res.append(MultiContentEntryText(pos=(0, 6), size=(400, 20), font=0, text=name))
	if (version != ''):
		res.append(MultiContentEntryText(pos=(292, 28), size=(98, 15), font=1, flags=RT_HALIGN_RIGHT, text=str(('Version: ' + version))))
	if (desc != ''):
		res.append(MultiContentEntryText(pos=(0, 28), size=(500, 15), font=1, text=str(('Desc: ' + desc))))
	if (author != ''):
		res.append(MultiContentEntryText(pos=(0, 44), size=(390, 15), font=1, text=str(('Author: ' + author))))
	if (size != ''):
		res.append(MultiContentEntryText(pos=(292, 44), size=(108, 15), font=1, flags=RT_HALIGN_RIGHT, text=str((('Size: ' + size) + 'kB'))))
	return res



def EGAddonMenuEntry(name, desc, function):
	res = [(name, function)]
	res.append(MultiContentEntryText(pos=(0, 5), size=(500, 20), font=0, text=name))
	if (desc != ''):
		res.append(MultiContentEntryText(pos=(0, 28), size=(500, 15), font=1, text=desc))
	return res


class EGListaAddonow(MenuList, HTMLComponent, GUIComponent):
	__module__ = __name__
	def __init__(self, list, enableWrapAround = False):
		GUIComponent.__init__(self)
		self.l = eListboxPythonMultiContent()
		self.list = list
		self.l.setList(list)
		self.l.setFont(0, gFont('Regular', 20))
		self.l.setFont(1, gFont('Regular', 14))
		self.l.setItemHeight(50)
		self.onSelectionChanged = []
		self.enableWrapAround = enableWrapAround
		
		GUI_WIDGET = eListbox
		
	def postWidgetCreate(self, instance):
		instance.setContent(self.l)
		instance.selectionChanged.get().append(self.selectionChanged)
		if self.enableWrapAround:
			self.instance.setWrapAround(True)
				
	def selectionChanged(self):
		for f in self.onSelectionChanged:
			f()
			
			
class EGScrollLabel(ScrollLabel):
	    __module__ = __name__
	  
	    def resizeAndSet(self, newText, height):
		s = self.instance.size()
		textSize = (s.width(), s.height())
		textSize = (textSize[0], (textSize[1] - height))
		self.instance.resize(eSize(*textSize))
		p = self.instance.position()
		pos = (p.x(), (p.y() + height))
		self.instance.move(ePoint(pos[0], pos[1]))
		self.long_text.resize(eSize(*textSize))
		self.long_text.move(ePoint(pos[0], pos[1]))
		s = self.long_text.size()
		lineheight = fontRenderClass.getInstance().getLineHeight(self.long_text.getFont())
		lines = int((s.height() / lineheight))
		self.pageHeight = int((lines * lineheight))
		self.instance.resize(eSize(s.width(), (self.pageHeight + int((lineheight / 6)))))
		self.scrollbar.move(ePoint((s.width() - 20), 0))
		self.scrollbar.resize(eSize(20, (self.pageHeight + int((lineheight / 6)))))
		self.scrollbar.setOrientation(eSlider.orVertical)
		self.scrollbar.setRange(0, 100)
		self.scrollbar.setBorderWidth(1)
		self.long_text.move(ePoint(0, 0))
		self.long_text.resize(eSize((s.width() - 30), (self.pageHeight * 16)))
		self.setText(newText)
		
		
class EGAddonInfo(Screen):
	__module__ = __name__
	def __init__(self, session, textFile, picFile):
		self.skin = EGAddonInfo_Skin
		Screen.__init__(self, session)
		self['text'] = EGScrollLabel('No info found...')
		self['image'] = Pixmap()
		self['image'].hide()
		self['actions'] = ActionMap(['WizardActions',
		  'DirectionActions'], {'ok': self.cancel,
		  'back': self.cancel,
		  'up': self['text'].pageUp,
		  'down': self['text'].pageDown}, -1)
		self.infoFile = textFile
		self.imageFile = picFile
		self.onLayoutFinish.append(self.downloadInfo)
		
		
	def cancel(self):
		self.close()
		unload_modules(__name__)


	def downloadInfo(self):
	    os.system('rm /tmp/AddonInfo.txt')
	    if (not self.infoFile.endswith('/')):
		    os.system((('wget -q ' + self.infoFile) + ' -O /tmp/AddonInfo.txt'))
	    if fileExists('/tmp/AddonInfo.txt'):
			infoFile = open('/tmp/AddonInfo.txt', 'r')
			theText = infoFile.read()
			infoFile.close()
			os.system('rm /tmp/AddonInfo.txt')
			self['text'].setText(theText)
	    else:
			self['text'].setText(_('No further information available.'))
	    try:
			(self.imageFile, width, height,) = self.imageFile.split('|')
	    except:
			width = 48
			height = 48
		    
	    width = int(width)
	    height = int(height)
	    os.system('rm /tmp/AddonInfo.png')
	    if (not self.imageFile.endswith('/')):
		    os.system((('wget -q ' + self.imageFile) + ' -O /tmp/AddonInfo.png'))
	    if fileExists('/tmp/AddonInfo.png'):
		    self['image'].instance.setPixmapFromFile('/tmp/AddonInfo.png')
		    pixSize = (width, height)
		    #self['image'].instance.resize(eSize(*pixSize))
		    #self['text'].resizeAndSet(theText, height)
		    self['image'].show()
		    os.system('rm /tmp/AddonInfo.png')

class EG_InternetAddons(Screen):
	__module__ = __name__
	ALLOW_SUSPEND = True
	STATE_IDLE = 0
	STATE_DOWNLOAD = 1
	STATE_INSTALL = 2
	def __init__(self, session, parent, childNode, url):
		Screen.__init__(self, session)
		self.skinName = "EG_InternetAddons"
		self.skin = EG_InternetAddons_Skin
		menuList = []
		self.multi = False
		self.url = url
		try:
			header = parent.getAttribute('text').encode('UTF-8')
			menuType = parent.getAttribute('type').encode('UTF-8')
			if (menuType == 'multi'):
				self.multi = True
			else:
				self.multi = False
			menuList = self.buildMenuTree(childNode)
		except:
			tracefp = StringIO.StringIO()
			traceback.print_exc(file=tracefp)
			message = tracefp.getvalue()
		if self.multi:
			self['menu'] = EGListaAddonow(menuList)
		else:
			self['menu'] = MenuList(menuList)
			
		self['actions'] = ActionMap(['ColorActions', 'OkCancelActions',
		  'MovieSelectionActions'], {'ok': self.nacisniecieOK,
		  'red': self.nacisniecieOK,
		  'cancel': self.closeNonRecursive,
		  'exit': self.closeRecursive,
		  'blue': self.showAddonInfo})
		
		self['status'] = Label(_('Please, choose addon to install:'))
		self['key_red'] = Label(_('Download'))
		self['key_blue'] = Label(_('Preview'))
		self.state = self.STATE_IDLE
		self.StateTimer = eTimer()
		self.StateTimer.stop()
		self.StateTimer.timeout.get().append(self.uruchomInstalator)


	def uruchomInstalator(self):
		if (self.state == self.STATE_DOWNLOAD):
			self.state = self.STATE_IDLE
			#self.fileUrl = 'http://egami-image.com.com/image-feed/enigma2/' + self.saved_url
			self.fileUrl = self.url[0:-19] + self.saved_url
			if os.path.exists('/tmp/Addon.ipk'):
				os.system('rm /tmp/Addon.ipk')
			if ((self.fileUrl.endswith(".tgz")) or (self.fileUrl.endswith(".tar.gz")) or (self.fileUrl.endswith(".tar.bz2"))):
				os.system((('wget -q ' + self.fileUrl) + ' -O /tmp/Addon.tgz'))
			else:
				os.system((('wget -q ' + self.fileUrl) + ' -O /tmp/Addon.ipk'))
			message = str(((_('Do You want to install') + ' ') + self.saved_item_name) + '?')
			if os.path.exists('/tmp/Addon.ipk'):
				installBox = self.session.openWithCallback(self.instalujIPK, MessageBox, _(message), MessageBox.TYPE_YESNO)
				installBox.setTitle(_('IPK Installation...'))
			elif os.path.exists('/tmp/Addon.tgz'):
				installBox = self.session.openWithCallback(self.instalujTGZ, MessageBox, _(message), MessageBox.TYPE_YESNO)
				installBox.setTitle(_('EGAMI Package Installation...'))
			else:
				errorBox = self.session.open(MessageBox, _('Failed to download an Addon...'), MessageBox.TYPE_ERROR)
				errorBox.setTitle(_('Failed...'))
			return None
		elif (self.state == self.STATE_INSTALL):
			if os.path.exists('/tmp/Addon.ipk'):
				resultFile = os.popen('ipkg -force-overwrite install /tmp/Addon.ipk ; rm /tmp/Addon.ipk')
				odinstalacyjnyPlik(resultFile, self.saved_item_name)
				infoBox = self.session.openWithCallback(self.rebootGUI, MessageBox, _("Addon installed sucessfully !\nTo get it on plugin list, You need to reload GUI. Would You like to do it right now ?"), MessageBox.TYPE_YESNO)
				infoBox.setTitle(_('Success...'))		
				self['status'].setText(_('Addon installed sucessfully !'))
				self.state = self.STATE_IDLE
				self.StateTimer.stop()
				return None
			elif os.path.exists('/tmp/Addon.tgz'):
				resultFile = os.popen('cd /; tar -xz -f /tmp/Addon.tgz ; rm /tmp/Addon.tgz;rm /usr/sbin/nab_e2_restart.sh; chmod 755 /tmp/egami_e2_installer.sh; /tmp/egami_e2_installer.sh; rm /tmp/egami_e2_installer.sh')
				if fileExists('/tmp/restartgui'):
					infoBox = self.session.openWithCallback(self.rebootGUI, MessageBox, _("Addon installed sucessfully !\nTo get it on plugin list, You need to reload GUI. Would You like to do it right now ?"), MessageBox.TYPE_YESNO)
				else:
					infoBox = self.session.open(MessageBox, _('Addon installed sucessfully !'), MessageBox.TYPE_INFO, 5)
				infoBox.setTitle(_('Success...'))
				self['status'].setText(_('Addon installed sucessfully !'))
				self.state = self.STATE_IDLE
				self.StateTimer.stop()
		elif (self.state == self.STATE_IDLE):
			self['status'].setText(_('Please, choose an addon to install:'))
			self.StateTimer.stop()
			return None


	def rebootGUI(self, yesno):
		if yesno:
			os.system("killall -9 enigma2")
		else:
			self['status'].setText(_('Remember to reload enigma2 !'))
		
		
	def pobierzIPK(self, item, url, size_str):
		self.saved_item_name = item
		self.saved_url = url
		self.state = self.STATE_DOWNLOAD
		self['status'].setText(_('Downloading an addon... Please wait...'))
		self.StateTimer.start(200, True)
		
		
	def instalujIPK(self, yesno):
		if yesno:
			self.state = self.STATE_INSTALL
			self['status'].setText(_('Installing an addon... Please wait...'))
			self.StateTimer.start(200, True)
		else:
			infoBox = self.session.open(MessageBox, _('Installation aborted !'), MessageBox.TYPE_INFO)
			self.state = self.STATE_IDLE
			return None


	def instalujTGZ(self, yesno):
		if yesno:
			self.state = self.STATE_INSTALL
			self['status'].setText(_('Installing an addon... Please wait...'))
			self.StateTimer.start(200, True)
		else:
			infoBox = self.session.open(MessageBox, _('Installation aborted !'), MessageBox.TYPE_INFO)
			self.state = self.STATE_IDLE
			return None
		
		
	def nacisniecieOK(self):
		try:
			if self.multi:
				selection = self['menu'].getCurrent()
				selection[0][1]()
			else:
				selection = self['menu'].l.getCurrentSelection()
				selection[1]()
		except:
			tracefp = StringIO.StringIO()
			traceback.print_exc(file=tracefp)
			message = tracefp.getvalue()
			
			
	def zamknijMenu(self, *res):
		if (len(res) and res[0]):
			plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
			self.close(True)
			unload_modules(__name__)


	def showAddonInfo(self):
		try:
			if self.multi:
				selection = self['menu'].getCurrent()
				info_txt = selection[0][2]
				info_pic = selection[0][3]
			else:
				selection = self['menu'].l.getCurrentSelection()
				info_txt = selection[2]
				info_pic = selection[3]
		except:
			info_txt = ''
			info_pic = ''
		info_txt = str(info_txt)
		info_pic = str(info_pic)
		self.root_url = ('http://egami-image.com/image-feed/enigma2/')
		infoBox = self.session.open(EGAddonInfo, str((self.root_url + info_txt)), str((self.root_url + info_pic)))
		if self.multi:
			selection = self['menu'].getCurrent()
			infoBox.setTitle(_(selection[0][0]))
		else:
			selection = self['menu'].l.getCurrentSelection()
			infoBox.setTitle(_(selection[0]))
	    
	    
	def noweMenu(self, destList, node):
		menuTitle = node.getAttribute('text').encode('UTF-8')
		menuDesc = node.getAttribute('desc').encode('UTF-8')
		a = BoundFunction(self.session.openWithCallback, self.zamknijMenu, EG_InternetAddons, node, node.childNodes, self.url)
		if self.multi:
			destList.append(EGAddonMenuEntry(menuTitle, menuDesc, a))
		else:
			destList.append((menuTitle, a))
			
			
	def addItem(self, destList, node):
		item_text = node.getAttribute('text').encode('UTF-8')
		item_url = node.getAttribute('url').encode('UTF-8')
		item_desc = node.getAttribute('desc').encode('UTF-8')
		item_author = node.getAttribute('author').encode('UTF-8')
		item_version = node.getAttribute('version').encode('UTF-8')
		item_size = node.getAttribute('size').encode('UTF-8')
		info_txt = node.getAttribute('info_txt').encode('UTF-8')
		info_pic = node.getAttribute('info_pic').encode('UTF-8')
		a = BoundFunction(self.pobierzIPK, item_text, item_url, item_size)
		if self.multi:
			destList.append(EGAddonEntry(item_text, item_desc, item_author, item_version, item_size, info_txt, info_pic, a))
		else:
			destList.append((item_text, a, info_txt, info_pic))
			
			
	def buildMenuTree(self, childNode):
		list = []
		for x in childNode:
			if (x.nodeType != xml.dom.minidom.Element.nodeType):
				pass
			elif (x.tagName == 'item'):
				self.addItem(list, x)
			elif (x.tagName == 'menu'):
				self.noweMenu(list, x)
		return list


	def closeNonRecursive(self):
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.close(False)
		unload_modules(__name__)


	def closeRecursive(self):
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.close(True)
		unload_modules(__name__)
	

class EG_PrzegladaczAddonow(EG_InternetAddons):
	__module__ = __name__
	def getMenuFile(self, url):
		#inputUrl = ('http://egami-image.com.com/image-feed/enigma2/catalog_enigma2.xml')
		inputUrl = url
		xmlFile = os.popen((('wget -q ' + inputUrl) + ' -O-')).read()
		mdom = xml.dom.minidom.parseString(xmlFile)
		return mdom

	def __init__(self, session, url):
		try:
			#self.root_url = ('http://egami-image.com.com/image-feed/enigma2/catalog_enigma2.xml')
			self.root_url = url
			mdom = self.getMenuFile(self.root_url)
			node = mdom.childNodes[0]
			child = mdom.childNodes[0].childNodes
			EG_InternetAddons.__init__(self, session, mdom.childNodes[0], mdom.childNodes[0].childNodes, url)
		except:
			tracefp = StringIO.StringIO()
			traceback.print_exc(file=tracefp)
			message = tracefp.getvalue()
			EG_InternetAddons.__init__(self, session, None, None, None)
            
            
class EGAddonRemove(Screen):
	__module__ = __name__
	def __init__(self, session):
		self.skin = EGAddonRemove_Skin
		Screen.__init__(self, session)
		
		self['status'] = Label(_('Please, choose addon to remove:'))
		self['key_red'] = Label(_('Remove'))
		
		self.mlist = []
		
		self['remove'] = MenuList(self.mlist)
		
		self['actions'] = ActionMap(['ColorActions', 'WizardActions',
		'DirectionActions'], {'ok': self.askRemoveIPK,
		'red' : self.askRemoveIPK,
		'back': self.closeAndReload}, -1)
		
		self.populateSL()
		
	def refr_sel(self):
		self['remove'].moveToIndex(1)
		self['remove'].moveToIndex(0)

	def closeAndReload(self):
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.close()
		unload_modules(__name__)
		
	def populateSL(self):
		self.mlist = []
		myscripts = os.listdir('/usr/uninstall')
		for fil in myscripts:
		    if ((fil.endswith('.del')) and (fil.startswith('Remove'))):
			fil2 = fil[6:-4]
			self.mlist.append(fil2)
		    elif ((fil.endswith('.del')) and not(fil.startswith('Remove'))):
			fil2 = fil[0:-4]
			self.mlist.append(fil2)                
		self['remove'].setList(self.mlist)
	    
	def askRemoveIPK(self):
		try:
			ipkName = self['remove'].getCurrent()
			removeBox = self.session.openWithCallback(self.removeIPK, MessageBox, _((('Do really want to remove ' + ipkName) + '?')), MessageBox.TYPE_YESNO)
			removeBox.setTitle(_('Package Removing...'))
			return None
		except:
			return None

	def removeIPK(self, yesno):
		if yesno:
			mysel = self['remove'].getCurrent()
			mysel2 = (('/usr/uninstall/' + mysel) + '.del')
			if fileExists(mysel2):
				os.system('chmod 777 ' +mysel2)
				os.system(mysel2)
			else:
				mysel2 = (('/usr/uninstall/Remove' + mysel) + '.del')
				os.system('chmod 777 ' +mysel2)
				os.system(mysel2)
			infoBox = self.session.open(MessageBox, (_('Addon removed!')), MessageBox.TYPE_INFO)
			infoBox.setTitle(_(('Remove Package')))
			plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
			self.populateSL()
		else:
			infoBox = self.session.open(MessageBox, (_('Addon NOT removed!')), MessageBox.TYPE_INFO)
			infoBox.setTitle(_(('Remove Package')))
            
   
class EG_Manual_installation(Screen):
	def __init__(self, session, args = None):
		self.skin = EG_Manual_installation_Skin
		Screen.__init__(self, session)
			
		self["listaaddonow"] = FileList('/tmp/', showDirectories=False, showFiles=True, matchingPattern='(?i)^.*\\.(ipk|tar.gz|tar.bz2)', isTop=False)
		self.addony = self["listaaddonow"]
		
		self['status'] = Label(_('Please, choose addon to install:'))
		self['key_red'] = Label(_('Install'))
		
        	self['actions'] = ActionMap(['ColorActions', 'WizardActions',
         	'DirectionActions'], {'ok': self.start,
         	'red': self.start,
         	'back': self.closeAndReload}, -1)
	
	def start(self):
		self.installItem = self['listaaddonow'].getFilename()
		try:
			if self["listaaddonow"].canDescent():
			    self["listaaddonow"].descent()
			else:
			    message = str((('Install ' + self.installItem) + '?'))              	
			    if self.installItem.endswith('.ipk'):
				installBox = self.session.openWithCallback(self.installIPK, MessageBox, _(message), MessageBox.TYPE_YESNO)
				installBox.setTitle(_('Install IPK'))
			    elif self.installItem.endswith('tar.gz'):
				installBox = self.session.openWithCallback(self.installTarGz, MessageBox, _(message), MessageBox.TYPE_YESNO)
				installBox.setTitle(_('Install Tar-ball'))
			    elif self.installItem.endswith('tar.bz2'):
				installBox = self.session.openWithCallback(self.installTarBz2, MessageBox, _(message), MessageBox.TYPE_YESNO)
				installBox.setTitle(_('Install Tar-ball'))
		except:
		    print "no file to install"
            
			
	def installIPK(self, yesno):
        	if yesno:
			os.system(('ipkg -force-overwrite install /tmp/' + self.installItem))
            		resultFile = os.popen(('ipkg -force-overwrite install /tmp/' + self.installItem))
			odinstalacyjnyPlik(resultFile, self.installItem)
            		infoBox = self.session.open(MessageBox, _('Addon installed!'), MessageBox.TYPE_INFO)
            		infoBox.setTitle(_('Addon installed sucessfully!'))
			os.system("rm -rf /tmp/*.ipk")
        	else:
            		infoBox = self.session.open(MessageBox, _('Addon NOT installed!'), MessageBox.TYPE_INFO)
            		infoBox.setTitle(_('Addon is not compatiable!'))
			os.system("rm -rf /tmp/*.ipk")
			
	def installTarGz(self, yesno):
		if yesno:
		    resultFile = os.popen(('cd /; tar -xz -f /tmp/' + self.installItem +';chmod 755 /tmp/egami_e2_installer.sh; /tmp/egami_e2_installer.sh; rm /tmp/egami_e2_installer.sh'))
		    infoBox = self.session.open(MessageBox, _('Package installed!'), MessageBox.TYPE_INFO)
		    infoBox.setTitle(_('Addon installed sucessfully!'))
		else:
		    infoBox = self.session.open(MessageBox, _('Package NOT installed!'), MessageBox.TYPE_INFO)
		    infoBox.setTitle(_('Addon is not compatiable!'))



	def installTarBz2(self, yesno):
		if yesno:
		    resultFile = os.popen(('cd /; tar -xj -f /tmp/' + self.installItem +';;chmod 755 /tmp/egami_e2_installer.sh; /tmp/egami_e2_installer.sh; rm /tmp/egami_e2_installer.sh'))
		    infoBox = self.session.open(MessageBox, _('Package installed!'), MessageBox.TYPE_INFO)
		    infoBox.setTitle(_('Addon installed sucessfully!'))
		else:
		    infoBox = self.session.open(MessageBox, _('Package NOT installed!'), MessageBox.TYPE_INFO)
		    infoBox.setTitle(_('Addon is not compatiable!'))
            
	def closeAndReload(self):
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.close()
		unload_modules(__name__)



class EGAddonMenu(Screen):
	def __init__(self, session):
	    self.skin = EGAddonMenu_Skin
	    Screen.__init__(self, session)
	    self.list = []
	    self["list"] = List(self.list)
	    self.updateList()
	    self["actions"] = ActionMap(["WizardActions", "ColorActions"], {"ok": self.KeyOk, "back": self.close})
	    
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		self.sel = self.sel[2]
		if (self.sel == 0):
			self.session.open(EG_PrzegladaczAddonow, "http://egami-image.com/image-feed/enigma2/catalog_enigma2.xml")
		elif (self.sel == 1):
			self.session.open(PluginDownloadBrowser, 0)
		elif (self.sel == 2):
			if fileExists('/etc/user_addon.txt'):
				urlfile = file('/etc/user_addon.txt', 'r')
				linieurl = urlfile.read()
				urlfile.close()
				self.session.open(EG_PrzegladaczAddonow, linieurl)
			else:
				plik = "There is no user_addon.txt file in /etc with server url!"
				self.session.open(MessageBox, _(plik), MessageBox.TYPE_INFO, timeout=5)			
		elif (self.sel == 3):
			self.session.open(EG_Manual_installation)
		elif (self.sel == 4):
			self.session.open(PluginDownloadBrowser, 1)
		elif (self.sel == 5):
			self.session.open(EGAddonRemove)
		elif (self.sel == 6):
			self.session.openWithCallback(self.runUpgrade, MessageBox, _("Do you want to update your EGAMI image?")+"\n"+_("\nAfter pressing OK, please wait!"))

		else:
			pass

	def noYet(self):
		nobox = self.session.open(MessageBox, "Function Not Yet Available", MessageBox.TYPE_INFO)
		nobox.setTitle(_("Info"))

	def runUpgrade(self, result):
		if result:
			from Plugins.SystemPlugins.SoftwareManager.plugin import UpdatePlugin
			self.session.open(UpdatePlugin, "/usr/lib/enigma2/python/Plugins/SystemPlugins/SoftwareManager")

	def updateList(self):
		self.list = []

		mypath = resolveFilename(SCOPE_CURRENT_SKIN)
		if not fileExists(mypath + "egami_icons"):
		    mypath = "/usr/share/enigma2/skin_default/"
		  
		mypixmap = (mypath + "egami_icons/addon_download.png")
		png = LoadPixmap(mypixmap)
		name = (_("Download EGAMI Addons"))
		desc = (_("Download iptv, softcams..."))
		idx = 0
		res = (name,png,idx,desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/addon_download.png")
		png = LoadPixmap(mypixmap)
		name = (_("Download Plugins"))
		desc = (_("Download plugins, skins, drivers, picons..."))
		idx = 1
		res = (name,png,idx, desc)
		self.list.append(res)

		mypixmap = (mypath + "egami_icons/addon_remove2.png")
		png = LoadPixmap(mypixmap)
		name = (_("----------------------------------------"))
		desc = (_("  "))
		idx = 66
		res = (name,png,idx, desc)
		self.list.append(res)
		
		self["list"].list = self.list
		mypixmap = (mypath + "egami_icons/addon_cvs.png")
		png = LoadPixmap(mypixmap)
		name = (_("User Server Addons"))
		desc = (_("Download User addons from url..."))
		idx = 2
		res = (name,png,idx, desc)
		self.list.append(res)
	  
		mypixmap = (mypath + "egami_icons/addon_cvs.png")
		png = LoadPixmap(mypixmap)
		name = (_("Manual Install EGAMI and IPK packages"))
		desc = (_("Install packages from /tmp ..."))
		idx = 3
		res = (name,png,idx, desc)
		self.list.append(res)


		mypixmap = (mypath + "egami_icons/addon_remove2.png")
		png = LoadPixmap(mypixmap)
		name = (_("----------------------------------------"))
		desc = (_("  "))
		idx = 66
		res = (name,png,idx, desc)
		self.list.append(res)
		
		
		mypixmap = (mypath + "egami_icons/addon_remove.png")
		png = LoadPixmap(mypixmap)
		name = (_("Remove Plugins"))
		desc = (_("Remove plugins, skins, drivers, picons..."))
		idx = 4
		res = (name,png,idx, desc)
		self.list.append(res)
		
		mypixmap = (mypath + "egami_icons/addon_remove.png")
		png = LoadPixmap(mypixmap)
		name = (_("Remove EGAMI addons"))
		desc = (_("Remove installed egami packages..."))
		idx = 5
		res = (name,png,idx, desc)
		self.list.append(res)
		

		mypixmap = (mypath + "egami_icons/addon_remove2.png")
		png = LoadPixmap(mypixmap)
		name = (_("----------------------------------------"))
		desc = (_("  "))
		idx = 66
		res = (name,png,idx, desc)
		self.list.append(res)
				
		mypixmap = (mypath + "egami_icons/addon_remove.png")
		png = LoadPixmap(mypixmap)
		name = (_("Update Your EGAMI now !"))
		desc = (_("Software update..."))
		idx = 6
		res = (name,png,idx, desc)
		self.list.append(res)
		
		self["list"].list = self.list