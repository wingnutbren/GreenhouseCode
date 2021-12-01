import json
import time
from collections import namedtuple
import RPi.GPIO as GPIO
import signal
import sys

#Declare Functions

#Access the thermometer dictionary and read the 'files' associated with each one to 
#determine the current temperature.  return the temperature in fahrenheit
def read_temp_fahrenheit(thermometer):
	therm_file = open(thermometer['path_to_file'],"r")
	contents = therm_file.read()
	#the contents of the thermostat file will look something like this:
	# e7 00 4b 46 7f ff 0c 10 6b : crc=6b YES
	# e7 00 4b 46 7f ff 0c 10 6b t=14437

	therm_file.close
	temp = int(contents.split("t=")[1])/1000.0
	temp = temp*1.8+32 #convert to Fahrenheit
	return(temp)

# Iterate through each thermometer and update its current temperature
def refresh_thermometers(therms):
    #iterate through Thermometers
    for thermometer in therms:
        thermometer['therm_temp'] = read_temp_fahrenheit(thermometer)
        print(thermometer['therm_name']+": "+str(thermometer['therm_temp'])+"\n")

# Iterate through each thermometer and, if the thermometer is being monitored,
# check its current temp against the allowable temps.
# Start the fan if the temp is outside allowable temp
# Stop the fan if the temp is within allowable temp
# Return the fan state
def alter_fan_state(data):
    #iterate through Thermometers
    for thermometer in data['therm_details']:
        if (thermometer['monitor_me'].lower()=="true" ):
            print('Monitoring '+thermometer['therm_name'])
            state='off'
            if(thermometer['therm_temp']>thermometer['temp_max']):
                    state='on'
            if(thermometer['therm_temp']<thermometer['temp_min']):
                    state='on'
    if(state=='on'):
        GPIO.output(18,GPIO.HIGH)
    else:
        GPIO.output(18,GPIO.LOW)
    return(state)   

#Process the Ctrl_C keystroke from shell
#This handler will be registered in the Main below
def sigint_handler(signal, frame):
    print('\n\nScript Interrupted by signal, Turning off fans and exiting')
    GPIO.output(18,GPIO.LOW)
    sys.exit(0)
	
####################     main    ####################
print("Launching Thermostat Control . . .\n")
#Say what to do when someone presses Ctrl+C
signal.signal(signal.SIGINT,sigint_handler)

#Initialize GPIO Pins for fan control
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

#Open File to read configurations
thermFile=open('Therms.json')
#get a dictionary based on file
data = json.load(thermFile)
#close the file
thermFile.close 

#Main loop: read temperatures, set fans on/off, record data to CSV
while(1):
    refresh_thermometers(data['therm_details'])
    fanstate = alter_fan_state(data)
    print("fan is now "+fanstate)
    time.sleep(float(data['check_freq_seconds']))
