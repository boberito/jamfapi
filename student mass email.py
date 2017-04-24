#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import os

#must know the ID of the advanced computer search
requestURL = "myjamfpro/JSSResource/computerreports/id/61"


#build the request
request = urllib2.Request(requestURL)
context = ssl._create_unverified_context()
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + base64.b64encode('USER' + ':' + 'PASS'))

reponse = urllib2.urlopen(request, context=context)

#request the json data
response = urllib2.urlopen(request)
response_data = json.loads(response.read())

#set the layer we're looking into
computers = response_data['computer_reports']

#loops and stuff
counter = 0
for record in computers:
		#if record['Department'] == "Class of " + classYear:
			counter+=1
			student_laptop = record['Computer_Name']
			student_username = record['Username']
			Email = record['Email_Address']
			FullName = record['Full_Name']
			FirstName = FullName.strip(" ")
			FirstName = FirstName.split(' ')[0]
			mycommand = "echo 'Hello "+FirstName+",\n\nThis would be the perfect time to run the macOS Sierra upgrade found in Self Service over the 3 day break. So please run the update today. \n\nThis will take approximately an hour, in that time your computer will not be usable. Do NOT close your computer lid during the upgrade. My suggestion is to run it right before going to bed tonight, plug your computer in and run it. \n \nThank you \nMr. Gendler' | mail -s 'Please upgrade your computer to macOS Sierra' " + Email
			os.system(mycommand)
			print mycommand
			print "----------------------------------------------------"
			print "Student UserName: " + student_username + " - Student Computer: " + student_laptop + " - Contacted"
			print "----------------------------------------------------"
print "Number of Students NOT on macOS Sierra:", counter