import RPi.GPIO as GPIO ## Import GPIO library
import sys
import os
import threading
import time
import logging
import getopt
import argparse

# More info about logging in python: https://docs.python.org/2.6/library/logging.html
def configureLogging(loglevel):
	numeric_level = getattr(logging, loglevel.upper(), None)
	FORMAT = '%(asctime)-15s %(message)s'
	logging.basicConfig(filename='/home/osmc/logs/fan.log',level=numeric_level,format=FORMAT)
	
# Return CPU temperature as a character string
def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))

def loop(pin, max_temp):
	CPU_temp = float(getCPUtemperature())
	enable = CPU_temp > max_temp
	GPIO.output(pin,enable)
	if enable:
		logging.info('Registered temperature: {} fan will start'.format(CPU_temp))
		threading.Timer(120, loop, [pin, max_temp]).start()
	else:		
		logging.debug('Temperature registered: {}'.format(CPU_temp))
		threading.Timer(2, loop, [pin, max_temp]).start()

def main():

	# Default values
	loglevel = 'INFO'
	max_temp = 40.0
	pin = 7

	# Command line arguments/options
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hl:t:p:")
	except getopt.GetoptError:
		logging.error('Failed to start. Example run command: python fan.py -l DEBUG -t 50.0')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
        		print 'python fan.py -l DEBUG -t 50.0'
			sys.exit()
		elif opt in ("-l"):
			loglevel = arg
			configureLogging(loglevel)
		elif opt in ("-t"):
			max_temp = arg
		elif opt in ("-p"):
			pin = int(arg)

	configureLogging(loglevel)

	#Configure pins
	GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
	GPIO.setup(pin, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

	logging.info('Configuration finished. Log_level: {}, max_temp: {}, starting main loop'.format(loglevel, max_temp))

	loop(pin, float(max_temp))

if __name__ == "__main__":
	main()
