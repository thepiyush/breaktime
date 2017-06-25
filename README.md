# breaktime
Reminder for BreakTime !!

## Parameters (with default values) :
> It reminds to take a break of 4 minute on every 50 (, 54 and 58) minutes by default.
* SYSTEM_CHECK_INTERVAL = 60*2
	* checking (if system is locked or not) interval in seconds
* SYSTEM_LOCK_THRESHOLD_LIST = [25,27,29] #times of SYSTEM_CHECK_INTERVAL
	* Threshold to lock system with pop-up notification, may ignore upto last notification
* SYSTEM_LOCKED_REDUCED_THRESHOLD = 8 #times of SYSTEM_CHECK_INTERVAL
	* Threshold to reduce checking interval (by same number) for locked system
* BREAKTIME = 2 #times of SYSTEM_CHECK_INTERVAL
	* If system unlocked before this breaktime then start notifications to lock system
  
## Supported OS :
* Window
