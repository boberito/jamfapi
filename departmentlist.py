#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import urllib

requestURL ="https://myjamfpro:8443/JSSResource/departments"

#build the request

request = urllib2.Request(requestURL)
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context
request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + base64.b64encode('USERNAME' + ':' + 'PASSWORD'))


#request the json data
response = urllib2.urlopen(request)
response_data = json.loads(response.read())

#set the layer we're looking into
departmentinfo = response_data['departments']

fulldepartment = ""

#loops for every instance of mapped printers
for ea in departmentinfo:
        departmentname = ea['name']
        fulldepartment = fulldepartment + departmentname + '\" \"'


print '\"' + fulldepartment
