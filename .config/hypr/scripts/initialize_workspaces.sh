#!/usr/bin/bash

INTERNAL_MONITOR="eDP"  # Replace with your internal monitor name
EXTERNAL_MONITOR="HDMI-A-1" # Replace with your external monitor name

# Check if external monitor is disconnected
if xrandr | grep -q "$EXTERNAL_MONITOR connected"; then
	hyprctl dispatch focusmonitor HDMI-A-1

	for i in {11..15}
	do
		hyprctl dispatch workspace $i
	done
	hyprctl dispatch workspace 11
fi

# initialize workspaces on the default monitor
hyprctl dispatch focusmonitor eDP-1

for i in {1..10}
do
	hyprctl dispatch workspace $i
done
# switch to the first workspace after init
hyprctl dispatch workspace 1
