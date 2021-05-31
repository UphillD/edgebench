#!/bin/bash
# edgebench/scripts/print_banner.sh
# Prints banners

# all designs are from https://patorjk.com/software/taag/

# Print help
if [ $# -eq 0 ]; then
	echo "Not enough arguments!"
	echo
	echo "Usage:  ./print_banner.sh <app>"
	echo 
	echo "  apps: edgebench, deepspeech, facenet, lanenet, retain"
	echo
	exit 1;
fi

if [ "$1" = "edgebench" ]; then
	# Big ASCII scheme
	clear
	printf "\e[1;36m%s\e[m\n" $'          _            _                     _     ';    sleep 0.2
	printf "\e[1;36m%s\e[m\n" $'  ___  __| | __ _  ___| |__   ___ _ __   ___| |__  ';    sleep 0.2
	printf "\e[1;36m%s\e[m\n" $' / _ \/ _` |/ _` |/ _ \ \'_ \ / _ \ \'_ \ / __| \'_ \ '; sleep 0.2
	printf "\e[1;36m%s\e[m\n" $'|  __/ (_| | (_| |  __/ |_) |  __/ | | | (__| | | |';    sleep 0.2
	printf "\e[1;36m%s\e[m\n" $' \___|\__,_|\__, |\___|_.__/ \___|_| |_|\___|_| |_|';    sleep 0.2
	printf "\e[1;36m%s\e[m\n" $'            |___/                                  ';    sleep 0.2
elif [ "$1" = "deepspeech" ]; then
	# threepoint ASCII scheme
	clear
	printf "\e[1;35m%s\e[m\n" $' _| _  _  _  _ _  _  _  _|_ '; sleep 0.2
	printf "\e[1;35m%s\e[m\n" $'(_|(/_(/_|_)_\|_)(/_(/_(_| |'; sleep 0.2
	printf "\e[1;35m%s\e[m\n" $'         |    |             '; sleep 0.2
	echo
elif [ "$1" = "facenet" ]; then
	# Elite ASCII scheme
	clear
	printf "\e[0;34m%s\e[m\n" $'·▄▄▄ ▄▄▄·  ▄▄· ▄▄▄ . ▐ ▄ ▄▄▄ .▄▄▄▄▄'; sleep 0.2
	printf "\e[0;34m%s\e[m\n" $'▐▄▄·▐█ ▀█ ▐█ ▌▪▀▄.▀·•█▌▐█▀▄.▀·•██  '; sleep 0.2
	printf "\e[0;34m%s\e[m\n" $'██▪ ▄█▀▀█ ██ ▄▄▐▀▀▪▄▐█▐▐▌▐▀▀▪▄ ▐█.▪'; sleep 0.2
	printf "\e[0;34m%s\e[m\n" $'██▌.▐█ ▪▐▌▐███▌▐█▄▄▌██▐█▌▐█▄▄▌ ▐█▌·'; sleep 0.2
	printf "\e[0;34m%s\e[m\n" $'▀▀▀  ▀  ▀ ·▀▀▀  ▀▀▀ ▀▀ █▪ ▀▀▀  ▀▀▀ '; sleep 0.2
	echo
elif [ "$1" = "lanenet" ]; then
	# bigchief ASCII scheme
	clear
	printf "\e[0;37m%s\e[m\n" $' __                                 __   '; sleep 0.2
	printf "\e[0;37m%s\e[m\n" $'|  |.---.-.-----.-----.-----.-----.|  |_ '; sleep 0.2
	printf "\e[0;37m%s\e[m\n" $'|  ||  _  |     |  -__|     |  -__||   _|'; sleep 0.2
	printf "\e[0;37m%s\e[m\n" $'|__||___._|__|__|_____|__|__|_____||____|'; sleep 0.2
	echo
elif [ "$1" = "retain" ]; then
	# JS Bracket Letters ASCII scheme
	clear
	printf "\e[1;32m%s\e[m\n" $'.----. .----..---.  .--.  .-..-. .-.'; sleep 0.2
	printf "\e[1;32m%s\e[m\n" $'| {}  }| {_ {_   _}/ {} \ | ||  `| |'; sleep 0.2
	printf "\e[1;32m%s\e[m\n" $'| .-. \| {__  | | /  /\  \| || |\  |'; sleep 0.2
	printf "\e[1;32m%s\e[m\n" $'`-\' `-\'`----\' `-\' `-\'  `-\'`-\'`-\' `-\''; sleep 0.2
	echo
fi












