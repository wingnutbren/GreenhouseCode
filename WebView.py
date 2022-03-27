#!/usr/bin/python3

import os
import sqlite3
import datetime

db_dir = "/home/pi/GreenHouseLogs"
connection = sqlite3.connect(db_dir+'/Greenhouse_data.db')



print ("Content-Type: text/html")
print ('') 
print (" <TITLE>CoonCreek Green House</TITLE>")

today = datetime.date.today()
print("<TABLE BORDER = 0 PADX='10px'><TR><TD>CURRENT</TD><TD></TD></TR>")
therm_list = []
cursor = connection.execute("select therm_name,ftemp,strftime('%H:%M',max(datetime)) from temps group by therm_name order by therm_name;")
for row in cursor.fetchall():
    therm_list.append(row[0])
    print("<TR bgcolor = 'lightgray'><TD>%s</TD><TD>%2.1f&#176;</TD><TD>@ %s</TD></TR>" %(row[0],row[1],row[2]) )
cursor.close()
print("</TABLE>")


   
#Print the Daily LOWS table
print("<HR>")
print("<TABLE><TR><TD>Today's Lows</TD><TD></TD></TR>")
for therm_name in therm_list:
    query = "select min(ftemp),strftime('%%H:%%M',datetime)as time from temps where therm_name = '%s' and datetime > '%s' " % (therm_name,today)
    lowcursor = connection.cursor();
    lowcursor.execute(query)

    for lowrow in lowcursor.fetchall():
        print ("<TR bgcolor = 'lightblue'><TD>%s</TD><TD>%2.1f&#176;</TD><TD>@ %s</TD></TR>"% (therm_name,lowrow[0],lowrow[1] )) 
print("</TABLE>")

#Print the Daily HIGHS table
print("<HR>")
print("<TABLE><TR><TD>Today's Highs</TD><TD></TD></TR>")
for therm_name in therm_list:
    query = "select max(ftemp),strftime('%%H:%%M',datetime)as time from temps where therm_name = '%s' and datetime > '%s' " % (therm_name,today)
    highcursor = connection.cursor();
    highcursor.execute(query)

    for highrow in highcursor.fetchall():
        print ("<TR bgcolor = 'pink'><TD>%s</TD><TD>%2.1f&#176;</TD><TD>@ %s</TD></TR>"% (therm_name,highrow[0],highrow[1] )) 
print("</TABLE>")






