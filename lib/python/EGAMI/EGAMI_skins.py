# -*- coding: utf-8 -*-

# EG Addon Menu
EGAddonMenu_Skin = """
		<screen name="EGAddonMenu" title="EGAMI Addon Management" position="center,center" size="620,550" >
			<widget source="list" render="Listbox" position="10,0" size="610,420" scrollbarMode="showOnDemand" >
				<convert type="TemplatedMultiContent">
				{"template": [
				MultiContentEntryText(pos = (90, 0), size = (690, 30), font=0, text = 0),
				MultiContentEntryPixmapAlphaTest(pos = (10, 10), size = (80, 80), png = 1),
				MultiContentEntryText(pos = (90, 30), size = (670, 50), font=1, flags = RT_VALIGN_TOP, text = 3),
				],
				"fonts": [gFont("Regular", 24),gFont("Regular", 16)],
				"itemHeight": 65
				}
				</convert>
			</widget>
		</screen>"""
		
#EG Addon Informations Window
EGAddonInfo_Skin = """
		<screen name="EGAddonInfo" position="center,center" size="820,550" title="EGAMI Addon Informations">
			<widget name="image" position="10,10" size="800,420" alphatest="on" />
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,385" size="800,4"/>
			<widget name="text" position="10,400" size="800,160" font="Regular;20" />
		</screen>"""

# EG Addon Internet Downloads Window
EG_InternetAddons_Skin = """
		<screen name="EG_InternetAddons" position="center,center" size="620,550" title="EGAMI Management Addons - Internet Addons" >
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,45" size="800,4"/>
			<widget name="menu" position="10,60" size="610,420" scrollbarMode="showOnDemand"/>
			<widget name="status" position="30,10" size="400,25" font="Regular;21" valign="center" halign="center"/>
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,485" size="800,4"/>
			<ePixmap position="30,509" zPosition="0" size="35,25" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_red" position="65,509" size="200,25" font="Regular;18"/>
			<ePixmap position="430,509" zPosition="0" size="35,25" pixmap="skin_default/egami_icons/buttons/button_blue.png" transparent="1" alphatest="on" />
			<widget name="key_blue" position="470,509" size="200,25" font="Regular;20" />
		</screen>"""
		
# EG Addon Remove Window
EGAddonRemove_Skin = """
		<screen name="EGAddonRemove" position="center,center" size="620,550" title="EGAMI Management Addons - Remove Addon" >
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,45" size="800,4"/>
			<widget name="remove" position="10,60" size="610,420" scrollbarMode="showOnDemand"/>
			<widget name="status" position="30,10" size="400,25" font="Regular;21" valign="center" halign="center"/>
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,485" size="800,4"/>
			<ePixmap position="30,509" zPosition="0" size="35,25" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_red" position="65,509" size="200,25" font="Regular;18"/>
		</screen>"""

# EG Addon Management Window
AddonManager_Skin = """
		<screen name="AddonManager" position="center,center" size="360,270" title="EGAMI Management Addons" >
			<widget name="menu" position="10,10" size="340,220" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="skin_default/egami_icons/div-h.png" position="10,70" size="340,4"/>
			<ePixmap pixmap="skin_default/egami_icons/div-h.png" position="10,120" size="340,4"/>
		</screen>"""

# EG Addon Manual Installation Window
EG_Manual_installation_Skin = """
		<screen name="EG_Manual_installation" position="center,center" size="620,550" title="EGAMI Management Addons - Manual Install" >
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,45" size="800,4"/>
			<widget name="listaaddonow" position="10,60" size="610,420" scrollbarMode="showOnDemand"/>
			<widget name="status" position="30,10" size="400,25" font="Regular;21" valign="center" halign="center"/>
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,485" size="800,4"/>
			<ePixmap position="30,509" zPosition="0" size="35,25" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_red" position="65,509" size="200,25" font="Regular;18"/>
		</screen>"""
		
		
#EG Extras Menu 
EGExtrasMenu_Skin = """
		  <screen name="EGExtrasMenu" title="EGAMI Extras Panel" position="center,center" size="620,550" >
			  <widget source="list" render="Listbox" position="10,0" size="610,540" scrollbarMode="showOnDemand" >
				  <convert type="TemplatedMultiContent">
				  {"template": [
				  MultiContentEntryText(pos = (90, 0), size = (510, 30), font=0, text = 0),
				  MultiContentEntryPixmapAlphaTest(pos = (10, 10), size = (80, 80), png = 1),
				  MultiContentEntryText(pos = (90, 30), size = (510, 30), font=1, flags = RT_VALIGN_TOP, text = 3),
				  ],
				  "fonts": [gFont("Regular", 24),gFont("Regular", 16)],
				  "itemHeight": 60
				  }
				  </convert>
			  </widget>
		  </screen>"""
		  
