#!/usr/bin/python
#
# Purpose: Speaker/session chair's tool using blink(1).
# Description: Green during talk, turns orange when time is 70% gone, flashes red when time expires
# Requirements: blink1-tool is in your path and can be run without sudo
# Usage: blink1.py -d|-e hh:mm:ss [-o hh:mm:ss]
#   where  -d, --duration specifies the total duration of the talk
#          -e, --end      specifies the end time of the talk
#          -o, --orange   specifies time before blink(1) turns orange (optional)
#   Either duration or end must be specified.  Quits if end time has already passed.
# Author: mkargo 20150807


# Import useful stuff
import time
import os
import sys
import getopt


# Define useful things
blink1_tool_path = os.popen("which %s" % "blink1-tool").read().strip()
percentage = 0.7	# How much of time to let pass before turning orange
start_time = time.localtime()
start_seconds = time.mktime(start_time)
end_orange = 0
okgo = False


# Define functions
def printTime(msg, mytime): 
	print msg + time.strftime("%H:%M:%S", mytime)

def changeState(options):
	cmd = blink1_tool_path + " " + options
	#print "cmd:", cmd
	os.popen(cmd)

def printHelp():
	print 'Usage: blink1.py -e|-d mm:ss [-o hh:mm:ss]'
	print '  -h, --help               print this help text'
	print '  -e, --end hh:mm:ss       specify end time'
	print '  -d, --duration hh:mm:ss  specify duration'
	print '  -o, --orange hh:mm:ss    also (optionally) specify time before turning orange'
	sys.exit()


try:
	opts, args = getopt.getopt(sys.argv[1:], "he:d:o:", ["help","end=","duration=","orange="])
except getopt.GetoptError:
	printHelp()

for opt, arg in opts:
	if opt in ('-h', '--help'):
		printHelp()
	elif opt in ("-e", "--end"):
		(end_h, end_m, end_s) = arg.split(':')
		tmp1 = (((start_time.tm_hour * 60) + start_time.tm_min) * 60) + start_time.tm_sec
		tmp2 = (((int(end_h) * 60) + int(end_m)) * 60) + int(end_s)
		toadd = tmp2 - tmp1
		okgo = True
	elif opt in ("-d", "--duration"):
		(dur_h, dur_m, dur_s) = arg.split(':')
		toadd = (((int(dur_h) * 60) + int(dur_m)) * 60) + int(dur_s)
		okgo = True
	elif opt in ("-o", "--orange"):
		(ora_h, ora_m, ora_s) = arg.split(':')
		toorr = (((int(ora_h) * 60) + int(ora_m)) * 60) + int(ora_s)
		end_orange = start_seconds + toorr

# Check inputs were sane
if not okgo:
	printHelp()
end_seconds = start_seconds + toadd
if end_orange == 0:
	end_orange = ((end_seconds - start_seconds) * percentage) + start_seconds
if end_seconds < start_seconds:
	print "Error: ends before it starts!"
	sys.exit()
if end_seconds < end_orange:
	print "Error: will end before it goes orange!"
	sys.exit()

printTime("start:  ", start_time)
printTime("orange: ", time.localtime(end_orange))
printTime("end:    ", time.localtime(end_seconds))

# Start doing pretty colours
doneO = False
doneR = False
while(time.localtime() < time.localtime(end_seconds)):
	if (time.localtime() < time.localtime(end_orange)):
		if not doneO:
			changeState('-ledn 2 -m 500 --rgb 00FF00')
		doneO = True
	if (time.localtime() > time.localtime(end_orange) and time.localtime() < time.localtime(end_seconds)):
		if not doneR:
			changeState('-ledn 2 -m 500 --rgb FFBB00')
		doneR = True
	time.sleep(1)

if (time.localtime() > time.localtime(end_seconds * (1-percentage))):
	changeState('-ledn 2 -m 500 --rgb FF0000  --blink 10')

changeState('-ledn 2 -m 500 --rgb FF0000')

stop_time = time.localtime()
printTime("stop:   ", stop_time)
sys.exit()
