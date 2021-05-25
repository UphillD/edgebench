# edgebench-RETAIN

An interpretable predictive model for healthcare applications.

Dockerized, pretrained and edge ready.

## Source

[RETAIN on GitHub, mp2893](https://github.com/mp2893/retain)

## Usage

Clone the repo:

    git clone https://github.com/UphillD/edgebench

`cd` into the project:

    cd retain

Download the prepared dataset & model:

    ./prepare.sh

Pull and run the docker image:

    docker run -v $PWD:/app uphilld/retain:[arch]

Available architectures:

* `amd64` = x86_64

* `rpiv6` = armv6 for Raspberry Pi Zero & 1

* `rpiv7` = armv7 for Raspberry Pi 2, 3 & 4