# EG Swap Manager
EGSwapManager_Skin = """
		   <screen name="EGSwapManager" position="center,center" size="570,350" title="EGAMI Swap File Manager" >
			      <widget name="config" position="10,10" size="540,180" scrollbarMode="showOnDemand" />
			      <widget name="state" position="70,220" size="430,75" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		</screen>"""
		
        		
#EG Devices Manager
EGDeviceManager_Skin = """
		      <screen name="EGDeviceManager" position="center,center" size="800,560" title="EGAMI Devices Manager">
			      <widget source="list" render="Listbox" position="10,0" size="780,510" scrollbarMode="showOnDemand" >
				      <convert type="TemplatedMultiContent">
				      {"template": [
				      MultiContentEntryText(pos = (90, 0), size = (690, 30), font=0, text = 0),
				      MultiContentEntryText(pos = (110, 30), size = (670, 50), font=1, flags = RT_VALIGN_TOP, text = 1),
				      MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (80, 80), png = 2),
				      ],
				      "fonts": [gFont("Regular", 24),gFont("Regular", 20)],
				      "itemHeight": 85
				      }
				      </convert>
			      </widget>
			      <widget name="lab1" zPosition="2" position="50,40" size="700,40" font="Regular;24" halign="center" transparent="1"/>
			      <widget name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="40,524" size="140,40" alphatest="on" />
			      <widget name="key_red" position="70,524" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <widget name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="210,524" size="140,40" alphatest="on" />
			      <widget name="key_green" position="240,524" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <widget name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="360,524" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="390,524" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <widget name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="510,524" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="540,524" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
	
#EG Devices Manager Setup
EGDeviceManager_Setup_Skin = """
		  <screen name="EGDeviceManager_Setup" position="center,center" size="902,340" title="EGAMI Devices Manager - Setup">
			  <widget name="config" position="30,10" size="840,275" scrollbarMode="showOnDemand"/>
			  <ePixmap pixmap="skin_default/egami_icons/buttons/button_red.png" position="200,300" size="140,40" alphatest="on"/>
			  <ePixmap pixmap="skin_default/egami_icons/buttons/button_green.png" position="550,300" size="140,40" alphatest="on"/>
			  <widget name="key_red" position="220,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
			  <widget name="key_green" position="570,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
		  </screen>"""

		  
# EG Devices - HDD Setup
EGHDDParm_Skin = """
		<screen name="EGHDDParm" position="center,center" size="520,270" title="EGAMI Hard Drive Setup" >
			<ePixmap name="czerwony" position="20,220" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<ePixmap name="zielony" position="190,220" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
	    		<ePixmap pixmap="skin_default/egami_icons/div-h.png" position="10,160" size="500,4" />
			<widget name="config" position="10,10" size="500,80" scrollbarMode="showOnDemand" />
			<widget name="key_red" position="0,229" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="center" transparent="1"/>
			<widget name="key_green" position="165,229" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="center" transparent="1"/>
			<widget name="status1" position="40,180" size="400,25" font="Regular;20" />
    		</screen>"""

# EG Devices - HDD Info Menu
EGHardDriveInfo_Skin = """
		<screen name="HardDriveInfo" position="center,center" size="380,290" title="EGAMI IDE Drive Info" >
      			<widget name="menu" position="10,10" size="360,200" scrollbarMode="showOnDemand" />
	    		<ePixmap pixmap="skin_default/egami_icons/div-h.png" position="10,46" size="360,4" />
	    		<ePixmap pixmap="skin_default/egami_icons/div-h.png" position="10,121" size="360,4" />
    		</screen>"""

#EG Services Menu 
EGServicesMenu_Skin = """
		  <screen name="EGServicesMenu" title="EGAMI Services Panel" position="center,center" size="620,560" >
			  <widget source="list" render="Listbox" position="10,0" size="610,550" scrollbarMode="showOnDemand">
				  <convert type="TemplatedMultiContent">
				  {"template": [
				  MultiContentEntryText(pos = (90, 0), size = (510, 30), font=0, text = 0),
				  MultiContentEntryPixmapAlphaTest(pos = (10, 10), size = (80, 80), png = 1),
				  MultiContentEntryText(pos = (90, 30), size = (510, 30), font=1, flags = RT_VALIGN_TOP, text = 3),
				  ],
				  "fonts": [gFont("Regular", 24),gFont("Regular", 16)],
				  "itemHeight": 55
				  }
				  </convert>
			  </widget>
		  </screen>"""


#EG Services Cron Manager
EGCronMang_Skin = """
		  <screen name="EGCronMang" position="center,center" size="570,350" title="EGAMI Cron Manager">
			    <widget source="list" render="Listbox" position="10,10" size="550,200" scrollbarMode="showOnDemand" >
				  <convert type="StringList" />
			      </widget>
			      <widget name="state" position="150,250" size="230,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		  </screen>"""

