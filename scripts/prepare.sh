#!/bin/bash
# Edgebench Framework
# Preparation Script
#
# Downloads and setups models, payloads, face database

# Source config file
source /app/apps/settings.cfg

# Print edgebench banner
source "${scripts}/print_banner.sh" "edgebench"

############
### URLs ###
############
# Model URLs
if [ "$platform" = "amd64" ]; then	model_deepspeech="https://dropbox.com/s/cx2z6ka4tjselyl/deepspeech_model_pbmm.zip" ;
else								model_deepspeech="https://dropbox.com/s/u2li4rw9zceb7uk/deepspeech_model_tflite.zip"; fi
model_facenet="https://dropbox.com/s/uf97u6iyk46q06j/facenet_model.zip"
model_lanenet="https://dropbox.com/s/n3zp4edgoep7iaz/lanenet_model.zip"
model_retain="https://dropbox.com/s/4x7aa985xf89am7/retain_model.zip"

# Testset URLs
testset_deepspeech="https://dropbox.com/s/qdtwfp0mhr2i5q1/deepspeech_testset_mini.zip"
testset_facenet="https://dropbox.com/s/i3zggkdxevnqp72/facenet_testset_mini.zip"
testset_lanenet="https://dropbox.com/s/hg30lgzhq44ty8e/lanenet_testset_mini.zip"
testset_retain="https://dropbox.com/s/sfd20o18vvnuqns/retain_testset_mini.zip"
testset_retain_full="https://dropbox.com/s/jsl2h35v0p3m3q7/retain_testset_full.zip"

# Payload URL
payload_all="https://dropbox.com/s/kzm1s4hcrk95l5p/payloads.zip"

# Face Database URL
face_db="https://dropbox.com/s/bczpwwj1vueig0c/face_database.zip"

###################
### Main Script ###
###################
echo
echo "Downloading pretrained models..."
echo

for app in $apps; do
	if [ -d ${models}/${app} ]; then
		echo "Model for ${app} app already exists."
	else
		model="model_${app}"
		wget -q --show-progress -O "${app}_model.zip" "${!model}" && \
		mkdir -p "${models}/${app}" && \
		unzip -u -qq "${app}_model.zip" -d "${models}/${app}" && \
		rm -rf "${app}_model.zip"
	fi
done

echo
echo "Downloading payloads..."
echo

if [ -d ${payloads} ]; then
	echo "Payloads already downloaded."
else
	wget -q --show-progress "${payload_all}" && \
	mkdir -p "${payloads}" && \
	unzip -u -qq "payloads.zip" -d "${payloads}" && \
	rm -rf "payloads.zip"
fi

echo
echo "Downloading face database..."
echo

if [ -d ${workdir}/face_database ]; then
	echo "Face database already exists."
else
	wget -q --show-progress "${face_db}" && \
	mkdir -p "${workdir}/face_database" && \
	unzip -u -qq "face_database.zip" -d "${workdir}/face_database" && \
	rm -rf "face_database.zip"
fi

echo
echo "Script done!"
echo

# Extra step: ask and store device platform
echo
echo "What device are you running this on?"
echo "Options: rpi4, rpi4_2, rpi4_3, tegra, nano, amd64, amd64_2"
read -p "Enter the name of the device:" device

sed -i "s/device_name = 'None'/device_name = '${device}'/g" "${algodir}/config.py"
