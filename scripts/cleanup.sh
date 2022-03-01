#!/bin/bash
# Edgebench Platform
# Cleaner Scripts
#
# Cleans up working directory

# Source config file
source /app/apps/settings.cfg

echo "Cleaning up working directory..."
rm -rf "${workdir}/app_"*
rm -rf "${workdir}/"*".pkl"
