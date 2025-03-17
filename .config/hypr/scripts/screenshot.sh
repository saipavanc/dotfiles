#!/bin/bash

active_window() {
    active_window_class=$(hyprctl -j activewindow | jq -r '(.class)')
    screenshot_filename="$HOME/Pictures/screenshots/$(date +"%d-%m-%Y-%H%S")-$active_window_class.png"

    hyprctl -j activewindow | jq -r '"\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"' | grim -g - $screenshot_filename

    echo "Screenshot saved as $screenshot_filename"
}

region() {
    grim -g "$(slurp -w 0)" - | swappy -f -
}

active_monitor() {
    local output_file="${1:-screenshot_$(date +%Y%m%d_%H%M%S).png}"
    local current_monitor=$(hyprctl monitors -j | jq -r '.[] | select(.focused == true).name')

    grim -o "$current_monitor" "$output_file"

    echo "Screenshot of current monitor saved as $output_file"
}

# Check if a function name is provided as an argument
if [ "$1" = "active" ]; then
    active_window "$2"
elif [ "$1" = "monitor" ]; then
    active_monitor "$2"
elif [ "$1" = "region" ]; then
    region
else
    echo "Usage: $0 [active|monitor|region] [output_file]"
    exit 1
fi
