#!/bin/sh

pashuapath="/usr/local/saes/Pashua.app/Contents/MacOS/Pashua"


pashua_run() {

    # Write config file
    local pashua_configfile=`/usr/bin/mktemp /tmp/pashua_XXXXXXXXX`
    echo "$1" > "$pashua_configfile"

    if [ "" = "$pashuapath" ]
    then
        >&2 echo "Error: Pashua could not be found"
        exit 1
    fi

    # Get result
    local result=$("$pashuapath" "$pashua_configfile")

    # Remove config file
    rm "$pashua_configfile"

    oldIFS="$IFS"
    IFS=$'\n'

    # Parse result
    for line in $result
    do
        local name=$(echo $line | sed 's/^\([^=]*\)=.*$/\1/')
        local value=$(echo $line | sed 's/^[^=]*=\(.*\)$/\1/')
        eval $name='$value'
    done

    IFS="$oldIFS"
}

REFERENCEDATE=$(date -r /System/Library/CoreServices/XProtect.bundle +%Y%m%d)
CURRENTSYSTEMDATE=$(date +%Y%m%d)

if [ "$CURRENTSYSTEMDATE" -ge "$REFERENCEDATE" ]; then 
    exit 0
else 
    echo "Going into one-time clock set..."

conf="
# Set window title
*.title = Date and Time
*.floating = 1

img.type = image
img.x = 0
img.y = 125
img.maxwidth = 50
img.maxheight = 50
img.path = /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertNoteIcon.icns

# Message
txt.type = text
txt.default = Your current date and time is incorrect. This will result in problems connecting to the network. 
txt.width = 200
txt.x = 60
txt.y = 110

# Date and time picker
d.type = date
d.label = Please set the Date and Time
d.textual = 1
d.date = 1
d.time = 1
"
    pashua_run "$conf" "$customLocation"

    newmonth=$(echo $d | awk '{ print $1 }' | awk -F "-" '{ print $2 }')
    newday=$(echo $d | awk '{ print $1 }' | awk -F "-" '{ print $3 }')
    newyear=$(echo $d | awk '{ print $1 }' | awk -F "-" '{ print $1 }' | cut -c 3-)
    UserSetDate="$(echo $d | awk '{ print $1 }' | awk -F "-" '{ print $2 }'):$(echo $d | awk '{ print $1 }' | awk -F "-" '{ print $3 }'):$(echo $d | awk '{ print $1 }' | awk -F "-" '{ print $1 }' | cut -c 3-)"
    UserSetClock=$(echo $d | awk '{ print $2 }')

    systemsetup -setusingnetworktime off
    systemsetup -setdate $UserSetDate
    systemsetup -settime $UserSetClock
    shutdown -r NOW
fi
