#!/bin/bash
# Cleans up data folders

# Source config file
source /app/apps/settings.cfg



echo "Removing inputs"
rm -rf "${inputs}/deepspeech/payload.wav"
rm -rf "${inputs}/facenet/payload.jpg"
rm -rf "${inputs}/lanenet/payload.jpg"*
rm -rf "${inputs}/retain/payload."*

echo "Removing outputs"
rm -f "${outputs}/deepspeech/"*
rm -f "${outputs}/facenet/"*
rm -f "${outputs}/lanenet/"*
rm -f "${outputs}/retain/"*

echo "Removing logs & temps"
rm -f "${logs}/"*
rm -f "${temps}/"*
