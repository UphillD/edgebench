#!/bin/bash
# Entrypoint for deepspeech app

# Source config file
source /app/apps/settings.cfg

# Enter app directory
cd "${appdir}/deepspeech"

# Print banner
source "${scripts}/print_banner.sh" "deepspeech"

# Set appropriate model depending on architecture
# note that the variable "$platform" is passed on 
#   in the docker container by the original launcher.sh
if [ "$platform" = "amd64" ]; then
	modeltype="pbmm"
else
	modeltype="tflite"
fi



# Launch one time inference
if [ "$1" = "launch" ]; then
	echo "Launching one-time inference for deepspeech..."
	
	cp "${payloads}/deepspeech/payload.wav" "${inputs}/deepspeech/payload.wav"
	temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	touch "${temp_f}"
	time deepspeech	--model "${models}/deepspeech/deepspeech-0.9.1-models.${modeltype}" \
					--audio "${inputs}/deepspeech/payload.wav" \
					>>	  "${outputs}/deepspeech/transcript.txt"
	
	
	rm -f "${inputs}/deepspeech/payload.wav"
	rm -f "${outputs}/deepspeech/transcript.txt"
	rm -f "${temp_f}"



# Launch listener
elif [ "$1" = "listen" ]; then
	echo "Launching listener for deepspeech..."
	
	# If no appid is set, use defaults
	if [ "$2" = "0" ]; then
		input_f="${inputs}/deepspeech/payload.wav"
		output_f="${outputs}/deepspeech/transcript.txt"
		temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	# otherwise, use the appid
	else
		mkdir -p "${workdir}/app_${2}"
		chmod -R 777 "${workdir}/app_${2}"
		input_f="${workdir}/app_${2}/payload.wav"
		output_f="${workdir}/app_${2}/transcript.txt"
		temp_f="${workdir}/app_${2}/exec.tmp"
	fi
	
	# Clean the data folders
	rm -f "${input_f}"
	rm -f "${output_f}"
	rm -f "${temp_f}"
	
	counter=0
	while sleep 0.01; do
		if [ -f "${input_f}" ]; then
			touch "${temp_f}"
			time deepspeech	--model "${models}/deepspeech/deepspeech-0.9.1-models.${modeltype}" \
							--audio "${input_f}" \
							>>	    "${output_f}" \
							2> /dev/null

			counter=$((counter+1))
			
			echo "Processed audio clips: ${counter}"
			
			rm -f "${input_f}"
			rm -f "${output_f}"
			rm -f "${temp_f}"
		fi
	done

fi
