#!/bin/sh

#API login info
apiuser='username'
apipass='password'
jamfProURL="https://myjamfpro:8443"

ComputerName=$1
getUser=$2

#update via serial number
apiURL="JSSResource/computers/name"

#XML header stuff
xmlHeader="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"


#API data load
#apiData="<computer><location><username>$getUser</username></location></computer>"

apiData="{
  \"computer\": {
    
    \"extension_attributes\": [
      
      {
        \"id\": 69,
        \"name\": \"Availability\",
        \"type\": \"String\",
        \"value\": \"Yes\"
      },
      {
        \"id\": 67,
        \"name\": \"DateOut\",
        \"type\": \"Date\",
        \"value\": \"11/26/81\"
      },
      {
        \"id\": 68,
        \"name\": \"DateReturned\",
        \"type\": \"Date\",
        \"value\": \"11/26/81\"
      }
      
    ]
 }   
}"

curl -sSkiu ${apiuser}:${apipass} "${jamfProURL}/${apiURL}/${ComputerName}" \
	-H "Content-Type: text/xml" \
	-d "${xmlHeader}${apiData}" \
	-X PUT  > /dev/null
	