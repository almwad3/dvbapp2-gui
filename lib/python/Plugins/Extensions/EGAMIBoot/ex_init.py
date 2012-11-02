#!/usr/bin/python 

import sys, egamiboot

if len(sys.argv) < 3:
	pass
else:
	egamiboot.EgamiBootMainEx(sys.argv[1], sys.argv[2], sys.argv[3])

