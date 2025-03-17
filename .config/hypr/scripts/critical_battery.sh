#!/bin/bash

# Function to hibernate the system
hibernate() {
    systemctl hibernate
}

# Function to show notification and handle user response
show_notification() {
    local pid
    coproc { notify-send -t 60000 -u critical -i system-hibernate "System Hibernation" "Your system will hibernate in 60 seconds.\nClick to cancel." --action="stop=Stop"; }
    pid=$!

    # Wait for user response or timeout
    if read -t 60 response <&${COPROC[0]}; then
        echo $response
        if [ "$response" = "stop" ]; then
            notify-send -t 5000 "Hibernation Cancelled" "The system will not hibernate."
            return 1
        fi
    fi
    return 0
}

# Main script
if show_notification; then
    hibernate
fi

