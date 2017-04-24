#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import os
import requests
import requests.packages.urllib3

r=requests.get('https://myjamfpro:8443/JSSResource/scripts', auth=('USER','PASS'), headers={'accept': 'application/json'})
jamfscripts = r.json()['scripts']

requests.packages.urllib3.disable_warnings()

for record  in jamfscripts:
	z=requests.get('https://myjamfpro:8443/JSSResource/scripts/id/%s' % record['id'], auth=('USER','PASS'), headers={'accept': 'application/json'})
	scriptfile = "JAMFScripts/" + record['name'] + ".sh"
	contents = z.json()['script']['script_contents']
	target = open(scriptfile, 'w')
	target.write(contents)
	target.close()
	

