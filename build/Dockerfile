# Pull base image
FROM debian:buster-slim

# Set label(s)
LABEL maintainer "akarteris21@gmail.com"

# Enable platform ARGs
ARG TARGETARCH

# Set working directory
WORKDIR /app

# Install packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
	python2.7 \
	python-pip python-setuptools python-six \
	python-numpy python-scipy \
	python3.7 \
	python3-pip python3-setuptools python3-six \
	python3-numpy python3-scipy python3-matplotlib python3-sklearn \
	python3-grpcio python3-joblib python3-requests python3-psutil \
	python3-h5py python3-opencv python3-pandas python3-pil \
	python3-tqdm python3-yaml \
	python3-paho-mqtt \
	mosquitto mosquitto-clients \
	unzip wget \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install theano
RUN pip2 install theano==1.0.4 --no-cache-dir

# Install tensorflow
RUN if [ "$TARGETARCH" = "amd64" ]; then \
		pip3 install tensorflow==1.14.0 --no-cache-dir; \
	elif [ "$TARGETARCH" = "arm64" ]; then \
		wget -nv https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.14.0-buster/tensorflow-1.14.0-cp37-none-linux_aarch64.whl \
	&&	pip3 install tensorflow-1.14.0-cp37-none-linux_aarch64.whl --no-cache-dir \
	&&	rm -f tensorflow-1.14.0-cp37-none-linux_aarch64.whl; \
	elif [ "$TARGETARCH" = "arm" ]; then \
		wget -nv https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.14.0-buster/tensorflow-1.14.0-cp37-none-linux_armv7l.whl \
	&&	pip3 install tensorflow-1.14.0-cp37-none-linux_armv7l.whl --no-cache-dir --extra-index-url https://piwheels.org/simple \
	&&	rm -f tensorflow-1.14.0-cp37-none-linux_armv7l.whl; \
	fi

# Install deepspeech
RUN if [ "$TARGETARCH" = "amd64" ]; then \
		pip3 install deepspeech --no-cache-dir; \
	elif [ "$TARGETARCH" = "arm64" ]; then \
		wget -nv https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-cp37-cp37m-linux_aarch64.whl \
	&&	pip3 install deepspeech-0.9.1-cp37-cp37m-linux_aarch64.whl --no-cache-dir \
	&&	rm -rf deepspeech-0.9.1-cp37-cp37m-linux_aarch64.whl; \
	elif [ "$TARGETARCH" = "arm" ]; then \
		pip3 install deepspeech --no-cache-dir --extra-index-url https://piwheels.org/simple; \
	fi

# Install python requirements
COPY build/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir --extra-index-url https://piwheels.org/simple

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
