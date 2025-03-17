#!/bin/sh

handle() {
  case $1 in monitoradded*)
	for i in {11..15}
	do
		hyprctl dispatch workspace $i
		hyprctl dispatch moveworkspacetomonitor '$i 1'
	done
  esac
}

socat - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/${HYPRLAND_INSTANCE_SIGNATURE}/.socket2.sock" | while read -r line; do handle "$line"; done
