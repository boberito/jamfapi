#!/bin/sh

#API login info
apiuser='username'
apipass='passowrd'
jamfProURL="https://myjamfpro:8443"

ComputerName=$1
getUser=$2

#update via serial number
apiURL="JSSResource/computers/name"

#XML header stuff
xmlHeader="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"


#API data load
apiData="<computer><location><username>$getUser</username></location></computer>"
curl -sSkiu ${apiuser}:${apipass} "${jamfProURL}/${apiURL}/${ComputerName}" \
	-H "Content-Type: text/xml" \
	-d "${xmlHeader}${apiData}" \
	-X PUT  > /dev/null
	