#EG Services Cron Conf Setup
EGSetupCronConf_Skin = """
		  <screen name="EGSetupCronConf" position="center,center" size="570,350" title="EGAMI Cron Setup">
			      <widget name="config" position="10,20" size="550,280" scrollbarMode="showOnDemand" />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
		  </screen>"""

# EG Services Configs - Dropbear
EGDropbearConfig_Skin = """
		      <screen name="EGDropbearConfig" position="center,center" size="570,350" title="EGAMI Dropbear Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
		      
# EG Services Configs - Pcscd
EGPcscdConfig_Skin = """
		      <screen name="EGPcscdConfig" position="center,center" size="570,350" title="EGAMI Pcscd Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
		      
# EG Services Configs - Samba
EGSambaConfig_Skin = """
		      <screen name="EGSambaConfig" position="center,center" size="570,350" title="EGAMI Samba Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""

# EG Services Configs - Telnet
EGTelnetConfig_Skin = """
		      <screen name="EGTelnetConfig" position="center,center" size="570,350" title="EGAMI Telnet Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
		      
# EG Services Configs - Ftp
EGFtpConfig_Skin = """
		      <screen name="EGFtpConfig" position="center,center" size="570,350" title="EGAMI FTP Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
		      
# EG Services Configs - OpenVPN
EGOpenVPNConfig_Skin = """
		      <screen name="EGOpenVPNConfig" position="center,center" size="570,350" title="EGAMI OpenVPN Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
		      
# EG Services Configs - DjMount
EGDjMountConfig_Skin = """
		<screen name="EGDjMountConfig" position="center,center" size="570,350" title="EGAMI DjMount Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""
# EG Services Configs Root - DjMount
EGDjMountConfigRoot_Skin = """
		<screen name="EGDjMountConfigRoot" position="center,center" size="540,460" >
			<widget name="text" position="0,2" size="540,22" font="Regular;22" />
			<widget name="target" position="0,23" size="540,22" valign="center" font="Regular;22" />
			<widget name="filelist" position="0,55" zPosition="1" size="540,210" scrollbarMode="showOnDemand" selectionDisabled="1" />
			<widget name="red" position="0,415" zPosition="1" size="135,40" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_red" position="0,415" zPosition="2" size="135,40" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />	
			<widget name="green" position="135,415" zPosition="1" size="135,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
			<widget name="key_green" position="135,415" zPosition="2" size="135,40" halign="center" valign="center" font="Regular;22" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		</screen>"""
		
# EG Services Configs - uShare
EGUShareConfig_Skin = """
		      <screen name="EGUShareConfig" position="center,center" size="570,350" title="EGAMI uShare Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		      </screen>"""

# EG Services Configs - Sys/Kernel LogD
EGSyslogDConfig_Skin = """
		    <screen name="EGSyslogDConfig" position="center,center" size="570,450" title="EGAMI Syslogd and Klogd Setup" >
			      <widget name="config" position="10,10" size="550,330" scrollbarMode="showOnDemand" />
			      <widget name="state" position="100,360" size="370,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,420" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,420" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,420" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,420" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,420" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,420" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,420" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,420" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		    </screen>"""

# EG Services HTTPD Setup
EGHttpd_Skin = """
		    <screen name="EGHttpd" position="center,center" size="570,350" title="EGAMI HTTPD Server Setup" >
			      <widget name="config" position="10,10" size="550,220" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,245" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		    </screen>"""

# EG Services Inadyn Setup
EGInadyn_Skin = """
		    <screen name="EGInadyn" position="center,center" size="570,370" title="EGAMI Inadyn - dynamic DNS Client" >
			      <widget name="config" position="10,10" size="550,260" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,280" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,340" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,340" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,340" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,340" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,340" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,340" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,340" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,340" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
		    </screen>"""
		

