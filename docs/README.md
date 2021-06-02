![edgebench logo](logo.png)

##

A collection of heterogenous machine learning applications employed as use-cases for the resource management algorithm I am developing for my bachelor thesis.

![arch: arm32v6](arch-arm32v6-blue.svg)
![arch: arm32v7](arch-arm32v7-blue.svg)
![arch: arm64v8](arch-arm64v8-blue.svg)
![arch: amd64](arch-amd64-blue.svg)

![platform: Raspberry Pi 4](platform-raspberrypi4-brightgreen.svg)
![platform: Jetson TX1](platform-jetsontx1-brightgreen.svg)
![platform: Jetson Nano](platform-jetsonnano-brightgreen.svg)
![platform: 

![platform:

## Table of Contents

1. [The Applications](#The-Applications)
2. [Docker image](#Docker-Image)
3. [Setup](#Setup)
4. [Usage](#Usage)
5. [Project Tree](#Project-Tree)
6. [Miscellaneous](#Miscellaneous)

## The Applications

* [DeepSpeech](https://github.com/mozilla/DeepSpeech), an embedded speech-to-text engine using Tensorflow
* [FaceNet](https://github.com/davidsandberg/facenet), a face recognizer using Tensorflow
* [LaneNet](https://github.com/MaybeShewill-CV/lanenet-lane-detection), a deep neural network for real time lane detection using Tensorflow
* [RETAIN](https://github.com/mp2893/retain), an interpretable predictive model for healthcare applications using Theano

## Docker Image

A docker image is utilized for easy & fast deployment on different platforms: [Docker Repository](https://hub.docker.com/repository/docker/uphilld/edgebench)

Pull it with `docker pull uphilld/edgebench:<platform>` or let the launcher do it for you!

Currently supported platforms: `arm32v6`, `arm32v7`, `arm64v8`, `amd64`

## Setup

Run the following command:

    git clone https://github.com/UphillD/edgebench && \
    cd edgebench && \
    git clone https://github.com/UphillD/edgebench.algos algo && \
    ./launcher.sh prepare
    
## Usage

Start the launcher:

__Interactive menu:__ `./launcher.sh`

__Interactive shell:__ `./launcher.sh explore`

__Direct call:__ `./launcher.sh <command> <arguments>`

## Project Tree

    $root
    ├ algo 🔒
    ├ apps
    ├    ├ deepspeech
    ├    ├ facenet
    ├    ├ lanenet
    ├    ├ retain
    ├    └ settings.cfg
    ├ build
    ├ data
    ├    ├ payloads
    ├    └ models
    ├ docs
    └ scripts

The algo folder is omitted for obvious reasons.

The data folder is also omitted, models and payloads can be downloaded via the corresponding selection on the menu.

## Miscellaneous

Shield badges provided by [Shields.io](https://shields.io/).

[⇯ Back to Top](#Table-of-Contents)
