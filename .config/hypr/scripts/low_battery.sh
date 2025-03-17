#!/bin/bash

# Get battery information
BATTERY_INFO=$(upower -i $(upower -e | grep BAT))

# Extract battery percentage
BATTERY_PERCENTAGE=$(echo "$BATTERY_INFO" | grep percentage | awk '{print $2}' | tr -d '%')

# Check if power is plugged in
POWER_STATUS=$(echo "$BATTERY_INFO" | grep state | awk '{print $2}')

# Function to send notification
send_notification() {
    notify-send -u critical "Battery Low" "Battery is at $BATTERY_PERCENTAGE%"
}

# Check battery level and send notifications if power is not plugged in
while true; do
    if [ "$POWER_STATUS" != "charging" ]; then
        if [ "$BATTERY_PERCENTAGE" -le 3 ]; then
            ./critical_battery.sh
        if [ "$BATTERY_PERCENTAGE" -le 5 ]; then
            notify-send -u critical "Battery critical" "Battery is at $BATTERY_PERCENTAGE%"
        elif [ "$BATTERY_PERCENTAGE" -le 10 ]; then
            notify-send -u critical "Battery Low" "Battery is at $BATTERY_PERCENTAGE%"

        elif [ "$BATTERY_PERCENTAGE" -le 20 ]; then
            hyprctl notify 0 5000 0 "Low battery: ${BATTERY_PERCENTAGE}%"

        fi
    fi
    sleep 70
done
