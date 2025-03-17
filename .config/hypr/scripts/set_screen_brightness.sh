#!/bin/bash

set_screen_brightness() {
    output=$1
    changetype=$2
    change=$3

    if [ "$output" == "0" ]; then
        if [ "$changetype" == "dec" ];then
	    brightnessctl s $change-
    	elif [ "$changetype" == "set" ];then
	    brightnessctl s "$change"
    	elif [ "$changetype" == "inc" ];then
	    brightnessctl s $change+
	fi
    else
        # Get current brightness
        current=$(ddcutil getvcp 10 -t -d $output | cut -d' ' -f4)
        
        # Calculate new brightness
        if [[ "$changetype" == "inc" ]]; then
		ddcutil -d $output setvcp 10 + $change
        elif [[ "$changetype" == "dec" ]]; then
		ddcutil -d $output setvcp 10 - $change 
        else
		ddcutil -d $output setvcp 10 $change
        fi
    fi
}

# Check if correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <output> <brightness_change>"
    echo "Example: $0 1 inc 10, to change the first display brightness using ddcutil"
    echo "$0 0 inc 5%, to change the laptop display brightness using xbacklight"
    exit 1
fi

set_screen_brightness "$1" "$2" "$3"

