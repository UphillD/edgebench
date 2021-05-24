![edgebench logo](logo.png)

##

A collection of machine learning applications, utilized as use-cases for the resource management algorithm that I am developing for my bachelor thesis.

![arch: arm32v6](arch-arm32v6-blue.svg)
![arch: arm32v7](arch-arm32v7-blue.svg)
![arch: arm64v8](arch-arm64v8-blue.svg)
![arch: arm64](arch-amd64-blue.svg)

![platform: Raspberry Pi 4](platform-raspberrypi4-brightgreen.svg)
![platform: Tegra X1](platform-tegrax1-brightgreen.svg)

## Table of Contents

1. [The Applications](#The-Applications)
2. [Docker image](#Docker-Image)
3. [Usage](#Usage)
4. [Project Tree](#Project-Tree)
5. [Miscellaneous](#Miscellaneous)

## The Applications

[DeepSpeech](https://github.com/mozilla/DeepSpeech), an embedded speech-to-text engine using Tensorflow

[FaceNet](https://github.com/davidsandberg/facenet), a face recognizer using Tensorflow

[LaneNet](https://github.com/MaybeShewill-CV/lanenet-lane-detection), a deep neural network for real time lane detection using Tensorflow

[RETAIN](https://github.com/mp2893/retain), an interpretable predictive model for healthcare applications using Theano

## Docker Image

A docker image is utilized for easy & fast deployment on different platforms.

[Docker image repo](https://hub.docker.com/repository/docker/uphilld/edgebench)

Currently supported platforms: amd64, arm32v6, arm32v7, arm64v8

## Usage

Either run the launcher without arguments (`./launcher.sh`) for an interactive menu,
or run the launcher with the proper arguments (see the file comments for more info).

## Project Tree

    $root
    ├ algo
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

The data folder is also omitted, models and payloads can be downloaded by entering the corresponding selection on the menu.

## Miscellaneous

Shield badges provided by [Shields.io](https://shields.io/).

[⇯ Back to Top](#Table-of-Contents)
