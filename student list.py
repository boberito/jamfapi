#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl



#Pass graduation year in 2 number format
classYear = sys.argv[1]

requestURL = "https://myjamfpro/JSSResource/computerreports/id/61"

#build the request
request = urllib2.Request(requestURL)
context = ssl._create_unverified_context()
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + base64.b64encode('ENTER USERNAME' + ':' + 'ENTER PASSWORD'))

reponse = urllib2.urlopen(request, context=context)

#request the json data
response = urllib2.urlopen(request)
response_data = json.loads(response.read())

#set the layer we're looking into
computers = response_data['computer_reports']

#loops and stuff
counter = 0
for record in computers:
		if record['Department'] == "Class of " + classYear:
			counter+=1
			student_laptop = record['Computer_Name']
			student_username = record['Username']
			print "Student UserName: %s" % student_username
			print "Student Computer: %s" % student_laptop
			print ""
print "Number of Students in Class of " + classYear + " NOT on macOS Sierra:", counter
print