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

## Flow of Program :
1. Check for system status (lock or unlock) on every SYSTEM_CHECK_INTERVAL
2. Pop-up notification on every SYSTEM_LOCK_THRESHOLD_LIST(times SYSTEM_CHECK_INTERVAL) interval
3. It is possible ignore upto last notification from SYSTEM_LOCK_THRESHOLD_LIST, then system should be lock for BREAKTIME(times SYSTEM_CHECK_INTERVAL) interval 
4. If system will unlocked before BREAKTIME(times SYSTEM_CHECK_INTERVAL) interval then it will pop-up notification to lock system (step 2)
5. For locked system, Checking interval will reduce by SYSTEM_LOCKED_REDUCED_THRESHOLD factor, after SYSTEM_LOCKED_REDUCED_THRESHOLD(times SYSTEM_CHECK_INTERVAL) interval

## Screenshots :
![Screenshot First](images/BreakTime_Notification_First.png)
![Screenshot Last](images/BreakTime_Notification_Last.png)
