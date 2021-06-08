#!/bin/bash
# edgebench/launcher.sh
# Docker image launcher

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

# Launch the docker image & pass any arguments through
#
# Possible invocations:
#      no arguments -> interactive menu
#   or explore      -> launch shell
#   or call directly:
#        listen <app> <app id>
#        loop <app> <app id>
#        custodian <app combination>
#        spawner <number of tasks> or <algorithm> <timeline>
#        device <algorithm> <device id>
#        gateway <algorithm> <gateway id>
#        profile <app> <arch> <combo> <index> <length>
#
# Parameters:
#   -it: make the shell interactive
#   -v:  mount a volume
#   -t:  set the image tag
#   --entrypoint: change image entrypoint
#
if   [ "$#" -eq 0 ];								then docker run -it -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@" ;
elif [ "$1" = "explore" ];							then docker run -it --entrypoint /bin/sh -v $PWD:/app -t uphilld/edgebench:"$platform" ;
elif [ "$1" = "spawn" ] || [ "$1" = "prepare" ];	then docker run -it -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@" ;
else													 docker run -v $PWD:/app -t uphilld/edgebench:"$platform" "$platform" "$@" ; fi