# EG Services NFS Setup
EGNfsServer_Skin = """
		   <screen name="EGNfsServer" position="center,center" size="570,350" title="EGAMI NFS Server Setup" >
			      <widget name="config" position="10,10" size="550,200" scrollbarMode="showOnDemand" />
			      <widget name="state" position="120,240" size="300,25" font="Regular;20" halign="center" noWrap="1" backgroundColor="red" foregroundColor="white" shadowOffset="-2,-2" shadowColor="black"  />
			      <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="10,320" size="140,40" alphatest="on" />
			      <widget name="key_red" position="40,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="150,320" size="140,40" alphatest="on" />
			      <widget name="key_green" position="180,320" zPosition="1" size="200,40" font="Regular;20" halign="left" valign="top" backgroundColor="#9f1313" transparent="1" />
			      <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="300,320" size="140,40" alphatest="on" />
			      <widget name="key_yellow" position="330,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			      <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="450,320" size="140,40" alphatest="on" />
			      <widget name="key_blue" position="480,320" zPosition="1" size="140,40" font="Regular;20" halign="left" valign="top" backgroundColor="#a08500" transparent="1" />
			</screen>"""


# EG EmuManager
EGEmuManager_Skin = """
		<screen name="EmuManager" position="center,center" size="780,550" title="EGAMI Blue Panel">
			<widget name="choose_cam" position="180,10" size="280,30" font="Regular;22" />
			<widget name="config" position="410,10" size="180,30" transparent="1" />
			<ePixmap pixmap="skin_default/egami_icons/default_cam.png" position="380,8" size="800,60" transparent="1" alphatest="on"/>
			<widget name="lb_provider" position="180,75" size="280,20" font="Regular;18" />
			<widget name="lb_channel" position="180,95" size="280,20" font="Regular;18" />
			<widget name="lb_aspectratio" position="180,115" size="280,20" font="Regular;18" />
			<widget name="lb_videosize" position="180,135" size="280,20" font="Regular;18" />
			<widget name="ecminfo" position="180,215" size="400,290" font="Regular;18" />
	    		<ePixmap pixmap="skin_default/egami_icons/div-h.png" position="10,483" size="800,4" />
	    		<ePixmap pixmap="skin_default/egami_icons/dish_scan.png" zPosition="0" position="30,55" size="200,200" transparent="1" alphatest="on"/>
	    		<ePixmap pixmap="skin_default/egami_icons/icon_camd.png" zPosition="0" position="20,225" size="200,200" transparent="1" alphatest="on" />
			<ePixmap position="40,504" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on"/>
			<ePixmap position="200,504" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on"/>
			<ePixmap position="360,504" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_yellow.png" transparent="1" alphatest="on"/>
			<ePixmap position="550,504" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_blue.png" transparent="1" alphatest="on"/>
			<widget name="key_red" position="60,504" zPosition="1" size="170,25" font="Regular;20" valign="top" halign="left" backgroundColor="red" transparent="1" />
			<widget name="key_green" position="220,504" zPosition="1" size="170,25" font="Regular;20" valign="top" halign="left" backgroundColor="green" transparent="1" />
			<widget name="key_yellow" position="380,504" zPosition="1" size="170,25" font="Regular;20" valign="top" halign="left" backgroundColor="yellow" transparent="1" />
			<widget name="key_blue" position="570,504" zPosition="1" size="170,25" font="Regular;20" valign="top" halign="left" backgroundColor="blue" transparent="1" />
		</screen>"""
# EG EmuManager - Starting
EGEmuManagerStarting_Skin = """
		<screen name="EGEmuManagerStarting" position="390,100" size="484,250" title="EGAMI" flags="wfNoBorder">
		    <widget name="starting" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/egami_icons/startcam_1.png,egami_icons/startcam_2.png,egami_icons/startcam_3.png,egami_icons/startcam_4.png,egami_icons/startcam_5.png,egami_icons/startcam_6.png,egami_icons/startcam_7.png,egami_icons/startcam_8.png,egami_icons/startcam_9.png,egami_icons/startcam_10.png,egami_icons/startcam_11.png" transparent="1" />
		    <widget name="text" position="10,180" halign="center" size="460,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />
		  </screen>"""
# EG EmuInfo Menu
EGEmuInfoScript_Skin = """
		<screen name="EGEmuInfoScript" position="center,center" size="560,405" title="EGAMI EmuInfo Tool" >
			<widget name="list" position="10,10" size="540,280" scrollbarMode="showOnDemand" />
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,290" size="540,4"/>
			<widget name="statuslab" position="10,295" size="540,30" font="Regular;16" valign="center" noWrap="1" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		</screen>"""

# EG Decoding Setup
EGDecodingSetup_Skin = """
		<screen name="EGDecodingSetup" position="center,center" size="670,250" title="EGAMI Decoding Setup" >
      			<widget name="config" position="10,10" size="650,180" scrollbarMode="showOnDemand" />
			<widget name="key_red" position="50,220" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_red_png" position="20,220" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_green" position="310,220" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_green_png" position="280,220" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
		</screen>"""


# EG Advanced Stream informations
EGAdvancedStreamInfo_Skin = """
		<screen name="DvbSnoop" position="center,center" size="380,310" title="EGAMI Stream Informations" >
      			<widget name="menu" position="10,10" size="360,280" scrollbarMode="showOnDemand" />
		</screen>"""


