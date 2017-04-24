#!/bin/sh

#API login info
apiuser=''
apipass=''
jamfProURL=""

#update via serial number
apiURL="JSSResource/computers/serialnumber"
MacSerial=`system_profiler SPHardwareDataType | grep 'Serial Number (system)' | awk '{print $NF}'`

#XML header stuff
xmlHeader="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"

#get current user info from AD
getUser=`ls -l /dev/console | awk '{ print $3 }'`
getclass=`dscl '/Active Directory/ACADEMIC/All Domains' -read /Users/$getUser dsAttrTypeNative:distinguishedName | awk '{ FS=","; print $2 }' | awk '{ FS="="; print $2 }' | tail -1`
getRealName=`dscl '/Active Directory/ACADEMIC/All Domains' -read /Users/$getUser RealName | grep -v ":"`

#API data load
apiData="<computer><location><username>$getUser</username><real_name>$getRealName</real_name><department>$getclass</department></location></computer>"
curl -sSkiu ${apiuser}:${apipass} "${jamfProURL}/${apiURL}/${MacSerial}" \
	-H "Content-Type: text/xml" \
	-d "${xmlHeader}${apiData}" \
	-X PUT  > /dev/null
	

#Old Way	
#jamf recon -endUsername $getUser -department "$getclass" -building "Postoak" -realname "$getRealName" -email "$getUser@saes.org"

