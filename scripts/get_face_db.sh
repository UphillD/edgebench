#!/bin/bash
# Looks for the models, downloads them if needed

# Source config file
source /app/apps/settings.cfg

echo
echo "Downloading face database..."
echo

#if [ ! -d "${payloads}" ]; then
echo "Downloading face database..."
echo
wget "${face_db}" && \
mkdir -p "/app/algo/workdir/face_database" && \
unzip -qq "face_database.zip" -d "/app/algo/workdir/face_database" && \
rm -rf "face_database.zip"

echo "Face DB ready."
echo