# EG Infobar Setup
EGInfoBarSetup_Skin = """
		<screen name="EGInfoBarSetup" position="center,center" size="670,550" title="EGAMI Infobar Setup" >
      			<widget name="config" position="10,10" size="650,480" scrollbarMode="showOnDemand" />
			<widget name="key_red" position="50,520" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_red_png" position="20,520" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_green" position="310,520" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_green_png" position="280,520" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
		</screen>"""

# EG Kernel Modules Menu
EGKernelModulesManager_Skin = """
		<screen name="EGKernelModulesManager" position="center,center" size="670,550" title="EGAMI Kernel Modules Manager" >
      			<widget name="config" position="10,10" size="650,480" scrollbarMode="showOnDemand" />
			<widget name="key_red" position="50,520" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_red_png" position="20,520" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_green" position="310,520" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_green_png" position="280,520" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
		</screen>"""

# EG Mount Edit Menu
EGMountEdit_Skin = """
		<screen name="MountEdit" position="center,center" size="500,280" title="Mount editor">
			<widget name="config" position="10,10" size="480,175" scrollbarMode="showOnDemand" />
		</screen>"""

# EG Mount Manager Menu
EGMountManager_Skin = """
		<screen name="MountManager" position="center,center" size="420,300" title="Mount Manager">
			<ePixmap name="greenbutton" position="0,0" zPosition="1" size="140,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
			<ePixmap name="yellowbutton" position="140,0" zPosition="1" size="140,40" pixmap="skin_default/egami_icons/buttons/button_yellow.png" transparent="1" alphatest="on" />
			<ePixmap name="bluebutton" position="280,0" zPosition="1" size="140,40" pixmap="skin_default/egami_icons/buttons/button_blue.png" transparent="1" alphatest="on" />
			<widget name="green" position="0,9" zPosition="2" size="140,40" font="Regular;20" valign="top" halign="center" transparent="1" />
			<widget name="yellow" position="140,9" zPosition="2" size="140,40" font="Regular;20" valign="top" halign="center" transparent="1" />
			<widget name="blue" position="280,9" zPosition="2" size="140,40" font="Regular;20" valign="top" halign="center" transparent="1" />
			<widget name="entries" position="10,50" size="410,175" scrollbarMode="showOnDemand" />
		</screen>"""


# EG SmartScript Menu
EGSmartScript_Skin = """
		<screen name="SmartScript" position="center,center" size="560,405" title="EGAMI SmartScript Tool" >
			<widget name="list" position="10,10" size="540,280" scrollbarMode="showOnDemand" />
			<ePixmap name="border" pixmap="skin_default/egami_icons/div-h.png" position="10,365" size="540,4"/>
			<widget name="statuslab" position="10,370" size="540,30" font="Regular;16" valign="center" noWrap="1" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		</screen>"""


# EG Process info
EGProcessInfo_Skin = """
		<screen name="EGProcessInfo" position="center,center" size="670,550" title="EGAMI Process Informations" >
      			<widget name="menu" position="10,10" size="650,480" scrollbarMode="showOnDemand" />
			<widget name="key_red" position="50,520" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_red_png" position="20,520" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on" />
			<widget name="key_green" position="310,520" zPosition="2" size="200,20" font="Regular;20" valign="top" halign="left" transparent="1"/>
			<ePixmap name="key_green_png" position="280,520" zPosition="1" size="200,40" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on" />
    		</screen>"""

# EG Kernel info
EGKernelInfo_Skin = """
		<screen name="EGKernelInfo" position="center,center" size="670,550" title="EGAMI Kernel Informations" >
			<widget name="menu" position="10,10" size="650,530" scrollbarMode="showOnDemand" />
    		</screen>"""
    		
# EG Enigma2 info
EGEnigma2ConfigInfo_Skin = """
		<screen name="EGEnigma2ConfigInfo" position="center,center" size="670,550" title="EGAMI Enigma2 Config" >
			<widget name="menu" position="10,10" size="650,530" scrollbarMode="showOnDemand" />
    		</screen>"""
    		
# EG PermanentClock
EGPermanentClock_Skin = """
    		<screen name="EGPermanentClock" position="610,30" size="60,24" flags="wfNoBorder" title="EGAMI Permanent Clock" backgroundColor="#55000000" >
        		<widget source="global.CurrentTime" render="Label" position="0,0" size="60,24" font="LCD;24" foregroundColor="#d0d0d0" valign="center" halign="center" transparent="1" >
            			<convert type="ClockToText">Default</convert>
        		</widget>
   		</screen>"""
   		
