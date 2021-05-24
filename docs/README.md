![edgebench logo](logo.png)

##

A collection of machine learning applications, utilized as use-cases for the resource management algorithm that I am developing for my thesis.

## Table of Contents

1. [The Applications](#The-Applications)
2. [Docker image](#Docker-Image)
3. [Usage](#Usage)
4. [Project Tree](#Project-Tree)
5. [Miscellaneous](#Miscellaneous)

## The Applications

[DeepSpeech](https://github.com/mozilla/DeepSpeech)

[FaceNet](https://github.com/davidsandberg/facenet)

[LaneNet](https://github.com/MaybeShewill-CV/lanenet-lane-detection)

[RETAIN](https://github.com/mp2893/retain)

## Docker Image

A docker image is utilized for easy & fast deployment on different platforms.

[Docker image repo](https://hub.docker.com/repository/docker/uphilld/edgebench)

Currently supported platforms: amd64, arm32v6, arm32v7, arm64v8

## Usage

Either run the launcher without arguments:	`./launcher.sh` for an interactive menu,
or run the launcher with the proper arguments.

## Project Tree

    $root
    ├ algo
    ├ apps
    ├    ├ deepspeech
    ├    ├ facenet
    ├    ├ lanenet
    ├    └ retain
    ├ build
    ├ data
    ├    ├ payloads
    ├    └ models
    ├ docs
    └ scripts

The algo folder is omitted for obvious reasons.

The data folder is also omitted, models and payloads can be downloaded by the corresponding selection on the menu.

## Miscellaneous

[⇯ Back to Top](#Table-of-Contents)
