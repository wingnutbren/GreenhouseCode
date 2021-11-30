import json
from collections import namedtuple
print("Launching Thermostat Control . . .\n")

#Declare Functions

def read_temp_fahrenheit(filename):
	therm_file = open(filename,"r")
	contents = therm_file.read()
	#the contents of the thermostat file will look something like this:
	# e7 00 4b 46 7f ff 0c 10 6b : crc=6b YES
	# e7 00 4b 46 7f ff 0c 10 6b t=14437

	therm_file.close
	temp = int(contents.split("t=")[1])/1000.0
	temp = temp*1.8+32 #convert to Fahrenheit
	return(temp)
	
#Open File
thermFile=open('Therms.json')

#get a dictionary based on file
data = json.load(thermFile)

#iterate through Thermometers
for thermometers in data['therm_details']:
	temp = read_temp_fahrenheit(thermometers['path_to_file'])
	print(thermometers['therm_name']+": "+str(temp)+"\n")

#close the file
thermFile.close