# EGExecute
EGExecute_Skin = """
	<screen name="EGExecute" position="center,center" size="876,475">
		<widget name="linelist" position="5,5" size="750,470" />
	</screen>"""

			
# EGAMI FileManager - Configuration
EGFileManagerConfig_Skin ="""
        		<screen name="EGFileManagerConfig" position="center,center" size="650,400" title="EGAMI File Manager - Configuration" >
            			<widget name="config" position="0,0" size="640,360" scrollbarMode="showOnDemand" />
            			<widget name="buttonred" position="120,360" size="100,40" zPosition="1"  transparent="1" foregroundColor="white" font="Regular;18"/>
            			<widget name="buttongreen" position="380,360" size="100,40" zPosition="1"  transparent="1" foregroundColor="white" font="Regular;18"/>
            			<ePixmap position="100,358" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="on"/>
            			<ePixmap position="360,358" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on"/>
        		</screen>"""

# EGAMI FileManager - Main Window
EGFileManager_Skin = """
        		<screen name="EGFileManager" position="center,center" size="935,590" title="EGAMI File Manager">
				<widget name="list_left_text" font="Regular;20" position="60,0" size="150,30"/>
				<widget name="list_right_text" font="Regular;20" position="575,0" size="150,30"/>
            			<widget name="list_left" position="0,30" size="460,480" scrollbarMode="showOnDemand" />
            			<widget name="list_right" position="465,30" size="460,480" scrollbarMode="showOnDemand" />
            			<ePixmap position="20,545" size="80,80" zPosition="1" pixmap="skin_default/egami_icons/buttons/button_red.png" transparent="1" alphatest="blend" />
            			<widget name="copy_text" zPosition="4" position="50,545" size="140,40" halign="left" valign="top" font="Regular;22" transparent="1" />
            			<ePixmap position="160,545" size="80,80" zPosition="1" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="blend" />
				<widget name="remove_text" zPosition="4" position="190,545" size="140,40" halign="left" valign="top" font="Regular;22" transparent="1" />
				<ePixmap position="320,545" size="80,80" zPosition="1" pixmap="skin_default/egami_icons/buttons/button_yellow.png" transparent="1" alphatest="blend" />
				<widget name="move_text" zPosition="4" position="350,545" size="140,40" halign="left" valign="top" font="Regular;22" transparent="1" />
				<ePixmap position="470,545" size="80,80" zPosition="1" pixmap="skin_default/egami_icons/buttons/button_blue.png" transparent="1" alphatest="blend" />
				<widget name="more_text" zPosition="4" position="500,545" size="240,40" halign="left" valign="top" font="Regular;22" transparent="1"  />
				<ePixmap position="740,545" size="80,80" zPosition="1" pixmap="skin_default/egami_icons/buttons/key_menu.png" transparent="1" alphatest="blend" />
				<widget name="settings_text" zPosition="4" position="790,545" size="240,40" halign="left" valign="top" font="Regular;22" transparent="1" />
        		</screen>"""

# EGAMI FileManager - More Options
EGFileManager_InfoMenu_Skin = """
           		<screen name="EGFileManager_InfoMenu" position="center,center" size="450,260" title="EGAMI File Manager - More Options" >
           			<widget name="menu" position="10,10" size="440,250" scrollbarMode="showOnDemand" />
           		</screen>"""
           		
# EGAMI FileManager - File Viewer	   
EGFileViewer_Skin = """
        		<screen position="center,center" size="650,500" title="EGAMI File Manager - Viewer" >
            			<widget name="filedata" position="0,0" size="650,460" font="Regular;16" zPosition="9" transparent="1" />
            			<widget name="status" position="10,360" size="600,40" valign="center" halign="center" zPosition="1"  transparent="1" foregroundColor="white" font="Regular;18"/>
        		</screen>"""

# EGAMI FileManager - Console
EGConsoleView_Skin = """
			<screen name="EGConsoleView" position="center,center" size="620,476" title="EGAMI File Manager - Console" >
            			<widget name="text" position="0,0" size="650,460" font="Regular;16" zPosition="9" transparent="1" />
            			<widget name="status" position="10,460" size="600,40" valign="center" halign="center" zPosition="1"  transparent="1" foregroundColor="white" font="Regular;18"/>
       		  	</screen>"""

# EGAMI FileManager - Picture Viewer
EGPicViewer_Skin="""
			<screen name="EGPicViewer" flags="wfNoBorder" position="0,0" size="1280,720" title="EGAMIPicViewer" backgroundColor="#00121214">
					<widget name="Picture" position="0,0" size="1280,720" zPosition="1" alphatest="on" />
			</screen>"""
			
