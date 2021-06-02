#!/bin/bash
# edgebench/apps/start.sh
# App launcher
# ./start.sh $app $id (default=0) $option (loop, default="")

# Source config file
source /app/apps/settings.cfg

# Grab app
app="$1"
appid="$2"
option="$3"

# Enter app directory
cd "${appdir}/${app}"

# Print banner
source "${scripts}/print_banner.sh" "${app}"

# Init & folder stuff
if [ "$appid" = "0" ] || [ "$appid" = "" ]; then	working="${workdir}/app_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 3 ; echo '');
else												working="${workdir}/app_${2}"; fi
rm -rf "$working"
mkdir -p "$working"
chmod -R 777 "$working"
temp_f="${working}/exec.tmp"

### Deepspeech
if [ "$app" = "deepspeech" ]; then

	if [ "$platform" = "amd64" ]; then	modeltype="pbmm" ;
	else 								modeltype="tflite" ; fi
	model="${models}/deepspeech/deepspeech-0.9.1-models.${modeltype}"
	input_f="${working}/payload.wav"
	output_f="${working}/transcript.txt"
	
	if [ "$3" = "loop" ]; then cp "${payloads}/deepspeech/payload.wav" "${input_f}" ; fi
	while sleep 0.01 ; do
		if [ -f "${input_f}" ]; then
			touch "$temp_f"
			time deepspeech --model "$model" --audio "$input_f" >> "$output_f"
			if [ ! "$3" = "loop" ]; then rm -f "${input_f}" ; fi
			rm -f "${output_f}"
			rm -f "${temp_f}"
		fi
	done


### Facenet
elif [ "$app" = "facenet" ]; then
	model="${models}/facenet/"
	input_f="${working}/"
	output_f="${working}/"
	
	if [ "$option" = "loop" ]; then	loop="True" ;
	else							loop="False" ; fi
	
	python3.7 infer.py "$model" "$input_f" "$output_f" "$temp_f" "$loop"

### Lanenet
elif [ "$app" = "lanenet" ]; then
	model="${models}/lanenet/tusimple_lanenet.ckpt"
	input_f="${working}/"
	output_f="${working}/"
	
	if [ "$option" = "loop" ]; then	loop="True" ;
	else							loop="False" ; fi
	
	python3.7 infer.py --image_dir "$input_f" --weights_path "$model" --save_dir "$output_f" --temp_file "$temp_f" --loop "$loop"


### RETAIN
elif [ "$app" = "retain" ]; then
	model="${models}/retain/model.13.npz"
	input_f="${working}/"
	output_f="${working}/result.txt"
	
	if [ "$3" = "loop" ]; then cp "${payloads}/retain/payload.zip" "${input_f}/payload.zip" ; fi
	while sleep 0.01; do
		if [ -e "${input_f}/payload.zip" ]; then
			touch "$temp_f"
			unzip -u -qq "${input_f}/payload.zip" -d "${input_f}/"
			time python2.7 infer.py "$model" \
									"${input_f}/payload.3digitICD9.seqs" \
									"${input_f}/payload.morts" \
									"${input_f}/payload.3digitICD9.types" \
									"$output_f" \
									&> /dev/null
			
			if [ ! "$3" = "loop" ]; then rm -f "${input_f}/payload."* ; fi
			rm -f "$output_f"
			rm -f "$temp_f"
		fi
	done
fi
