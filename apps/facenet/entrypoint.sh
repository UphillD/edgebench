#!/bin/bash
# Entrypoint for facenet benchmark

# Source config file
source /app/apps/settings.cfg

# Enter benchmark directory
cd "${appdir}/facenet"

# Print banner
source "${helpers}/print_banner.sh" "facenet"



# Launch one time inference
if [ "$1" = "launch" ]; then
	echo "Launching one-time inference for facenet..."
	temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	cp "${payloads}/facenet/payload.jpg" "${inputs}/facenet/payload.jpg"
	python3.7 contributed/cluster_2.py 	"${models}/facenet/" \
										"${inputs}/facenet/" \
										"${outputs}/facenet/" \
										"${temp_f}"
	rm -f "${inputs}/facenet/payload.jpg"

# Launch listener
elif [ "$1" = "listen" ]; then
    echo "Launching listener for facenet..."

	if [ "$2" == "0" ]; then
		input_f="${inputs}/facenet/"
		output_f="${outputs}/facenet/"
		temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
		
		python3.7 infer.py	"${models}/facenet/" \
							"${input_f}" \
							"${output_f}" \
							"${temp_f}"
	else
		mkdir -p "${workdir}/app_${2}"
		chmod -R 777 "${workdir}/app_${2}"
		input_f="${workdir}/app_${2}"
		output_f="${workdir}/app_${2}"
		temp_f="${workdir}/app_${2}/exec.tmp"

		python3.7 infer.py	"${models}/facenet/" \
							"${input_f}" \
							"${output_f}" \
							"${temp_f}"
    fi
    
fi