# EGAMI FileManager - New SymLink
EGFileManager_symlink_create_Skin = """
        		<screen name="EGFileManager_symlink_create" position="center,center" size="550,400" title="EGAMI File Manager - New Symlink" >
            			<widget name="config" position="0,0" size="550,360" scrollbarMode="showOnDemand" />
            			<widget name="buttongreen" position="120,360" size="100,40" valign="center" halign="center" zPosition="1"  transparent="1" foregroundColor="white" font="Regular;18"/>
            			<ePixmap position="120,360" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on"/>
        		</screen>"""
			
# EGAMI FileManager - File Permissions
EGFileManager_file_permision_Skin = """
        		<screen name="EGFileManager_file_permision" position="center,center" size="550,400" title="EGAMI File Manager - File permission settings" >
            			<widget name="config" position="0,0" size="550,360" scrollbarMode="showOnDemand" />
            			<widget name="buttongreen" position="120,360" size="100,40" valign="center" halign="center" zPosition="1"  transparent="1" foregroundColor="white" font="Regular;18"/>
            			<ePixmap position="120,360" size="100,40" zPosition="0" pixmap="skin_default/egami_icons/buttons/button_green.png" transparent="1" alphatest="on"/>
        		</screen>"""

    		
#EG Green Panel 
EGGreenPanel_Skin = """
		  <screen name="EGGreenPanel" position="center,center" size="700,560" title="EGAMI Green Panel" >
			  <eLabel text="Addons" zPosition="4" position="50,520" size="140,40" halign="left" font="Regular;22" transparent="1" />
			  <eLabel text="Extras" zPosition="4" position="230,520" size="140,40" halign="left" font="Regular;22" transparent="1" />
			  <eLabel text="File Mode" zPosition="4" position="400,520" size="140,40" halign="left" font="Regular;22" transparent="1" />
			  <eLabel text="Scripts" zPosition="4" position="580,520" size="140,40" halign="left" font="Regular;22" transparent="1"  />
			  <ePixmap name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="20,520" size="140,40" alphatest="on" />
			  <ePixmap name="key_green_png" pixmap="skin_default/egami_icons/buttons/button_green.png" position="200,520" size="140,40" alphatest="on" />
			  <ePixmap name="key_yellow_png" pixmap="skin_default/egami_icons/buttons/button_yellow.png" position="370,520" size="140,40" alphatest="on" />
			  <ePixmap name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="550,520" size="140,40" alphatest="on" />
			  <widget source="list" render="Listbox" position="10,0" size="680,510" zPosition="2" scrollbarMode="showOnDemand" transparent="1">
				<convert type="TemplatedMultiContent">
				    {"template": [
				    MultiContentEntryText(pos = (125, 0), size = (650, 24), font=0, text = 0),
				    MultiContentEntryText(pos = (125, 24), size = (650, 24), font=1, text = 1),
				    MultiContentEntryPixmapAlphaTest(pos = (6, 5), size = (100, 40), png = 2),
				    ],
				    "fonts": [gFont("Regular", 24),gFont("Regular", 20)],
				    "itemHeight": 50
				    }
				</convert>
			  </widget>
		  </screen>"""



#EG Wifi & USB dongles Panel
EGUsbWifiTuner_Skin = """
		      <screen name="EGUsbWifiTuner" position="center,center" size="800,560" title="EGAMI Wifi and USB Tuners Dongles Setup">
			      <widget source="menu" render="Listbox" position="10,0" size="780,510" scrollbarMode="showOnDemand" >
				      <convert type="TemplatedMultiContent">
				      {"template": [
				      MultiContentEntryPixmapAlphaTest(pos = (10, 10), size = (80, 80), png = 0),
				      MultiContentEntryText(pos = (90, 0), size = (790, 30), font=0, text = 1),
				      MultiContentEntryText(pos = (110, 30), size = (790, 50), font=1, flags = RT_VALIGN_TOP, text = 2),
				      MultiContentEntryText(pos = (110, 60), size = (790, 50), font=1, flags = RT_VALIGN_TOP, text = 3),
				      ],
				      "fonts": [gFont("Regular", 24),gFont("Regular", 20)],
				      "itemHeight": 95
				      }
				      </convert>
			      </widget>
			      <widget name="key_red_png" pixmap="skin_default/egami_icons/buttons/button_red.png" position="60,524" size="140,40" alphatest="on" />
			      <widget name="key_blue_png" pixmap="skin_default/egami_icons/buttons/button_blue.png" position="600,524" size="140,40" alphatest="on" />
			      <widget name="key_red" position="60,520" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			      <widget name="key_blue" position="600,520" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		      </screen>"""

		  

