#!/bin/bash
# edgebench/entrypoint.sh
# Docker image entrypoint
# This is (and should be) called from within the image

# Grab the execution platform passed on by the launcher
platform="$1"

# Source the config file
source /app/apps/settings.cfg

### Functions
# Print help message
print_help () {
	echo
	echo "Usage:  ./launcher.sh              for interactive menu"
	echo "    or  ./launcher.sh explore      for interactive shell"
	echo "    or  ./launcher.sh <command>    for direct launch"
	echo
	echo "    commands: listen <app> <app id>,"
	echo "              loop <app> <app id>,"
	echo "              custode <combination>,"
	echo "              spawn <num of tasks> or <algorithm> <timeline>,"
	echo "              device <algorithm> <device id>,"
	echo "              gateway <algorithm> <gateway id>,"
	echo "              profile <app> <arch> <combo> <index> <length>"
	echo "              prepare"
	echo "              log"
	echo
}

# Macro functions
# These are called by the interactive menu
get_app () {
	echo "Select an app:"
	echo "[1] deepspeech"
	echo "[2] facenet"
	echo "[3] lanenet"
	echo "[4] retain"
	read -p "Enter your selection [1, 2, 3, 4]:" option
	echo
	case "$option" in
		"1")	app="deepspeech" ;;
		"2")	app="facenet" ;;
		"3")	app="lanenet" ;;
		"4")	app="retain" ;;
		*)		echo "Please enter a valid selection." ; exit 1 ;;
	esac
}

get_algo () {
	echo "Select an algorithm:"
	echo "[1] Offload None"
	echo "[2] Offload All"
	echo "[3] Oracle"
	echo "[4] DMRM"
	echo "[5] SGRM"
	read -p "Enter your selection [1, 2, 3, 4, 5]:" option
	case "$option" in
		"1")	algorithm="OffloadNone" ;;
		"2")	algorithm="OffloadAll" ;;
		"3")	algorithm="Oracle" ;;
		"4")	algorithm="DMRM" ;;
		"5")	algorithm="SGRM" ;;
		*)		echo "Please enter a valid selection." ; exit 1 ;;
	esac
}

### Direct launch
if [ $# -gt 1 ]; then
	case "$2" in
	"listen")		app="$3"
					id="$4"
					source "${appdir}/start.sh" "$app" "$id"
					;;
	"loop")			app="$3"
					id="$4"
					source "${appdir}/start.sh" "$app" "$id" "loop"
					;;
	"custode")		combination="$3"
					cd "$workers"
					python3 "${workers}/custodian.py" "$combination" "$platform"
					;;
	"spawn")		mode="$3"
					name="$4"
					cd "$workers"
					python3 "${workers}/spawner.py" "$mode" "$name"
					;;
	"device")		algorithm="$3"
					device_id="$4"
					cd "${algodir}/${algorithm}"
					python3 "${algodir}/${algorithm}/device.py" "$device_id"
					;;
	"gateway")		algorithm="$3"
					gateway_id="$4"
					cd "${algodir}/${algorithm}"
					python3 "${algodir}/${algorithm}/gateway.py" "$gateway_id"
					;;
	"log")			cd "$workers"
					python3 "${workers}/logger.py"
					;;
	"prepare")		source "${scripts}/prepare.sh"
					;;
	"profile")		app="$3"
					dev="$4"
					combo="$5"
					index="$6"
					length="$7"
					cd scripts
					python3 "${scripts}/profile.py" "$platform" "$app" "$dev" "$combo" "$index" "$length"
					;;
	*)				source "${scripts}/print_banner.sh" "edgebench"
					print_help
					;;
	esac

### Interactive menu
elif [ $# -eq 1 ]; then
	# Print edgebench banner
	source "${scripts}/print_banner.sh" "edgebench"
	
	#echo
	echo "Welcome!"
	echo "--------------------------------------------------"
	echo "[1] Launch an App Listener"
	echo "[2] Launch an App Listener ad nauseam"
	echo "--------------------------------------------------"
	echo "[3] Launch a Custodian"
	echo "[4] Launch a Spawner"
	echo "[5] Launch a Device Module"
	echo "[6] Launch a Gateway Module"
	echo "[7] Launch a Logger"
	echo "--------------------------------------------------"
	echo "[8] Launch an App Profiler"
	echo "--------------------------------------------------"
	echo "[9] Prepare models, payloads & face database"
	echo "[0] Cleanup"
	echo "--------------------------------------------------"
	read -n1 -p "Enter your selection [0 - 9]:" command
	echo
	
	echo
	case "$command" in
	"1")	get_app
			source "${appdir}/start.sh" "$app" "0"
			;;
	"2")	get_app
			source "${appdir}/start.sh" "$app" "0" "loop"
			;;
	"3")	read -p "Enter your app combo in the form of a,b,c,d:" combination
			python3 "${workers}/custodian.py" "$combination" "$platform"
			;;
	"4")	read -p "Enter the number of tasks you want to spawn:" task_number
			python3 "${workers}/spawner.py" "$task_number"
			;;
	"5")	get_algo
			read -p "Enter your device id:" device_id
			cd "${algodir}/${algorithm}"
			python3 "${algodir}/${algorithm}/device.py" "$device_id"
			;;
	"6")	get_algo
			read -p "Enter your gateway id:" gateway_id
			cd "${algodir}/${algorithm}"
			python3 "${algodir}/${algorithm}/gateway.py" "$gateway_id"
			;;
	"7")	python3 "${workers}/logger.py"
			;;
	"8")	get_app
			read -p "Enter the name of the architecture:" arch
			read -p "Enter the app combo:" combo
			read -p "Enter the app combo index:" index
			read -p "Enter the total app combos:" length
			cd scripts
			python3 "${scripts}/profile.py" "$platform" "$app" "$arch" "$combo" "$index" "$length"
			;;
	"9")	source "${scripts}/prepare.sh"
			;;
	"0")	source "${scripts}/cleanup.sh"
			;;
	*)		echo "Please enter a valid selection! Exiting..."
			;;
	esac
	echo
	
fi
