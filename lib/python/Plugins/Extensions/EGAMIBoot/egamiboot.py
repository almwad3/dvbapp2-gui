import sys
import os
import struct

def getKernelVersionString():
	try:
		return open("/proc/version","r").read().split(' ', 4)[2].split('-',2)[0]
	except:
		return _("unknown")

def EgamiBootMainEx(source, target, installsettings):
    egamihome = '/media/egamiboot'
    egamiroot = 'media/egamiboot'
    rc = os.system('init.sysvinit 2')
    cmd = 'showiframe /usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/egamiboot.mvi > /dev/null 2>&1'
    rc = os.system(cmd)
    to = ('/media/egamiboot/EgamiBootI/' + target)
    cmd = ('rm -r %s > /dev/null 2<&1' % to)
    rc = os.system(cmd)
    to = ('/media/egamiboot/EgamiBootI/' + target)
    cmd = ('mkdir %s > /dev/null 2<&1' % to)
    rc = os.system(cmd)
    to = ('/media/egamiboot/EgamiBootI/' + target)
    cmd = ('chmod -R 0777 %s' % to)
    rc = os.system(cmd)
    rc = EgamiBootExtract(source, target)
    cmd = ('mkdir -p %s/EgamiBootI/%s/media > /dev/null 2>&1' % (egamihome,
     target))
    rc = os.system(cmd)
    cmd = ('rm %s/EgamiBootI/%s/%s > /dev/null 2>&1' % (egamihome,
     target,
     egamiroot))
    rc = os.system(cmd)
    cmd = ('rmdir %s/EgamiBootI/%s/%s > /dev/null 2>&1' % (egamihome,
     target,
     egamiroot))
    rc = os.system(cmd)
    cmd = ('mkdir -p %s/EgamiBootI/%s/%s > /dev/null 2>&1' % (egamihome,
     target,
     egamiroot))
    rc = os.system(cmd)
    cmd = ('cp /etc/network/interfaces %s/EgamiBootI/%s/etc/network/interfaces > /dev/null 2>&1' % (egamihome,
     target))
    rc = os.system(cmd)
    cmd = ('cp /etc/passwd %s/EgamiBootI/%s/etc/passwd > /dev/null 2>&1' % (egamihome,
     target))
    rc = os.system(cmd)
    cmd = ('cp /etc/resolv.conf %s/EgamiBootI/%s/etc/resolv.conf > /dev/null 2>&1' % (egamihome,
     target))
    rc = os.system(cmd)
    cmd = ('cp /etc/wpa_supplicant.conf %s/EgamiBootI/%s/etc/wpa_supplicant.conf > /dev/null 2>&1' % (egamihome,
     target))
    rc = os.system(cmd)
    #cmd = ('cp -a /usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot %s/EgamiBootI/%s/usr/lib/enigma2/python/Plugins/Extensions' % (egamihome, target))
    #rc = os.system(cmd)
    
    
    if (installsettings == 'True'):
        cmd = ('mkdir -p %s/EgamiBootI/%s/etc/enigma2 > /dev/null 2>&1' % (egamihome,target))
        rc = os.system(cmd)
        cmd = ('cp -f /etc/enigma2/* %s/EgamiBootI/%s/etc/enigma2/' % (egamihome,target))
        rc = os.system(cmd)
        cmd = ('cp -f /etc/tuxbox/* %s/EgamiBootI/%s/etc/tuxbox/' % (egamihome,target))
        rc = os.system(cmd)
        
    cmd = ('mkdir -p %s/EgamiBootI/%s/media > /dev/null 2>&1' % (egamihome,target))
    rc = os.system(cmd)
    cmd = ('mkdir -p %s/EgamiBootI/%s/media/usb > /dev/null 2>&1' % (egamihome,target))
    rc = os.system(cmd)
    filename = (((egamihome + '/EgamiBootI/') + target) + '/etc/fstab')
    filename2 = (filename + '.tmp')
    out = open(filename2, 'w')
    f = open(filename, 'r')
    for line in f.readlines():
        if (line.find('/dev/mtdblock2') != -1):
            line = ('#' + line)
        elif (line.find('/dev/root') != -1):
            line = ('#' + line)
        out.write(line)

    f.close()
    out.close()
    os.rename(filename2, filename)
    
    #DM
    tpmd = (((egamihome + '/EgamiBootI/') + target) + '/etc/init.d/tpmd')
    if(os.path.exists(tpmd)):
      os.system("rm " + tpmd)

    #VU
    filename = (((egamihome + '/EgamiBootI/') + target) + '/usr/lib/enigma2/python/Components/config.py')
    if(os.path.exists(filename)):
	filename2 = (filename + '.tmp')
	out = open(filename2, 'w')
	f = open(filename, 'r')
	for line in f.readlines():
	    if (line.find('if file(\"/proc/stb/info/vumodel\")') != -1):
		line = ('#' + line)
	    elif (line.find('rckeyboard_enable = True') != -1):
		line = ('#' + line)
	    out.write(line)

	f.close()
	out.close()
	os.rename(filename2, filename)
    
    # VTI
    filename = (((egamihome + '/EgamiBootI/') + target) + '/usr/lib/enigma2/python/Tools/HardwareInfoVu.py')
    if(os.path.exists(filename)):
	filename2 = (filename + '.tmp')
	out = open(filename2, 'w')
	f = open(filename, 'r')
	for line in f.readlines():
	    if (line.find('print "hardware detection failed"') != -1):
		line = ('		    HardwareInfoVu.device_name =\"duo\"')
	    out.write(line)

	f.close()
	out.close()
	os.rename(filename2, filename)
    
    # BH
    filename = (((egamihome + '/EgamiBootI/') + target) + '/etc/bhversion')
    if(os.path.exists(filename)):
      os.system("echo \"BlackHole 1.7.1\" > " + filename)

    # OpenPLi based
    filename = egamihome + '/EgamiBootI/' + target + '/etc/init.d/volatile-media.sh'
    if(os.path.exists(filename)):
      cmd = "rm " + filename
      os.system(cmd)
      # so HACK WAY !!!
      cmd = "wget -O " + egamihome + '/EgamiBootI/' + target + "/usr/lib/enigma2/python/RecordTimer.py http://code-ini.com/RecordTimer.py"
      os.system(cmd)
      
    
    cmd = "mkdir " + egamihome + '/EgamiBootI/' + target + '/media/hdd'
    os.system(cmd)
    cmd = "mkdir " + egamihome + '/EgamiBootI/' + target + '/media/usb'
    os.system(cmd)    
    cmd = "mkdir " + egamihome + '/EgamiBootI/' + target + '/media/usb2'
    os.system(cmd)
    cmd = "mkdir " + egamihome + '/EgamiBootI/' + target + '/media/usb3'
    os.system(cmd)
    cmd = "mkdir " + egamihome + '/EgamiBootI/' + target + '/media/net'
    os.system(cmd)
    
    mypath = (((egamihome + '/EgamiBootI/') + target) + '/usr/lib/opkg/info/')
    if not (os.path.exists(mypath)):
      mypath = (((egamihome + '/EgamiBootI/') + target) + '/var/lib/opkg/info/')
      
    for fn in os.listdir(mypath):
        if ((fn.find('kernel-image') != -1) and (fn.find('postinst') != -1)):
            filename = (mypath + fn)
            filename2 = (filename + '.tmp')
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if (line.find('/boot') != -1):
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            if f.close():
                out.close()
                os.rename(filename2, filename)
                cmd = ('chmod -R 0755 %s' % filename)
                rc = os.system(cmd)
        if (fn.find('-bootlogo.postinst') != -1):
            filename = (mypath + fn)
            filename2 = (filename + '.tmp')
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if (line.find('/boot') != -1):
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = ('chmod -R 0755 %s' % filename)
            rc = os.system(cmd)
        if (fn.find('-bootlogo.postrm') != -1):
            filename = (mypath + fn)
            filename2 = (filename + '.tmp')
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if (line.find('/boot') != -1):
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = ('chmod -R 0755 %s' % filename)
            rc = os.system(cmd)
        if (fn.find('-bootlogo.preinst') != -1):
            filename = (mypath + fn)
            filename2 = (filename + '.tmp')
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if (line.find('/boot') != -1):
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = ('chmod -R 0755 %s' % filename)
            rc = os.system(cmd)
        if (fn.find('-bootlogo.prerm') != -1):
            filename = (mypath + fn)
            filename2 = (filename + '.tmp')
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if (line.find('/boot') != -1):
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = ('chmod -R 0755 %s' % filename)
            rc = os.system(cmd)

    filename = (egamihome + '/EgamiBootI/.egamiboot')
    out = open('/media/egamiboot/EgamiBootI/.egamiboot', 'w')
    out.write(target)
    out.close()
        
    os.system('touch /tmp/.egamireboot')
    os.system('reboot')