# EG Services Menu - NOT USED ANY MORE !
EGServices_Skin = """
		<screen name="EGServices" position="center,center" size="450,385" title="EGAMI Daemons / Services Manager" >
			<widget source="menu" render="Listbox" position="5,5" size="440,320" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{ "template": [  MultiContentEntryText(pos = (50, 5), size = (355, 30), flags = RT_HALIGN_CENTER, text = 0, border_width=1), 
					MultiContentEntryPixmapAlphaTest(pos = (10, 10), size = (40, 30), png = 1)], "fonts": [gFont("Regular", 20)], "itemHeight": 40 }
				</convert>
			</widget>
			<widget name="key_yellow_big_png" position="20,340" size="200,40" pixmap="skin_default/egami_icons/buttons/button_yellow.png" alphatest="on" />
			<widget name="key_blue_big_png" position="230,340" size="200,40" pixmap="skin_default/egami_icons/buttons/button_blue.png" alphatest="on" />
			<widget name="key_yellow" position="20,340" size="200,40" font="Regular;20" backgroundColor="#a08500" zPosition="2" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
			<widget name="key_blue" position="230,340" size="200,40" font="Regular;20" backgroundColor="#18188b" zPosition="2" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		</screen>"""

# EG BackupPanel 
EGAMIBackupPanel_Skin = """
		<screen name="EGAMIBackupPanel" position="center,center" size="902,380" title="EGAMI Image Backup Panel - STEP 1" >
		      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>
		      <widget name="label2" position="10,80" size="840,290" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>
		      <widget name="label3" position="10,110" size="840,290" zPosition="1" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>
		      <widget name="list" position="10,170" size="840,290" scrollbarMode="showOnDemand"/>
		      <ePixmap pixmap="skin_default/egami_icons/buttons/yellow.png" position="72,290" size="140,40" alphatest="on" />
		      <ePixmap pixmap="skin_default/egami_icons/buttons/blue.png" position="284,290" size="140,40" alphatest="on" />
		      <widget name="key_yellow" position="72,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		      <widget name="key_blue" position="284,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		</screen>"""

# EG BackupPanel_Step2 
EGAMIBackupPanel_Step2_Skin = """
		<screen name="EGAMIBackupPanel_Step2" position="center,center" size="902,380" title="EGAMI Backup Location - STEP 2">
		      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>
		      <widget name="label2" position="10,80" size="840,290" zPosition="1" halign="center" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>
		      <widget name="config" position="130,160" size="450,290" scrollbarMode="showOnDemand"/>
		      <ePixmap pixmap="skin_default/egami_icons/buttons/yellow.png" position="200,340" size="140,40" alphatest="on"/>
		      <ePixmap pixmap="skin_default/egami_icons/buttons/green.png" position="550,340" size="140,40" alphatest="on"/>
		      <widget name="key_yellow" position="200,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		      <widget name="key_green" position="550,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
		</screen>"""	

# EG BackupPanel_Step3
EGAMIBackupPanel_Step3_Skin = """
		<screen name="EGAMIBackupPanel_Step3" position="center,center" size="484,250" title="EGAMI Backup in progress..." flags="wfNoBorder">
		      <widget name="status" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/egami_icons/backup_1.png,egami_icons/backup_2.png,egami_icons/backup_3.png,egami_icons/backup_4.png,egami_icons/backup_5.png,egami_icons/backup_6.png"  />
		      <widget name="label" position="0,200" halign="center" size="484,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />
		</screen>"""
	
EGAMIRestorePanel_Step1_Skin = """	
		<screen name="EGAMIRestorePanel_Step1" position="center,center" size="902,550" title="EGAMI Backup Restore - STEP 1">
		      <widget name="config" position="30,10" size="840,510" scrollbarMode="showOnDemand"/>
		      <ePixmap pixmap="skin_default/egami_icons/buttons/blue.png" position="380,510" size="140,40" alphatest="on"/>
		      <widget name="key_blue" position="380,510" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		      <ePixmap pixmap="skin_default/egami_icons/buttons/green.png" position="550,510" size="140,40" alphatest="on"/>
		      <widget name="key_green" position="550,510" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
		</screen>"""	
		
EGAMIRestorePanel_Step2_Skin = """
	      <screen name="EGAMIRestorePanel_Step2" position="center,center" size="484,250" title="EGAMI Restore in progress..." flags="wfNoBorder">
		    <widget name="status" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/egami_icons/restore_1.png,egami_icons/restore_2.png,egami_icons/restore_3.png,egami_icons/restore_4.png,egami_icons/restore_5.png,egami_icons/restore_6.png"  />
		    <widget name="label" position="0,200" halign="center" size="484,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />
	      </screen>"""
	
	
	