#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import os


requestURL = "https://***REMOVED***:8443/JSSResource/computerreports/id/67"

#build the request
request = urllib2.Request(requestURL)
context = ssl._create_unverified_context()
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + base64.b64encode('API-USERNAME' + ':' + 'API-PASS'))

reponse = urllib2.urlopen(request, context=context)

#request the json data
response = urllib2.urlopen(request)
response_data = json.loads(response.read())

#set the layer we're looking into
computers = response_data['computer_reports']

#loops and stuff
for record in computers:
		student_laptop = record['Computer_Name']
		student_username = record['Username']
		Email = record['Email_Address']
		FullName = record['Full_Name']
		FirstName = FullName.strip(" ")
		FirstName = FirstName.split(' ')[0]
		mycommand = "echo 'Hello "+FirstName+",\n\nYour computer has not reported into our inventory system in a while. It is reporting your computer missing or stolen. It is nothing you have done, these things sometimes happen. If you can swing by with your computer, it should only take a few minutes to get it to check back in with our system. \n\nThanks, Mr. Gendler' | mail -s 'Please swing by the Tech Department' " + Email
		os.system(mycommand)
		print mycommand
