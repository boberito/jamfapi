#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import os
import requests
import requests.packages.urllib3

APIUsername='username'
APIPassword='password'
JamfProServer='https://YOURJAMFPROSERVER:8443/'

r=requests.get(JamfProServer + 'JSSResource/computerextensionattributes', auth=(APIUsername,APIPassword), headers={'accept': 'application/json'})
EAs = r.json()['computer_extension_attributes']

requests.packages.urllib3.disable_warnings()

for record in EAs:
	z=requests.get(JamfProServer + 'JSSResource/computerextensionattributes/id/%s' % record['id'], auth=(APIUsername,APIPassword), headers={'accept': 'application/json'})
	if z.json()['computer_extension_attribute']['input_type']['type'] == "script":
		scriptfile = "/Users/Shared/ExtensionAttributes/" + record['name'] + ".sh"
		contents = z.json()['computer_extension_attribute']['input_type']['script'] 
		target = open(scriptfile, 'w')
		target.write(contents)
		target.close()
	
