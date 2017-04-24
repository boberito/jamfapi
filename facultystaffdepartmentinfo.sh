#!/bin/sh

OLDIFS="$IFS"
IFS=$','

#API login info
apiuser='APIUSERNAME'
apipass='APIPASSWORD'
jamfProURL="https://myjamfpro:8443"

#update via serial number
apiURL="JSSResource/computers/serialnumber"
MacSerial=`system_profiler SPHardwareDataType | grep 'Serial Number (system)' | awk '{print $NF}'`

#XML header stuff
xmlHeader="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"

#get current user info from AD
getUser=`ls -l /dev/console | awk '{ print $3 }'`
getRealName=`dscl '/Active Directory/ACADEMIC/All Domains' -read /Users/$getUser RealName | grep -v ":" | tail -1`

#API data load
xmlresult=`curl -k "$jamfProURL/JSSResource/departments" --user "$apiuser:$apipass"  -H "Accept: application/xml" --silent | xmllint --format - | awk -F'>|<' '/<name>/{print $3","}'`


selectedDepartment=`/usr/local/saes/CocoaDialog.app/Contents/MacOS/CocoaDialog dropdown --title "Select Department" --text "Select the Department to assign your computer to:
" --items $xmlresult --button1 "Ok" --float --string-output | awk -F 'Ok' '{print $1}' | tail -1`


apiData="<computer><location><username>$getUser</username><real_name>$getRealName</real_name><department>$selectedDepartment</department></location></computer>"

curl -sSkiu ${apiuser}:${apipass} "${jamfProURL}/${apiURL}/${MacSerial}" \
	-H "Content-Type: text/xml" \
	-d "${xmlHeader}${apiData}" \
	-X PUT > /dev/null


 curl -k -H "Content-Type: text/json" "$jamfProURL/JSSResource/departments" --user "$apiuser:$apipass" | cut -c 18- | rev | cut -c 4- |  rev | awk -F "},{" '{ for (i=1;i<= NF; i++)print $i }' | awk -F ":" '{print $3}'
