#!/bin/sh

#API login info
apiuser="USERNAME"
apipass='PASSWORD'
jamfProURL="https://jamfproserver:8443"

ComputerName=$(hostname)

#update group with ID 232 aka group you want
GroupID="1234"
apiURL="JSSResource/computergroups/id/${GroupID}"

#XML header stuff
xmlHeader="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"

apiData="<computer_group><id>${GroupID}</id><name>Whatever the GroupName Is</name><computer_additions><computer><name>$ComputerName</name></computer></computer_additions></computer_group>"

curl -sSkiu ${apiuser}:${apipass} "${jamfProURL}/${apiURL}" \
    -H "Content-Type: text/xml" \
    -d "${xmlHeader}${apiData}" \
    -X PUT  > /dev/null
