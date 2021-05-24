#!/bin/bash
# Entrypoint for lanenet benchmark

# Source settings file
source /app/apps/settings.cfg

# Enter directory
cd "${appdir}/lanenet"

# Print banner
source "${scripts}/print_banner.sh" "lanenet"



# Launch one time inference
if [ "$1" = "launch" ]; then
	echo "Launching one-time inference for lanenet..."
	temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	cp "${payloads}/lanenet/payload.jpg" "${inputs}/lanenet/payload.jpg"
	time python3.7 infer.py	--image_dir "${inputs}/lanenet/" \
							--weights_path "${models}/lanenet/tusimple_lanenet.ckpt" \
							--save_dir "${outputs}/lanenet/" \
							--temp_file "${temp_f}"
	
	rm -f "${inputs}/lanenet/payload.jpg"



# Launch listener
elif [ "$1" = "listen" ]; then
    echo "Launching listener for lanenet..."
    
	if [ "$2" = "0" ]; then
		input_f="${inputs}/lanenet"
		output_f="${outputs}/lanenet"
		temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	else
		mkdir -p "${workdir}/app_${2}"
		chmod -R 777 "${workdir}/app_${2}"
		input_f="${workdir}/app_${2}"
		output_f="${workdir}/app_${2}"
		temp_f="${workdir}/app_${2}/exec.tmp"
    fi
    
	time python3.7 infer.py	--image_dir "${input_f}/" \
							--weights_path "${models}/lanenet/tusimple_lanenet.ckpt" \
							--save_dir "${output_f}" \
							--temp_file "${temp_f}"
fi
