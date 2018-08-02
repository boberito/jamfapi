#!/usr/bin/python

#Create an extension attribute
#Create a smart group based off of that extension attribute
#Scope policies or configuration profiles to that smart group.
#Now you have an easy way to toggle that setting on/off for a computer without digging through the JSS

import urllib2
import base64
import json
import sys
import ssl
import urllib
import getpass


def ***REMOVED***(item):
    if sys.argv[1] == "-u":
        return "https://YOURJAMFPROSERVER:8443/JSSResource/users/name/" + item
    elif sys.argv[1] == "-c":
        return "https://YOURJAMFPROSERVER:8443/JSSResource/computers/name/" + item

def PIVAction(url, action):
    jssuser = raw_input("Enter Your JSS Account:")
    jsspass = getpass.getpass("Password: ")
    action = action.lower()
    action = action.capitalize()
    if action == "Enable" or action == "Disable":
        action = action + "d"
    
    if action == "Enabled" or action == "Disabled":
        #Extension Attribute ID and Name may need to be changed
        xmldata = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><computer><extension_attributes><extension_attribute><id>497</id><name>.PIV Enforced</name><type>String</type><value>" + action + "</value></extension_attribute></extension_attributes></computer>"
        
      opener = urllib2.build_opener(urllib2.HTTPSHandler)
        request = urllib2.Request(url, data=xmldata)

        request.add_header('content-type', 'application/xml')
        request.add_header('Authorization', 'Basic ' + base64.b64encode(jssuser + ':' + jsspass))
        request.get_method = lambda: 'PUT'

        response = opener.open(request)
        
        print "PIV Enforcement has been " + action + " for computer " + sys.argv[2]
    
    else:
        print action + " is not an appropriate action."
def computerlist(requestURL):
    jssuser = raw_input("Enter Your JSS Account: ")
    jsspass = getpass.getpass("Password: ")

    request = urllib2.Request(url)
    
    request.add_header('Accept', 'application/json')
    request.add_header('Authorization', 'Basic ' + base64.b64encode(jssuser + ':' + jsspass))

    response = urllib2.urlopen(request)
    response_data = json.loads(response.read())
    print "------------------------------------"
    print "Full Name: " + response_data['user']['full_name']
    print "Email: " + response_data['user']['email_address']
    print "Phone Number: " + response_data['user']['phone_number']
    print "------------------------------------"
    computers = response_data['user']['links']['computers']
    for computer in computers:
        print "Computer: " + computer['name']

if len(sys.argv) > 1:
    options = sys.argv[1]
    if options == "-h":
        print "   -h \t\t\t\t\t List help"
        print "   -u [Username]\t\t\t List the computers assigned to the user"
        print "   -c [Computer] [enabled/disabled]\t Computer to enable/disable Forced PIV"

    elif options == "-u":
        if len(sys.argv) > 2:
            url = ***REMOVED***(sys.argv[2])
            computerlist(url)
        else:
            print "No username inputted"
    elif options == "-c":
        if len(sys.argv)  > 3:
            PIVAction(***REMOVED***(sys.argv[2]), sys.argv[3])
        else:
            print "Missing either computer or action"
    else:
        print "Command not found"
else:
    print "   -h \t\t\t\t\t List help"
    print "   -u [Username]\t\t\t List the computers assigned to the user"
    print "   -c [Computer] [enabled/disabled]\t Computer to enable/disable Forced PIV"
    
