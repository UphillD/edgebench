#!/bin/bash
# Looks for the models, downloads them if needed

# Source config file
source /app/apps/settings.cfg

echo
echo "Downloading pretrained models..."
echo

if [ ! -d "${payloads}" ]; then
    echo "Downloading payloads..."
    echo
    wget "${payload_all}" && \
    mkdir -p "${payloads}" && \
    unzip -qq "payloads.zip" -d "${payloads}" && \
    rm -rf "payloads.zip"
else
	echo "Payloads already exist, skipping ..."
	echo
fi

echo "Payloads ready."
echo
