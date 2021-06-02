#!/bin/bash
# edgebench/scripts/cleanup.sh
# Cleans up workdir

# Source config file
source /app/apps/settings.cfg

echo "Cleaning up workdir"
rm -rf "${workdir}/app_"*
