#
# File name: bootup.py
#
# Author: Piyush
#
# Description: Calling Script for breaktime.py (Example)
# 
# Chanage log:
# 06/25/2017 : Initial version. (Piyush)
#
#

import os
import sys

if(os.name == 'nt'): #For Window
	os.system("start /B C:\Python27\pythonw.exe src\breaktime.py") #Run in Background
	#os.system("C:\Python27\python.exe src\breaktime.py") #Run in Foreground (Debugging)
#elif(os.name == 'mac'): #For MacOS
#	print("Current OS type: MacOS.")
else: # Not supported system
	print("This program is not supported in current OS.")
	sys.exit(0)

