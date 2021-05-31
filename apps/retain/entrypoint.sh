#!/bin/bash
# Entrypoint for retain benchmark

# Source config file
source /app/apps/settings.cfg

# Enter directory
cd "${appdir}/retain"

# Print banner
source "${scripts}/print_banner.sh" "retain"



# Launch one time inference
if [ "$1" = "launch" ]; then
	echo "Launching one-time inference for retain..."
	temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	touch "${temp_f}"
	cp "${payloads}/retain/payload.zip" "${inputs}/retain/payload.zip"
	unzip -qq "${inputs}/retain/payload.zip" -d "${inputs}/retain/" 
	time python2.7 test_retain.py	"${models}/retain/model.13.npz" \
									"${inputs}/retain/payload.3digitICD9.seqs" \
									"${inputs}/retain/payload.morts" \
									"${inputs}/retain/payload.3digitICD9.types" \
									"${outputs}/retain/result.txt"
	rm -rf "${inputs}/retain/payload."*
	rm -f "${temp_f}"



# Launch listener
elif [ "$1" = "listen" ]; then
    echo "Launching listener for retain..."
    counter=0
    
	if [ "$2" = "0" ]; then
		input_f="${inputs}/retain"
		output_f="${outputs}/retain"
		temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	else
		mkdir -p "${workdir}/app_${2}"
		chmod -R 777 "${workdir}/app_${2}"
		input_f="${workdir}/app_${2}"
		output_f="${workdir}/app_${2}"
		temp_f="${workdir}/app_${2}/exec.tmp"
    fi
    
    while sleep 0.01; do
		if [ -e "${input_f}/payload.zip" ]; then
			touch "${temp_f}"
			unzip -qq "${input_f}/payload.zip" -d "${input_f}/"
			time python2.7 infer.py	"${models}/retain/model.13.npz" \
											"${input_f}/payload.3digitICD9.seqs" \
											"${input_f}/payload.morts" \
											"${input_f}/payload.3digitICD9.types" \
											"${output_f}/result.txt" \
											&> /dev/null

			
			counter=$((counter+1))
			echo "Processed patient files: ${counter}"
			rm -f "${input_f}/payload."*
			rm -f "${output_f}/result.txt"
			rm -f "${temp_f}"
			
		fi
	done

# Launch listener
elif [ "$1" = "loop" ]; then
    echo "Launching listener for retain..."
    counter=0
    
	if [ "$2" = "0" ]; then
		input_f="${inputs}/retain"
		output_f="${outputs}/retain"
		temp_f="${temps}/"$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6 ; echo '')".tmp"
	else
		mkdir -p "${workdir}/app_${2}"
		chmod -R 777 "${workdir}/app_${2}"
		input_f="${workdir}/app_${2}"
		output_f="${workdir}/app_${2}"
		temp_f="${workdir}/app_${2}/exec.tmp"
    fi
    
    
	cp "${payloads}/retain/payload.zip" "${input_f}/payload.zip"
    
    while sleep 0.01; do
		if [ -e "${input_f}/payload.zip" ]; then
			touch "${temp_f}"
			unzip -f -qq "${input_f}/payload.zip" -d "${input_f}/"
			time python2.7 infer.py	"${models}/retain/model.13.npz" \
											"${input_f}/payload.3digitICD9.seqs" \
											"${input_f}/payload.morts" \
											"${input_f}/payload.3digitICD9.types" \
											"${output_f}/result.txt" \
											&> /dev/null

			
			counter=$((counter+1))
			echo "Processed patient files: ${counter}"
			rm -f "${output_f}/result.txt"
			rm -f "${temp_f}"
			
		fi
	done

fi
