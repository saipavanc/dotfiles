#!/bin/bash

# Paramiter one used to set time in sec between reads
sleepDurationSeconds=$1

# read cpu stats to arrays
readarray -t previousStats < <( awk '/^cpu /{flag=1}/^intr/{flag=0}flag' /proc/stat )
sleep $sleepDurationSeconds
readarray -t currentStats < <( awk '/^cpu /{flag=1}/^intr/{flag=0}flag' /proc/stat )

# Declare arrays
declare -A cpu_usage_array
# loop through the arrays
for i in "${!previousStats[@]}"; do
  # Break up arrays 1 line sting into an array element for each item in string
  previousStat_elemant_array=(${previousStats[i]})
  currentStat_elemant_array=(${currentStats[i]})

  # Get all columns from user to steal
  previousStat_colums="${previousStat_elemant_array[@]:1:7}"
  currentStat_colums="${currentStat_elemant_array[@]:1:7}"

  # Replace the column seperator (space) with +
  previous_cpu_sum=$((${previousStat_colums// /+}))
  current_cpu_sum=$((${currentStat_colums// /+}))

  # Get the delta between two reads
  cpu_delta=$((current_cpu_sum - previous_cpu_sum)) 

  # Get the idle time Delta
  cpu_idle=$((currentStat_elemant_array[4]- previousStat_elemant_array[4]))

  # Calc time spent working
  cpu_used=$((cpu_delta - cpu_idle)) 

  # Calc percentage
  cpu_usage=$((100 * cpu_used / cpu_delta))

  # Get cpu used for calc cpu percentage used
  cpu_used_for_calc="${currentStat_elemant_array[0]}"

  if [[ "$cpu_used_for_calc" == "cpu" ]]; then
    # echo "total: "$cpu_usage"%"
    echo $cpu_usage
    # total_cpu_usage=$cpu_usage
  fi
#   else
    # echo $cpu_used_for_calc": "$cpu_usage"%"
    # cpu_usage_array[$cpu_used_for_calc]=$cpu_usage
#   fi

done
