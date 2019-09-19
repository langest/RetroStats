#!/bin/bash
function ask_choice() {
	local text="$1"
	shift
	local options=()
	local choice
	local opt
	local i

	[[ "$#" -eq 0 ]] && return 1

	i=1
	for opt in "$@"; do
		options+=( "$i" "$opt" )
		((i++))
	done
	choice=$(dialog --menu "$text" 22 86 16 "${options[@]}" 2>&1 >/dev/tty) || exit 1


	echo "${options[choice*2-1]}"
}

function choose_system() {
	system=$(ask_choice "Choose system" all $(ls /home/pi/roms)) || exit 1
	if [ "$system" = "all" ]; then
		echo ""
	else
		echo -s $system
	fi
}

function choose_criteria() {
	criteria=$(ask_choice "Choose criteria" \
		"Time Played" \
		"Number of Times Played" \
		"Average Session" \
		"Median Session") || exit 1
	case $criteria in
		"Time Played")
			echo -c total
			;;
		"Number of Times Played")
			echo -c times
			;;
		"Average Session")
			echo -c average
			;;
		"Median Session")
			echo -c median
			;;
	esac
}
