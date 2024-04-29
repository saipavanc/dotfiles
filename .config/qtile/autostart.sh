#!/bin/bash
#   ___ _____ ___ _     _____   ____  _             _    
#  / _ \_   _|_ _| |   | ____| / ___|| |_ __ _ _ __| |_  
# | | | || |  | || |   |  _|   \___ \| __/ _` | '__| __| 
# | |_| || |  | || |___| |___   ___) | || (_| | |  | |_  
#  \__\_\|_| |___|_____|_____| |____/ \__\__,_|_|   \__| 
#                                                        
#  
# by Stephan Raabe (2023) 
# ----------------------------------------------------- 

# My screen resolution
# xrandr --rate 120

# For Virtual Machine 
# xrandr --output Virtual-1 --mode 1920x1080

# start kwallet
/usr/lib/pam_kwallet_init &

# Keyboard layout
setxkbmap us

# Load picom
picom &

# Load power manager
xfsettingsd &
xfce4-power-manager &
nm-applet &
# xfce4-session &
# xfce4-panel -d &
# Load notification service
# dunst &
# dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP &

# touchpad gestures
fusuma &

# Setup Wallpaper and update colors
~/dotfiles/qtile/scripts/wallpaper.sh init

# setup ags widgets
ags &

# startup applications
/usr/bin/kdeconnect-indicator &
