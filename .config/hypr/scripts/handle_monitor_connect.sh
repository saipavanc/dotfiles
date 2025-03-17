#!/bin/sh

handle() {
  case $1 in monitoradded*)
    for i in {11..15}; do
      hyprctl dispatch workspace $i
      hyprctl dispatch moveworkspacetomonitor '$i 1'
    done
    ;;
  esac
  # restart fabric widgets
  #fabric-cli exec bar "app.quit()"
  #sleep 1 && python ~/dotfiles/fabric-bar/fabric_bar.py &
  #   sleep 2
  #   python $HOME/dotfiles/fabric-bar/refresh.py
}

socat - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/${HYPRLAND_INSTANCE_SIGNATURE}/.socket2.sock" | while read -r line; do handle "$line"; done
