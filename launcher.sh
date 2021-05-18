#!/bin/bash
# Launches the docker image

# Get & Set the platform name
# We set this in order to pull the correct docker tag
# and pass it inside the docker container
# (it misbehaves when checked from inside)
if   [ "$(uname -m)" = "x86_64" ]; then
	platform="amd64"
elif [ "$(uname -m)" = "aarch64" ]; then
	platform="arm64v8"
elif [ "$(uname -m)" = "armv7l" ]; then
	platform="arm32v7"
elif [ "$(uname -m)" = "armv6l" ]; then
	platform="arm32v6"
fi

# Launch the docker image
# Passes all arguments through to the docker image
# Parameters:
#   -it: make the shell interactive
#   -v:  mount the current dir
#   -t:  pull the appropriate tag
if [ "$1" = "launch" ]; then
	docker run -it -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@"
else
	docker run -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@"
fi
