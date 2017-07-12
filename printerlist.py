#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import urllib


#Enter computer name (for example EA1234)
computer_name = sys.argv[1]

requestURL ="https://myjamfpro:8443/JSSResource/computers/name/" + computer_name

#build the request
request = urllib2.Request(requestURL)
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + base64.b64encode('JAMF API USERNAME' + ':' + 'JAMF API PASSWORD'))

response = urllib2.urlopen(request)
response_data = json.loads(response.read())

#set the layer we're looking into
printers = response_data['computer']['hardware']['mapped_printers']


#loops for every instance of mapped printers
for ea in printers:
        printer_name = ea['name']
        printer_type = ea['type']
        print "Printer Name: %s" % printer_name
	print "Printer Type: %s" % printer_type
	print ""
