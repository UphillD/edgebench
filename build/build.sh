#!/bin/bash
# edgebench/build/build.sh
# Builds and pushes the docker image

# Print help
if [ $# -eq 0 ]; then
	echo "Not enough arguments!"
	echo
	echo "Usage:  ./build.sh <architecture>"
	echo 
	echo "    architectures: amd64, arm64v8, arm32v7, arm32v6, all"
	echo
	exit 1;
fi

# Build
if [ "$1" = "amd64" ] || [ "$1" = "all" ]; then
	docker buildx build --platform linux/amd64 -f Dockerfile -t uphilld/edgebench:amd64 --push ../
fi
if [ "$1" = "arm64v8" ] || [ "$1" = "all" ]; then
	docker buildx build --platform linux/arm64 -f Dockerfile -t uphilld/edgebench:arm64v8 --push ../
fi
if [ "$1" = "arm32v7" ] || [ "$1" = "all" ]; then
	docker buildx build --platform linux/arm/v7 -f Dockerfile -t uphilld/edgebench:arm32v7 --push ../
fi
if [ "$1" = "arm32v6" ] || [ "$1" = "all" ]; then
	docker buildx build --platform linux/arm/v6 -f Dockerfile.arm32v6 -t uphilld/edgebench:arm32v6 --push ../
fi
