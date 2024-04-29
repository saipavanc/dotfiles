#!/usr/bin/env bash


# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Script file to manage hyprctl workspaces, and limit movement in persistent workspaces of the current screen. Uses split-monitor-workspaces plugin for hyprland."
   echo
   echo "Syntax: persistent_workspaces [-h|-n|-s]"
   echo "options:"
   echo "-h     
   Print this Help."
   echo "-n     
   Go to next workspace if it exists in the persistent workspaces of the current monitor."
   echo "-s <workspace_id>
   Switch to the workspace with id <workspace_id>, if it exists in the persistent_workspaces of the current monitor."
   echo
}

current_monitor_id=$(hyprctl activeworkspace -j | jq '.monitorID')
number_of_workspaces=$(hyprctl workspaces -j | jq -c '.[] | select(.monitorID=='$current_monitor_id')' | wc -l)

max_workspace_id=$number_of_workspaces
if [[ $current_monitor_id == 1 ]];
then
max_workspace_id=$(($max_workspace_id + 10))
fi 

current_workspace_id=$(hyprctl activeworkspace -j | jq '.id')
 
workspace_in_persistent_workspaces=0
if [[ $current_workspace_id -lt $max_workspace_id ]]; then workspace_in_persistent_workspaces=1; fi

echo $workspace_in_persistent_workspaces, $max_workspace_id, $number_of_workspaces
# Get the options
OPTSTRING=":hns:i"
while getopts ${OPTSTRING} option; do
   case $option in
      h) # display Help
        Help
        exit;;
      n) # move to next workspace
		if [[ $workspace_in_persistent_workspaces == 1 ]]; then hyprctl dispatch split-workspace r+1; fi
		exit;;
	  s) # switch to the workspace given in argument 
		if [[ $OPTARG -le $number_of_workspaces ]]; then hyprctl dispatch split-workspace $OPTARG; fi
		exit;;
     i) # initiate workspaces
      # initialize all the workspaces
      for N in {1..15}; do hyprctl dispatch workspace $N; done; notify-send "Workspaces initiated!"
      exit;;	
	  \?) # invalid option
	 	echo "Invlaid option"
	 	exit;;
   esac
done