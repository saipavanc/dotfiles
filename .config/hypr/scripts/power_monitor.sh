#!/bin/bash

# run the low_battery.sh script
pidof -x low_battery.sh || $HOME/.config/hypr/scripts/low_battery.sh &

is_plugged_old_state=$(systemd-ac-power)

while true; do
    if $(systemd-ac-power); then
#         echo plugged
        is_plugged_old_state="yes"
        # Charger is plugged in
        sleep 5  # Check every 5 seconds
    else
        if [ "$is_plugged_old_state" = "yes" ]; then
            # only restart the script if it was plugged before
            pkill -f "low_battery.sh"
            $HOME/.config/hypr/scripts/low_battery.sh &
        fi
        is_plugged_old_state="no"
#         echo unplugged
        sleep 5
    fi
done