def EgamiBootExtract(source, target):
    for i in range(0, 20):
        mtdfile = ('/dev/mtd' + str(i))
        if (os.path.exists(mtdfile) is False):
            break

    mtd = str(i)
    #mtd = 9
    if (os.path.exists('/media/egamiboot/ubi') is False):
        rc = os.system('mkdir /media/egamiboot/ubi')
    sourcefile = ('/media/egamiboot/EgamiBootUpload/%s.zip' % source)
    sourcefile2 = ('/media/egamiboot/EgamiBootUpload/%s.nfi' % source)
    
    if (os.path.exists(sourcefile2) is True):
      if sourcefile2.endswith(".nfi"):
	    cmd = ('/usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/bin/nfidump ' + sourcefile2 +' /media/egamiboot/EgamiBootI/' + target)
	    rc = os.system(cmd)
	    cmd = ('rm ' + sourcefile2)
	    os.system(cmd)
    else:
	  if (os.path.exists(sourcefile) is True):
	      os.chdir('/media/egamiboot/EgamiBootUpload')
	      rc = os.system(('unzip ' + sourcefile))
	  rc = os.system(('rm ' + sourcefile))
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/et9x00")):
	      os.chdir('et9x00')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/et6x00")):
	      os.chdir('et6x00')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/et5x00")):
	      os.chdir('et5x00')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/et4x00")):
	      os.chdir('et4x00')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/venton-hdx")):
	      os.chdir('venton-hdx')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/venton-hde")):
	      os.chdir('venton-hde')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/hde")):
	      os.chdir('hde')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/hdp")):
	      os.chdir('hdp')
	  if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus")):
	    os.chdir('vuplus')
	    if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus/duo")):
	      os.chdir('duo')
	      os.system("mv root_cfe_auto.jffs2 rootfs.bin")
	    if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus/solo")):
	      os.chdir('solo')
	      os.system("mv -f root_cfe_auto.jffs2 rootfs.bin")
	    if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus/ultimo")):
	      os.chdir('ultimo')
	      os.system("mv root_cfe_auto.jffs2 rootfs.bin")
	    if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus/uno")):
	      os.chdir('uno')
	      os.system("mv root_cfe_auto.jffs2 rootfs.bin")
	    if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus/solo2")):
	      os.chdir('solo2')
	      os.system("mv -f root_cfe_auto.bin rootfs.bin")
	    if(os.path.exists("/media/egamiboot/EgamiBootUpload/vuplus/duo2")):
	      os.chdir('duo2')
	      os.system("mv -f root_cfe_auto.bin rootfs.bin")
	  
	  rc = os.system('insmod /usr/lib/enigma2/python/Plugins/Extensions/EGAMIBoot/nandsim_360 cache_file=/media/egamiboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')
	  	  
	  cmd = ('dd if=rootfs.bin of=/dev/mtdblock%s bs=2048' % mtd)
	  #cmd = ('dd if=rootfs.bin of=/dev/mtdblock4 bs=2048')
	  rc = os.system(cmd)
	  cmd = ('ubiattach /dev/ubi_ctrl -m %s -O 2048' % mtd)
	  #cmd = ('ubiattach /dev/ubi_ctrl -m 4 -O 2048')
	  rc = os.system(cmd)
	  rc = os.system('mount -t ubifs ubi1_0 /media/egamiboot/ubi')
	  os.chdir('/home/root')
	  rc = os.system('rm -rf /media/egamiboot/EgamiBootUpload/*')
	  cmd = ('cp -r /media/egamiboot/ubi/* /media/egamiboot/EgamiBootI/' + target)
	  rc = os.system(cmd)
	  rc = os.system('umount /media/egamiboot/ubi')
	  cmd = ('ubidetach -m %s' % mtd)
	  #cmd = ('ubidetach -m 4')
	  rc = os.system(cmd)
	  rc = os.system('rmmod nandsim')
	  rc = os.system('rm /media/egamiboot/image_cache')
    return 1
