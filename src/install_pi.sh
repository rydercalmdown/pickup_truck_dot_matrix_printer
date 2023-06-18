#!/bin/bash

echo "Installing dependencies";
sudo apt-get update
sudo apt-get install -y ffmpeg \
    libsm6 \
    libxext6 \
    tini \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-h5py \
    libopenexr25 \
    build-essential \
    cmake \
    unzip \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    tmux

echo "Installing Python Requirements";
python3 -m pip install -r requirements.txt
