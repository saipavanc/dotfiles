rofi() {
    exec command ${=ROFI:-rofi} -theme light "$@"
}

display_message() {
    rofi -e "$1" &
    MESSAGE_PID=$!
}

dismiss_message() {
    if [[ $MESSAGE_PID ]]; then
        kill "$MESSAGE_PID"
        unset MESSAGE_PID
    fi
}

change_brightness() {
    local change="$1" i b
    local -a new_brightness_levels

    for i in {1..$#BRIGHTNESS_LEVELS}; do
        b=$((${BRIGHTNESS_LEVELS[$i]} + change))
        (( b < 0 || b > 100 )) && return
        new_brightness_levels+=("$b")
    done

    display_message "Setting brightness..."
    for i in {1..$#new_brightness_levels}; do
        sudo ddcutil -d "$i" setvcp 10 "${new_brightness_levels[$i]}"
    done
    BRIGHTNESS_LEVELS=($new_brightness_levels)
    AVERAGE_BRIGHTNESS=$(((${(j:+:)BRIGHTNESS_LEVELS}) / $#BRIGHTNESS_LEVELS))
    dismiss_message
}

display_message "Reading current brightness levels..."
BRIGHTNESS_LEVELS=("${(@f)$(sudo ddcutil detect | awk '/^Display/ { print $2 }' | xargs -I{} sudo ddcutil --brief -d {} getvcp 10 | awk '{ print $4 }')}")
AVERAGE_BRIGHTNESS=$(((${(j:+:)BRIGHTNESS_LEVELS}) / $#BRIGHTNESS_LEVELS))
dismiss_message

while print "+10\n+5\n+1\n0\n-1\n-5\n-10" | rofi -dmenu -p brightness -mesg "<b>Current: ${AVERAGE_BRIGHTNESS}</b>" -selected-row 3 | read choice; do
    if [[ $choice == '0' ]]; then
        exit
    elif [[ $choice =~ '^[0-9]+$' ]]; then
        change_brightness $((choice - AVERAGE_BRIGHTNESS))
    elif [[ $choice =~ '^[+-][0-9]+$' ]]; then
        change_brightness $choice
    else
        rofi -e "Unsupported choice: '$choice'"
    fi
done
