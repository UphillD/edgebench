#!/bin/bash
# edgebench/scripts/prepare.sh
# Downloads and setups models, payloads, face database

# Source config file
source /app/apps/settings.cfg

# Print edgebench banner
source "${scripts}/print_banner.sh" "edgebench"

### URLs
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

### Main Script
echo
echo "Downloading pretrained models..."
echo

for app in $apps; do
    model="model_${app}"
    wget -q --show-progress -O "${app}_model.zip" "${!model}" && \
    mkdir -p "${models}/${app}" && \
    unzip -u -qq "${app}_model.zip" -d "${models}/${app}" && \
    rm -rf "${app}_model.zip"
done

echo
echo "Downloading payloads..."
echo

wget -q --show-progress "${payload_all}" && \
mkdir -p "${payloads}" && \
unzip -u -qq "payloads.zip" -d "${payloads}" && \
rm -rf "payloads.zip"

echo
echo "Downloading face database..."
echo

wget -q --show-progress "${face_db}" && \
mkdir -p "${workdir}/face_database" && \
unzip -u -qq "face_database.zip" -d "${workdir}/face_database" && \
rm -rf "face_database.zip"

echo
echo "Script done!"
echo
