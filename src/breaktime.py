#
# File name: breaktime.py
#
# Author: Piyush
#
# Description: Remainder for BreakTime
# 
# Chanage log:
# 2017/06/25 : Initial version. (Piyush)
# 2017/06/30 : Updated GUI class & Parameters AND Removed 'while True' loop from main. (Piyush)
#
#

import os
import sys
import time
import Tkinter as tk #import tkinter
import ctypes

class SystemLockGUI(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.root = master
		self.root.title("BreakTime!!")
		##### User Parameters #####
		self.BREAKTIME = 4*60						#(in seconds) #If system unlocked before this breaktime then start notifications again to lock system
		self.SYSTEM_LOCK_NOTIFICATION_LIST = [50*60,54*60,58*60]	#(in seconds) #Threshold to lock system with pop-up notification, possible to ignore upto last notification
		self.SYSTEM_CHECK_INTERVAL = 2*60 				#(in seconds) #Checking(if system is locked or not) interval
		self.SYSTEM_CHECK_INTERVAL_REDUCED = 15*60			#(in seconds) #Reduced checking interval for locked system (after same interval)
		self.NOTIFICATION_TIMER_INIT = 30				#(in seconds) #System lock Notification timer initialization time/value
		###########################
		# Round of Notification list to checking interval
		self.SYSTEM_LOCK_NOTIFICATION_LIST = sorted(list(set([self.roundoff(x, self.SYSTEM_CHECK_INTERVAL) for x in self.SYSTEM_LOCK_NOTIFICATION_LIST])))
		## Variables
		sys_status_curr_abs = abs(self.get_sys_status())
		self.sys_status = [-sys_status_curr_abs,sys_status_curr_abs-1,-sys_status_curr_abs+(2*self.BREAKTIME),0]
		self.gui_exit_with_sys_lock = False
		self.gui_timer_sec = 0
		## To Keep window on TOP
		self.root.lift()
		self.root.call('wm', 'attributes', '.', '-topmost', True)
		self.root.after_idle(master.call, 'wm', 'attributes', '.', '-topmost', False)
		## create widgets
		self.root.protocol('WM_DELETE_WINDOW', self.closeGUI)
		self.pack()
		self.hideGUI()
		self.createWidgets()

	def createWidgets(self):
		self.info = tk.Label(self)
		self.info["fg"]   = "black"
		self.info["text"] = "System will be locked after following seconds.."
		self.info.grid(row=0,column=0, columnspan=2, sticky="WE")

		self.timer = tk.Button(self, font=('Helvetic', 48))
		self.now = tk.StringVar()
		self.now.set("30")
		self.timer["textvariable"] = self.now
		self.timer["command"] = self.wait_more
		self.timer.grid(row=1, column=0, columnspan=2, sticky="WENS")

		self.lock = tk.Button(self)
		self.lock["fg"]   = "blue"
		self.lock["text"] = "LOCK Now"
		self.lock["command"] = self.system_lock
		self.lock.grid(row=2,column=0, columnspan=1, sticky="WE")

		self.QUIT = tk.Button(self)
		self.QUIT["fg"]   = "red"
		self.QUIT["text"] = "Ignore"
		self.QUIT["command"] =  self.closeGUI
		self.QUIT.grid(row=2, column=1, columnspan=1, sticky="WE")
		self.QUIT.lower() #To Hide when 'lock' button size changes

		self.onUpdate()

	def updateGUI(self, gui_timer_sec):
		self.now.set(str(gui_timer_sec))
		if(self.gui_exit_with_sys_lock == True):
			self.lock.grid(row=2,column=0, columnspan=2, sticky="WE")
		else:
			self.lock.grid(row=2,column=0, columnspan=1, sticky="WE")

	def wait_more(self):
		self.gui_timer_sec = self.gui_timer_sec + self.NOTIFICATION_TIMER_INIT

	def onUpdate(self):
		sys_status_prev = self.sys_status[0]
		sys_status_curr = self.get_sys_status()
		if(not self.is_same_sign(sys_status_curr,sys_status_prev)): #push changed sys status
			self.sys_status[1:] = self.sys_status[:-1]
		elif(sys_status_curr < 0 and sys_status_prev < 0 and self.abs_diff(sys_status_curr,sys_status_prev) > self.BREAKTIME): #Reset sys_status after 'long' unlocked/sleep state
			self.sys_status[1] = - sys_status_curr - 2
			sys_status_prev = - (- sys_status_curr - 1)
		self.sys_status[0] = sys_status_curr
		sys_status_checking_time = self.SYSTEM_CHECK_INTERVAL
		if(self.sys_status[0] >= 0): #locked system
			self.hideGUI()
			if(self.abs_diff(self.sys_status[0],self.sys_status[1]) >= self.SYSTEM_CHECK_INTERVAL_REDUCED):
				sys_status_checking_time = self.SYSTEM_CHECK_INTERVAL_REDUCED
		else: #unlocked system
			if(self.abs_diff(self.sys_status[1],self.sys_status[2]) < self.BREAKTIME):
				self.sys_status[1:-2] = self.sys_status[3:]
			sys_unlocked_duration_prev = self.abs_diff(sys_status_prev,self.sys_status[1])
			sys_unlocked_duration_curr = self.abs_diff(self.sys_status[0],self.sys_status[1])
			if(next((True for n in self.SYSTEM_LOCK_NOTIFICATION_LIST if(sys_unlocked_duration_prev < n <= sys_unlocked_duration_curr)),False)): #Pop-up GUI
				self.unhideGUI()
				self.gui_timer_sec = (self.gui_timer_sec if(self.gui_timer_sec)else self.NOTIFICATION_TIMER_INIT)
			self.gui_exit_with_sys_lock = (True if((sys_unlocked_duration_curr + self.gui_timer_sec) >= self.SYSTEM_LOCK_NOTIFICATION_LIST[-1])else False)
			if(self.get_gui_status()): #Update GUI
				self.updateGUI(self.gui_timer_sec)
				self.gui_timer_sec = self.gui_timer_sec - 1
				if(self.gui_timer_sec == 0): #Lock the system
					self.system_lock()
				else:
					sys_status_checking_time = 1
		self.after(sys_status_checking_time*1000, self.onUpdate)
		#print("sys_status="+str(self.sys_status)+", gui_timer_sec="+str(self.gui_timer_sec)+", GUIstatus="+str(self.get_gui_status()))

	def get_sys_status(self):
		return (int(time.time()) if(self.is_system_locked())else -int(time.time()))

	def system_lock(self):
		if(os.name == 'nt'): #For Window7
			ctypes.windll.user32.LockWorkStation()
		#elif(os.name == 'mac'): #For MacOS
		#	subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend', shell=True)
		#print("System LOCKED.")
		self.hideGUI()

	def is_system_locked(self):
		if(os.name == 'nt'): #For Window7
			system_lock_status = not ctypes.windll.User32.SwitchDesktop(ctypes.windll.User32.OpenDesktopA("default", 0, False, 0x0100))
		#elif(os.name == 'mac'): #For MacOS
		#	system_lock_status = 
		return system_lock_status

	def roundoff(self, x, n):
		return int(n * round(float(x)/n))

	def is_same_sign(self, a, b):
		return ((a>=0 and b>=0) or (a<=0 and b<=0))

	def abs_diff(self, a, b):
		return abs(abs(a) - abs(b))

	def get_gui_status(self):
		return (True if(self.root.state() != "withdrawn")else False)

	def unhideGUI(self):
		if(self.root.state() == "withdrawn"):
			self.root.deiconify()

	def hideGUI(self):
		self.gui_exit_with_sys_lock = False
		self.gui_timer_sec = 0
		if(self.root.state() != "withdrawn"):
			self.root.withdraw()
	
	def closeGUI(self):
		if(self.gui_exit_with_sys_lock == True):
			self.system_lock()
		else:
			self.hideGUI()
		#self.quit()

if __name__ == '__main__':
	if(os.name == 'nt'): #For Window
		print("Current OS type: Window.")
	#elif(os.name == 'mac'): #For MacOS
	#	print("Current OS type: MacOS.")
	else: # Not supported system
		print("This program is not supported in current OS.")
		sys.exit(0)
	root = tk.Tk()
	app = SystemLockGUI(master=root)
	app.mainloop()
	try:
		root.destroy()
	except:
		pass
	#print("GUI Destroyed.")
	#raw_input("Press any to key to Exit.")
