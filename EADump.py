#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import os
import requests
import requests.packages.urllib3

r=requests.get('https://myjamfpro:8443/JSSResource/computerextensionattributes', auth=('username','password'), headers={'accept': 'application/json'})
EAs = r.json()['computer_extension_attributes']

requests.packages.urllib3.disable_warnings()

for record in EAs:
	z=requests.get('https://myjamfpro:8443/JSSResource/computerextensionattributes/id/%s' % record['id'], auth=('username','password'), headers={'accept': 'application/json'})
	if z.json()['computer_extension_attribute']['input_type']['type'] == "script":
		scriptfile = "/Users/rgendler/ExtensionAttributes/" + record['name'] + ".sh"
		contents = z.json()['computer_extension_attribute']['input_type']['script'] 
		target = open(scriptfile, 'w')
		target.write(contents)
		target.close()
	
