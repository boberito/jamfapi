#!/bin/sh

#API login info
apiuser='username'
apipass='password'
jamfProURL="https://myjamfpro:8443"

ComputerName=`hostname`

#update via serial number
#moves them into the static group
apiURL="JSSResource/computergroups/id/232"

#XML header stuff
xmlHeader="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"

apiData="<computer_group>
<id>232</id>
<name>SonicWall Mobile Connect</name>
<computers>
<computer>
<name>$ComputerName</name>
</computer>
</computers>
</computer_group>"

curl -sSkiu ${apiuser}:${apipass} "${jamfProURL}/${apiURL}" \
	-H "Content-Type: text/xml" \
	-d "${xmlHeader}${apiData}" \
	-X PUT  > /dev/null
