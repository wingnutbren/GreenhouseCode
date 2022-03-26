#!/usr/bin/python3

import os
import sqlite3
import datetime

db_dir = "/home/pi/GreenHouseLogs"
connection = sqlite3.connect(db_dir+'/Greenhouse_data.db')



print ("Content-Type: text/html")
print ('') 
print ("""
      <TITLE>CoonCreek Green House</TITLE>
      <H2> Greenhouse Temperatures</H2>


      """)

today = datetime.date.today()
#cursor = connection.execute("select distinct(therm_name) from temps order by therm_name")
#for row in cursor.fetchall():
    #print(row[0])
#print('')
#print("<TABLE BORDER = 1><TR><TD></TD><TD>CURRENT</TD><TD bgcolor = 'pink'>24h High</TD><TD bgcolor = 'lightblue'>24h Low</TD></TR>")
print("<TABLE BORDER = 1><TR><TD></TD><TD>CURRENT</TD></TR>")

cursor = connection.execute("select therm_name,ftemp,max(datetime) from temps group by therm_name order by therm_name;")
for row in cursor.fetchall():
    print("<TR><TD>%s</TD><TD>%2.1f</TD></TR>" %(row[0],row[1]) )
cursor.close()
print("</TABLE>")
   
#cursor = connection.execute("select distinct(therm_name) from temps order by therm_name")
#therm_list = cursor.fetchall()
#cursor.close()

#for row in therm_list:
    ##lowcursor = connection.execute("select therm_name,max(ftemp),datetime from temps where threm_name = '"+row[0]+"' and datetime > "
    #print lowcursor.fetchall()






