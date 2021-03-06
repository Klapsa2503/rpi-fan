# rpi-fan

### Description

This script checks current RaspberryPi temperature and in case it's higher than limit set by user it will enable fan and 
display notification on OSMC display.

Script checks current device temperature every 2 seconds. In case temperature will be too high, 
fan will be enabled for 120 seconds and then temperature will be rechecked.

### Installation

#### Prepare fan

To install this script first you need to setup electrical circuit so that fan can start when temperature will rise.
 Following illustration shows how to do that:
 
![alt tag](circuit-diagram.png)
 
##### Start script

* Download file `fan.py` and place it wherever you like.
* Execute command `sudo crontab -e`
* Add new cron entry, example: `@reboot /usr/bin/python /home/osmc/scripts/fan.py -l INFO -t 45.0`. 
Script will start with RaspberryPi

Available arguments:

* **-h** - help
* **-l** - log level (TRACE, DEBUG, ...) [default: `INFO`]
* **-t** - temperature above which fan will start [default: `40.0`]
* **-p** - pin to which fan (`PWM`) will be connected [default: `7`]
* **-b** - pin to which fan buzzer will be connected [default: buzzer is disabled]
* **-d** - if passed, notifications will not be shown

### Debugging

Logs are located in `/home/osmc/logs/fan.log`

### Other

Actions, such as displaying notification cam be performed thanks to built in script `xbmc-send`
More details about available functions are listed in this [wiki](http://kodi.wiki/view/List_of_built-in_functions)