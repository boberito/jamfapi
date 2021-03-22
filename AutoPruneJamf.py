#!/usr/bin/python

#####################################################################
#
# Scrapes the more the Advanced Computer Search -Hasn't checked in for more than 6 months
# Moves machines that haven't checked in for more than 6 months to Unmanaged
# Writes a file of what was moved and some details about it to /Library/Logs/Moved-to-Unmanaged.log
# Scrapes that log file, if the machine hasn't Recon'd in more than a year
# Downloads an individual xml file for each to /Library/Logs/unmanaged_computers_deleted/
# Then deletes the record from Jamf
#
#####################################################################

import urllib2
import base64
import json
import os
import ssl
import csv
import plistlib
from datetime import date, timedelta
from time import gmtime, strftime
import subprocess

#Base64 of credentials
# format username:password
credentials = ''

#Advanced Computer Search ID of machines that have a last checkin or inventory of more than 6 months
ACS = '421'

outputcsv = "/Library/Logs/Moved-to-Unmanaged.log"
target = open(outputcsv, 'a')

#You can set jamfURL to https://jamfserver:8443/ or read from the plist
#whatever is more fun for you, and just comment out line 41-43
pref_path = "/Library/Preferences/com.jamfsoftware.jamf.plist"

jamfURL = ""

if os.path.exists(pref_path) is True and jamfproserver == "":
	command = "defaults read " + pref_path + " jss_url"
	jamfURL = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)[:-1]


today = date.today()
todayDate=today.strftime('%m-%d-%y')


jamfproserver = jamfURL + 'JSSResource/advancedcomputersearches/id/' + ACS
request = urllib2.Request(jamfproserver)   
request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + credentials)
jamfresponse = urllib2.urlopen(request)
response_data = json.loads(jamfresponse.read())

computers = response_data['advanced_computer_search']['computers']
newlist = []
previous_entry = ""


####
# This is the portion that moves old machines to unmanaged
###
for computer in computers:
	if computer['Managed'] == "Managed":
			xmldata = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><computer><general><remote_management><managed>false</managed></remote_management></general></computer>"
			jamfcomputer = jamfproserver + "JSSResource/computers/serialnumber/" + computer['Serial_Number']

			opener = urllib2.build_opener(urllib2.HTTPSHandler)
			request = urllib2.Request(jamfcomputer, data=xmldata)

			request.add_header('content-type', 'application/xml')
			request.add_header('Authorization', 'Basic ' + credentials)
			request.get_method = lambda: 'PUT'

			response = opener.open(request)
			now = strftime("%m-%d-%y %H:%M", gmtime())
			print >>target, now, ",", computer['Computer_Name']  + "," + computer['Serial_Number'] + ",Moved to Unmanaged,Last Recon: " + computer['Last_Inventory_Update'] + ",Last CheckIn: " + computer['Last_Check_in']

target.close()

logfile = file("/Library/Logs/Moved-to-Unmanaged.log")
unmanaged = csv.reader(logfile)

####
# This is the portion that deletes old machines
###

### comment out all below if you dont want deleting
for row in unmanaged:
	checkIn = row[4].split(": ")
	justDate = checkIn[1].split(" ")
	
	yearAgo = date.today() - timedelta(365)
	yearAgoDate = yearAgo.strftime('%Y-%m-%d')
	if justDate[0] < yearAgoDate:
		
		computerRecordOutput = "/Library/Logs/unmanaged_computers_deleted/" + row[1][1:] + ".xml"
		#print computerRecordOutput
		if os.path.exists(computerRecordOutput) is False:
			computerXML = open(computerRecordOutput, "w")
			jamfProServerComputer = jamfproserver + 'JSSResource/computers/serialnumber/' + row[2]
			request = urllib2.Request(jamfProServerComputer)   
			request.add_header('Accept', 'text/xml')
			request.add_header('Authorization', 'Basic ' + credentials)
			jamfresponse = urllib2.urlopen(request)
			print jamfProServerComputer
            print >> computerXML, jamfresponse.read()
			computerXML.close()

			computerToDelete = jamfproserver + "JSSResource/computers/serialnumber/" + row[2]
			#print computerToDelete
			#computerToDelete = jamfproserver + "JSSResource/computers/serialnumber/" + computer['Serial_Number']
			#print computerToDelete
			opener = urllib2.build_opener(urllib2.HTTPSHandler)
			request = urllib2.Request(computerToDelete)
			request.add_header('Authorization', 'Basic ' + credentials)
			request.get_method = lambda: 'DELETE'
			response = opener.open(request)
			#print computerToDelete

logfile.close()
