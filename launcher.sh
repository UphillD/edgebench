#!/bin/bash
# edgebench/launcher.sh
# edgebench launcher
# Launches the docker image

# Get & Set the execution platform
# We set this in order to pull the correct docker tag
# and pass it through to the docker container
# (it misbehaves when checked from inside)
if   [ "$(uname -m)" = "x86_64"  ]; then
	platform="amd64"
elif [ "$(uname -m)" = "aarch64" ]; then
	platform="arm64v8"
elif [ "$(uname -m)" = "armv7l"  ]; then
	platform="arm32v7"
elif [ "$(uname -m)" = "armv6l"  ]; then
	platform="arm32v6"
fi

## Launch the docker image
# Passes any arguments through to the docker image
# Possible invocations:
#    no argument -> interactive menu
# or explore     -> launch shell
# or call directly:
#       listen <app> <id>
#       loop <app> <id>
#       custodian <app combination>
#       spawner <number of tasks>
#       device <algorithm> <device id>
#       gateway <algorithm> <gateway id>
#
# Parameters:
#   -it: make the shell interactive
#   -v:  mount the current dir
#   -t:  set the appropriate tag
#   --entrypoint: change entrypoint script
#
if [ $# -eq 0 ]; then
	docker run -it -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform"
elif [ "$1" = "explore" ]; then
	docker run -it --entrypoint /bin/sh -v $PWD:/app -t uphilld/edgebench:"$platform"
else
	docker run -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@"
fi
