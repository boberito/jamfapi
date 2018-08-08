#!/usr/bin/python

import urllib2
import base64
import json
import sys
import ssl
import os
import requests
import requests.packages.urllib3

APIUsername=''
APIPassword=''
JamfProServer='https://YOURJAMFPROSERVER:8443/'

r=requests.get(JamfProServer + 'JSSResource/scripts', auth=(APIUsername,APIPassword), headers={'accept': 'application/json'})
jamfscripts = r.json()['scripts']

requests.packages.urllib3.disable_warnings()

for record  in jamfscripts:
	z=requests.get(JamfProServer + 'JSSResource/scripts/id/%s' % record['id'], auth=(APIUsername,APIPassword), headers={'accept': 'application/json'})
	scriptfile = "JAMFScripts/" + record['name'] + ".sh"
	contents = z.json()['script']['script_contents'].encode('utf8')
	contents = contents.replace("\r","")
	target = open(scriptfile, 'w')
	target.write(contents)
	target.close()
	

