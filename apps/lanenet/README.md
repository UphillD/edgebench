# edgebench-lanenet

A real time lane detection model for automotive applications.

Dockerized, pretrained and edge ready.

## Source

[lanenet-lane-detection on GitHub, MaybeShewill-CV](https://github.com/MaybeShewill-CV/lanenet-lane-detection)

## Usage

Clone the repo:

    git clone https://github.com/UphillD/edgebench

`cd` into the project:

    cd lanenet

Download the prepared dataset & model:

    ./prepare.sh

Pull and run the docker image:

    docker run -v $PWD:/app uphilld/lanenet:[arch]

Available architectures:

* `amd64` = x86_64

* `rpiv6` = armv6 for Raspberry Pi Zero & 1

* `rpiv7` = armv7 for Raspberry Pi 2, 3 & 4
