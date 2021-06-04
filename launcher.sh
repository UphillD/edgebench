#!/bin/bash
# edgebench/launcher.sh
# edgebench launcher
# Launches the docker image

# Get & Set the execution platform
# We set this in order to pull the correct docker tag
# and pass it through to the docker container
# (it misbehaves when checked from inside)
case "$(uname -m)" in
	"x86_64")	platform="amd64" ;;
	"aarch64")	platform="arm64v8" ;;
	"armv7l")	platform="arm32v7" ;;
	"armv6l")	platform="arm32v6" ;;
	*)			echo 'Platform not found'; exit 1 ;;
esac

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
#       profile <app> <arch> <combo> <index> <length>
#
# Parameters:
#   -it: make the shell interactive
#   -v:  mount the current dir
#   -t:  set the appropriate tag
#   --entrypoint: change image entrypoint
#
if [ "$1" = "explore" ]; then	docker run -it --entrypoint /bin/sh -v $PWD:/app -t uphilld/edgebench:"$platform" ;
else							docker run -it -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@" ; fi
