#!/bin/bash
# edgebench - launcher.sh
# Docker image entrypoint
# This should be called from within the image

# Grab the execution platform passed on by the launcher
platform="$1"

# Source the config file
source /app/apps/settings.cfg

# Set permissions
chmod -R 777 *

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
	"custodian")	combination="$3"
					cd "$algodir"
					python3 "${algodir}/custodian.py" "$platform" "$combination"
					;;
	"spawner")		task_number="$3"
					cd "$algodir"
					python3 "${algodir}/spawner.py" "$task_number"
					;;
	"device")		algorithm="$3"
					device_id="$4"
					cd "${algodir}/${algorithm}"
					python3 "${algodir}/${algorithm}/device.py" "$platform" "$device_id"
					;;
	"gateway")		algorithm="$3"
					gateway_id="$4"
					cd "${algodir}/${algorithm}"
					python3 "${algodir}/${algorithm}/gateway.py" "$platform" "$gateway_id"
					;;
	"logger")		cd "${algodir}/${algorithm}"
					python3 "${algodir}/${algorithm}/logger.py"
					;;
	"prepare")		source "${scripts}/prepare.sh"
					;;
	"profile")		app="$3"
					dev="$4"
					cd scripts
					python3 "${scripts}/profiler.py" "$platform" "$app" "$dev"
					;;
	*)				print_help
					;;
	esac

###
# Interactive menu
###
elif [ $# -eq 1 ]; then
	# Print edgebench banner
	source "${scripts}/print_banner.sh" "edgebench"
	
	echo
	echo "Welcome!"
	echo "[1] Launch an app"
	echo "[2] Launch an app listener"
	echo "[3] Launch a Custodian"
	echo "[4] Launch a Spawner"
	echo "[5] Launch a device module"
	echo "[6] Launch a gateway module"
	echo "[7] Prepare models, payloads & face database"
	echo "[0] Cleanup"
	read -n1 -p "Enter your selection [0 - 7]:" command
	echo

	# Command specific settings
	if [ "$command" = "1" ] || [ "$command" = "2" ]; then
		echo
		echo "Select an app:"
		echo "[1] deepspeech"
		echo "[2] facenet"
		echo "[3] lanenet"
		echo "[4] retain"
		read -n1 -p "Enter your selection [1, 2, 3, 4]:" option
		echo
		
		case "$option" in
			"1") app="deepspeech" ;;
			"2") app="facenet" ;;
			"3") app="lanenet" ;;
			"4") app="retain" ;;
		esac
	elif [ "$command" = "3" ]; then
		echo
		read -p "Enter your app combo in the form of a,b,c,d:" combination
		echo
	elif [ "$command" = "4" ]; then
		echo
		read -p "Enter the number of tasks you want to spawn:" task_number
		echo
	elif [ "$command" = "5" ]; then
		echo
		echo "Select an algorithm:"
		echo "[1] SGRM"
		echo "[2] Oracle"
		echo "[3] NoOffload"
		read -n1 -p "Enter your selection [1, 2, 3]:" option
		echo
		case "$option" in
			"1") algorithm="SGRM" ;;
			"2") algorithm="Oracle" ;;
			"3") algorithm="NoOffload" ;;
		esac
		read -n1 -p "Enter your device id:" device_id
		echo
	elif [ "$command" = "6" ]; then
		echo
		echo "Select an algorithm:"
		echo "[1] SGRM"
		echo "[2] Oracle"
		read -n1 -p "Enter your selection [1, 2]:" option
		echo
		case "$opt2" in
			"1") algorithm="SGRM" ;;
			"2") algorithm="Oracle" ;;
		esac
		read -n1 -p "Enter your gateway id:" gateway_id
		echo
	fi
	
	case "$command" in
		"1") source "${appdir}/${app}/entrypoint.sh" "launch" ;;
		"2") source "${appdir}/${app}/entrypoint.sh" "listen" ;;
		"3") python3 "${algodir}/custodian.py" "$platform" "$combination" ;;
		"4") python3 "${algodir}/spawner.py" "$task_number" ;;
		"5") python3 "${algodir}/${algorithm}/device.py" "$device_id" ;;
		"6") python3 "${algodir}/${algorithm}/gateway.py" "$gateway_id" ;;
		"7") source "${scripts}/prepare.sh" ;;
		"0") source "${scripts}/clean_all.sh" ;;
		*)   echo "Please enter a valid selection!" ;;
	esac
fi
