#!/bin/bash
# Looks for the models, downloads them if needed

# Source config file
source /app/apps/settings.cfg

echo
echo "Downloading pretrained models..."
echo

for app in $apps; do
    if [ ! -d "${models}/${app}" ]; then
        echo "Downloading pretrained model for ${app}..."
        echo
        model="model_${app}"
        wget -O "${app}_model.zip" "${!model}" && \
        mkdir -p "${models}/${app}" && \
        unzip -qq "${app}_model.zip" -d "${models}/${app}" && \
        rm -rf "${app}_model.zip"
    else
        echo "Pretrained model for ${app} already exists, skipping..."
        echo
    fi
done

echo "Pretrained models ready."
echo
