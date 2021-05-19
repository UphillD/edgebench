#!/bin/bash
# Docker image entrypoint
# This should be called from within the image

# Grab the platform name passed on by the docker image launcher
platform="$1"

# Source the config file
source /app/apps/settings.cfg

# Create the necessary folders in case they don't exist
create_dirs () {
	# Create input dirs
	mkdir -p "${inputs}/deepspeech"
	mkdir -p "${inputs}/facenet"
	mkdir -p "${inputs}/lanenet"
	mkdir -p "${inputs}/retain"
	# Create output dirs
	mkdir -p "${outputs}/deepspeech"
	mkdir -p "${outputs}/facenet"
	mkdir -p "${outputs}/lanenet"
	mkdir -p "${outputs}/retain"
	# Create temp & log dirs
	mkdir -p "$temps"
	mkdir -p "$logs"
}



if [ "$2" = "listen" ]; then

	create_dirs
	
	# Indicate app & app id
	app="$3"
	id="$4"
	
	source "${appdir}/${app}/entrypoint.sh" "listen" "$id"



elif [ "$2" = "custodian" ]; then
	cd "$algodir"
	python3 "${algodir}/custodian.py" "$platform" "$3"

elif [ "$2" = "local" ]; then
	cd "$sgrm"
	python3 "${sgrm}/local.py" "$3"
	
elif [ "$2" = "gateway" ]; then
	cd "$sgrm"
	python3 "${sgrm}/gateway.py" "$3"

elif [ "$2" = "arbiter" ]; then
	cd "$sgrm"
	python3 "${sgrm}/arbiter.py"
	
elif [ "$2" = "spawner" ]; then
	cd "$sgrm"
	python3 "${algodir}/spawner.py"



# Interactive menu
###
### WIP
###
elif [ "$2" = "launch" ]; then
	# Print edgebench banner
	source "${helperdir}"/print_banner.sh edgebench
	
	# Create the directories
	create_dirs

	echo
	echo "Welcome!"
	echo "[1] Launch an app"
	echo "[2] Launch an app listener"
	echo "[3] Launch a Custodian"
	echo "[4] Launch a Spawner"
	echo "[5] Launch an SGRM module"
	echo "[6] Launch an Oracle module (WIP)"
	echo "[8] Download models"
	echo "[9] Cleanup"
	read -n1 -p "Enter your selection [1, 2, 3, 4, 5, 6, 8, 9]:" opt1
	echo

	if [ "$opt1" = "1" ] || [ "$opt1" = "2" ]; then
		echo
		echo "Select an app:"
		echo "[1] deepspeech"
		echo "[2] facenet"
		echo "[3] lanenet"
		echo "[4] retain"
		read -n1 -p "Enter your selection [1, 2, 3, 4]:" opt2
		echo
		
		case "$opt2" in
			"1") app="deepspeech" ;;
			"2") app="facenet" ;;
			"3") app="lanenet" ;;
			"4") app="retain" ;;
		esac
	
	elif [ "$opt1" = "3" ]; then
		echo
		read -n7 -p "Enter your app combo:" opt2
		echo
	
	elif [ "$opt1" = "5" ]; then
		echo
		echo "Select a module:"
		echo "[1] local"
		echo "[2] gateway"
		echo "[3] arbiter"
		read -n1 -p "Enter your selection [1, 2, 3]:" opt2
		echo
		
		if [ "$opt2" = "1" ]; then
			read -n1 -p "Enter your device id:" opt3
		elif [ "$opt2" = "2" ]; then
			read -n1 -p "Enter your gateway id:" opt3
		fi
		
		case "$opt2" in
			"1") module="local" ;;
			"2") module="gateway" ;;
			"3") module="arbiter" ;;
		esac
		
	elif [ "$opt1" = "6" ]; then
		echo
		echo "Select a module:"
		echo "[1] local"
		echo "[2] gateway"
		read -n1 -p "Enter your selection [1, 2]:" opt2
		echo
		
		case "$opt2" in
			"1") module="local" ;;
			"2") module="gateway" ;;
		esac
	fi

#	case "$opt1" in
#		"1") source "${appdir}/${app}/entrypoint.sh" "launch" ;;
#		"2") source "${appdir}/${app}/entrypoint.sh" "listen" ;;
#		"3") python3 "${algodir}/custodian.py" "$platform" "$opt2";;
#		"4") python3 "${algodir}/spawner.py" ;;
#		"5") python3 "${sgrm}/${module}.py" ;;
#		"6")
#		"8") source "/app/helpers/get_models.sh" ;;
#		"9") source "/app/helpers/clean_all.sh" ;;
#		*)   echo "Please enter a valid selection" ;;
#	esac



fi
