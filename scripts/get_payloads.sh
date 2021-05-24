#!/bin/bash
# Looks for the models, downloads them if needed

# Source config file
source /app/apps/settings.cfg

echo
echo "Downloading pretrained models..."
echo

for app in $apps; do
    if [ ! -d "${payloads}" ]; then
        echo "Downloading payloads..."
        echo
        wget "${payload_all}" && \
        mkdir -p "${payloads}" && \
        unzip -qq "payloads_all.zip" -d "${payloads}" && \
        rm -rf "payloads_all.zip"
    else
		echo "Payloads already exist, skipping ..."
		echo
	fi
done

echo "Payloads ready."
echo
