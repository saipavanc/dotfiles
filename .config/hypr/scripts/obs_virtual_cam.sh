#!/usr/bin/env bash

case "$(pidof obs | wc -l)" in

0)  notify-send "Starting OBS virtual cam for screen share..."
    obs --startvirtualcam --minimize-to-tray
    ;;
1)  notify-send "Stopping OBS virtual cam."
	kill -2 $(pidof obs)
    ;;
*)  echo "Invalid option"
    ;;
esac
