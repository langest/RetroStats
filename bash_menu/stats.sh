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
