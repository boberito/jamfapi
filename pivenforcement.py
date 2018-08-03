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
import getpass
import os
import subprocess

def login():
    jssuser = raw_input("Enter Your JSS Account:")
    jsspass = getpass.getpass("Password: ")
    return {'user':jssuser, 'pass':jsspass}

#Function to build the Jamf Pro Classic API URL Request
def ***REMOVED***(arg, item):
    #if enrolled, use the current jamf server or set the server below
    #example jamfproserver = "https://YOURJAMFPROSERVER:8443/"
    #if set to nothing, and it finds the jamf.plist then use the enrolled server
    jamfproserver = ""
    pref_path = "/Library/Preferences/com.jamfsoftware.jamf.plist"
    if os.path.exists(pref_path) is True and jamfproserver == "":
        command = "defaults read " + pref_path + " jss_url"
        jamfproserver = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    
    if arg == "-u":
        jamfproserver = jamfproserver[:-1] + "JSSResource/users/name/" + item
        return jamfproserver 
    elif arg == "-c":
        jamfproserver = jamfproserver[:-1] + "JSSResource/computers/name/" + item
        return jamfproserver

#If you are enabling or disabling function
def PIVAction(url, action, credentials="MISSING"):
    if credentials == "MISSING":
        credentials = login()

    #makes sure everything is the same case
    action = action.lower()
    action = action.capitalize()
    #script is nice and fixes your mistake
    if action == "Enable" or action == "Disable":
        action = action + "d"
    
    if action == "Enabled" or action == "Disabled":
        #####
        #Extension Attribute ID and Name WILL need to be changed
        #Set EA_ID and EA_name
        #####
        EA_ID = "497"
        EA_name = ".PIV Enforced"
        ##### 
        xmldata = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><computer><extension_attributes><extension_attribute><id>" + EA_ID + "</id><name>" + EA_name + "</name><type>String</type><value>" + action + "</value></extension_attribute></extension_attributes></computer>"     
        
        try:
            opener = urllib2.build_opener(urllib2.HTTPSHandler)
            request = urllib2.Request(url, data=xmldata)

            request.add_header('content-type', 'application/xml')
            request.add_header('Authorization', 'Basic ' + base64.b64encode(credentials['user'] + ':' + credentials['pass']))
            request.get_method = lambda: 'PUT'

            response = opener.open(request)
            if response.getcode() != "200":
                computer = url.split("/", 6)
                print "PIV Enforcement has been " + action + " for computer " + computer[6]
            else:
                print "Something went wrong"

        except urllib2.URLError, error:
            #ERROR Checking, returns HTTP Error Codes     
            print "Something went wrong.\n", error
            return error.code

    else:
        print action + " is not an appropriate action."


#if you enter the user it will display the computers assigned to that user
def computerlist(requestURL, credentials="MISSING"):
    if credentials == "MISSING":
        credentials = login()
    try:
        request = urllib2.Request(requestURL)   
        request.add_header('Accept', 'application/json')
        request.add_header('Authorization', 'Basic ' + base64.b64encode(credentials['user'] + ':' + credentials['pass']))
        response = urllib2.urlopen(request)

        if response.getcode() != "200":
            response_data = json.loads(response.read())
            print "-----------------------------------------------"
            print "|\tFull Name: " + response_data['user']['full_name']
            print "|\tEmail: " + response_data['user']['email_address']
            print "|\tPhone Number: " + response_data['user']['phone_number']
            print "-----------------------------------------------"
            computers = response_data['user']['links']['computers']
            for computer in computers:
                print "|\tComputer: " + computer['name']
            print "-----------------------------------------------"
        return response.getcode()
    except urllib2.URLError, error:
            #ERROR Checking, returns HTTP Error Codes
            print "Something went wrong.\n", error
            return error.code
    
    
#Main Function        
def main():
    if len(sys.argv) > 1:
        options = sys.argv[1]
        if options == "-h":
            print "   -h \t\t\t\t\t List help"
            print "   -u [Username]\t\t\t List the computers assigned to the user"
            print "   -c [Computer] [enabled/disabled]\t Computer to enable/disable Forced PIV"

        elif options == "-u":
            if len(sys.argv) > 2:
                url = ***REMOVED***(options, sys.argv[2])
                computerlist(url)
            else:
                print "----------------------------"
                print "*** No username inputted ***"
                print "----------------------------"
        elif options == "-c":
            if len(sys.argv)  > 3:
                PIVAction(***REMOVED***(options, sys.argv[2]), sys.argv[3])
            else:
                print "------------------------------"
                print "*** Missing item or action ***"
                print "------------------------------"
        else:
            print "Command not found"
    else:
        print "Interactive Mode!"
        print "------------------------------------"
        #INTERACTIVE MODE BEGINS
        apilogin = "MISSING"
        print ""        
        print "   -h \t\t\t\t\t List help"
        print "   -u [Username]\t\t\t List the computers assigned to the user"
        print "   -c [Computer] [enabled/disabled]\t Computer to enable/disable Forced PIV"
        print "   quit\t\t\t\t\t Type \'quit\' to quit interactive mode"

        while True:

            user_input = raw_input("Please enter an option: ")
            if user_input.strip().lower() == "quit" or user_input.strip().lower() == "q":
                break
            
            the_input = user_input.split(" ", 3)
            the_input += [None] * (3 - len(the_input))
            options, item, action = the_input
            action = str(action)
            if options == "-h":
                print "   -h \t\t\t\t\t List help"
                print "   -u [Username]\t\t\t List the computers assigned to the user"
                print "   -c [Computer] [enabled/disabled]\t Computer to enable/disable Forced PIV"
                print "   quit\t\t\t\t\t Type \'quit\' to quit interactive mode"
            elif options == "-u":
                if item == None:
                    print "----------------------------"
                    print "*** No username inputted ***"
                    print "----------------------------"
                else:
                    if apilogin == "MISSING":
                        apilogin = login()

                    url = ***REMOVED***(options, item)
                    print url
                    Notsuccessful = str(computerlist(url, apilogin))
                    if Notsuccessful == "401":
                        apilogin = "MISSING"
            
            elif options == "-c":
                if item == None:
                    print "--------------------"
                    print "*** Missing item ***"
                    print "--------------------"
                else:
                    print action
                    if action == "None":
                        print "----------------------"
                        print "*** Missing action ***"
                        print "----------------------"
                    else:
                        if apilogin == "MISSING":
                            apilogin = login()

                        Notsuccessful = str(PIVAction(***REMOVED***(options, item), action, apilogin))
                    
                        if Notsuccessful == "401":
                            apilogin = "MISSING"
            else:
                print "-------------------------"
                print "*** Command not found ***"
                print "-------------------------"

if __name__== "__main__":
  main()
