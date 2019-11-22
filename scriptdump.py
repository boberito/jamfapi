#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import getpass
import os

JSSServer='https://Jamf Pro Server:8443'

JSSUser = raw_input("Enter Your JSS Account:")
JSSPass = getpass.getpass("Password: ")

ScriptrequestURL = JSSServer + "/JSSResource/scripts"
request = urllib2.Request(ScriptrequestURL)   
request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'Basic ' + base64.b64encode(JSSUser + ':' + JSSPass))
response = urllib2.urlopen(request)

response_data = json.loads(response.read())
JamfScripts = response_data['scripts']
for record in JamfScripts:
    scriptrequest = JSSServer + '/JSSResource/scripts/id/%s' % record['id']
    request = urllib2.Request(scriptrequest)   
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', 'Basic ' + base64.b64encode(JSSUser + ':' + JSSPass))
    response = urllib2.urlopen(request)
    response_data = json.loads(response.read())
    contents = str(response_data['script']['script_contents'].encode("ascii", 'ignore'))
    contents = contents.replace("\r","")
    scriptfile = "/Users/Shared/JAMFScripts/" + record['name']
    if scriptfile[-3:] != ".sh":
        scriptfile = scriptfile + ".sh"
    scriptfile = scriptfile.replace(" ", "_")
    target = open(scriptfile, 'w')
    target.write(contents)
    target.close()
