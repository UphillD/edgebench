#!/bin/bash
# edgebench/scripts/cleanup.sh
# Cleans up working directory

# Source config file
source /app/apps/settings.cfg

echo "Cleaning up working directory..."
rm -rf "${workdir}/app_"*
rm -rf "${workdir}/"*".pkl"
