#
# File name: breaktime.py
#
# Author: Piyush
#
# Description: Remainder for BreakTime
# 
# Chanage log:
# 06/25/2017 : Initial version. (Piyush)
#
#

import os
import sys
import time
import Tkinter as tk #import tkinter
import ctypes

def is_system_locked():
	if(os.name == 'nt'): #For Window7
		system_status = not ctypes.windll.User32.SwitchDesktop(ctypes.windll.User32.OpenDesktopA("default", 0, False, 0x0100))
	#elif(os.name == 'mac'): #For MacOS
	#	system_status = 
	return system_status

class SystemLockGUI(tk.Frame):
	def __init__(self, master=None, ignorance_type="NoIgnore"):
		tk.Frame.__init__(self, master)
		master.title("BreakTime!!")
		##To Keep window on TOP
		master.lift()
		master.call('wm', 'attributes', '.', '-topmost', True)
		master.after_idle(master.call, 'wm', 'attributes', '.', '-topmost', False)
		##
		master.protocol('WM_DELETE_WINDOW', self.closeGUI)
		self.pack()
		self.timer_sec = 0
		self.ignorance_type = ignorance_type
		self.createWidgets()

	def createWidgets(self):
		self.timer_sec = 30

		self.info = tk.Label(self)
		self.info["fg"]   = "black"
		self.info["text"] = "System will be locked after following seconds.."
		self.info.grid(row=0,column=0, columnspan=2, sticky="WE")

		self.timer = tk.Button(self, font=('Helvetic', 48))
		self.now = tk.StringVar()
		self.timer["textvariable"] = self.now
		self.timer["command"] = self.wait_more
		self.timer.grid(row=1, column=0, columnspan=2, sticky="WENS")
		self.onUpdate()

		self.lock = tk.Button(self)
		self.lock["fg"]   = "blue"
		self.lock["text"] = "LOCK Now"
		self.lock["command"] = self.system_lock
		
		if(self.ignorance_type == "NoIgnore"):
			self.lock.grid(row=2,column=0, columnspan=2, sticky="WE")
		else:
			self.lock.grid(row=2,column=0, columnspan=1, sticky="WE")

			self.QUIT = tk.Button(self)
			self.QUIT["fg"]   = "red"
			self.QUIT["text"] = "Ignore"
			self.QUIT["command"] =  self.quit
			self.QUIT.grid(row=2, column=1, sticky="WE")

	def onUpdate(self):
		self.timer_sec = self.timer_sec - 1
		self.now.set(str(self.timer_sec))
		if(self.timer_sec > 0):
			self.after(1000, self.onUpdate)
		else:
			self.system_lock()
                
	def system_lock(self):
		self.timer_sec = 0
		if(os.name == 'nt'): #For Window7
			ctypes.windll.user32.LockWorkStation()
		#elif(os.name == 'mac'): #For MacOS
		#	subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend', shell=True)
		#print("System LOCKED.")
		time.sleep(10)
		self.quit()

	def wait_more(self):
		self.timer_sec = self.timer_sec + 30
		#print("Okey, 30 seconds added in waiting timer..")

	def closeGUI(self):
		if(self.ignorance_type == "NoIgnore"):
			self.system_lock()
		self.quit()

def runGUI(ignore_type):
	root = tk.Tk()
	app = SystemLockGUI(master=root, ignorance_type=ignore_type)
	app.mainloop()
	try:
		root.destroy()
	except:
		pass
	#print("GUI Destroyed.")

if __name__ == '__main__':
	if(os.name == 'nt'): #For Window
		print("Current OS type: Window.")
	#elif(os.name == 'mac'): #For MacOS
	#	print("Current OS type: MacOS.")
	else: # Not supported system
		print("This program is not supported in current OS.")
		sys.exit(0)
	SYSTEM_CHECK_INTERVAL = 60*2 							#Checking(if system is locked or not) interval in seconds
	SYSTEM_LOCK_THRESHOLD_LIST = [25,27,29] #times of SYSTEM_CHECK_INTERVAL		#Threshold to lock system with pop-up notification, may ignore upto last notification
	SYSTEM_LOCKED_REDUCED_THRESHOLD = 8 #times of SYSTEM_CHECK_INTERVAL		#Threshold to reduce checking interval (by same number) for locked system
	BREAKTIME = 2 #times of SYSTEM_CHECK_INTERVAL					#If system unlocked before this breaktime then start notifications to lock system
	sys_status = BREAKTIME
	while True:
		timer_sleep = SYSTEM_CHECK_INTERVAL
		if(is_system_locked()):
			sys_status = (0 if(sys_status < 0)else (sys_status + 1))
			if(sys_status > SYSTEM_LOCKED_REDUCED_THRESHOLD):
				timer_sleep = (SYSTEM_LOCKED_REDUCED_THRESHOLD*SYSTEM_CHECK_INTERVAL)
		else:
			sys_status = (-1 if(sys_status >= BREAKTIME)else ((-SYSTEM_LOCK_THRESHOLD_LIST[0]) if(sys_status >= 0)else (sys_status - 1)))
			if((-sys_status) in SYSTEM_LOCK_THRESHOLD_LIST[:-1]):
				runGUI("MayIgnore")
			elif((-sys_status) == SYSTEM_LOCK_THRESHOLD_LIST[-1]):
				runGUI("NoIgnore")
				sys_status = 0
		time.sleep(timer_sleep)
		#print("sys_status = " + str(sys_status) + ", timer_sleep = " + str(timer_sleep))
	#raw_input("Press any to key to Exit.")
