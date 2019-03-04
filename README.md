# QPod Hub Package

[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![TravisCI Pipeline Status](https://img.shields.io/travis/com/QPod/qpod-hub.svg)](https://travis-ci.com/QPod/qpod-hub)
[![PyPI version](https://img.shields.io/pypi/v/qpod-hub.svg)](https://pypi.org/project/qpod-hub/#history)
[![PyPI format](https://img.shields.io/pypi/format/qpod-hub.svg)](https://pypi.org/project/qpod-hub/#files)
[![PyPI download month](https://img.shields.io/pypi/dm/qpod-hub.svg)](https://pypi.org/project/qpod-hub/)
[![GitHub Starts](https://img.shields.io/github/stars/QPod/qpod-hub.svg?label=Stars&style=social)](https://github.com/QPod/qpod-hub/stargazers)

**Notice:** If you are looking for the out-of-box QPod docker images, please goto: https://github.com/QPod/docker-images

## Introduction

The `qpod-hub` package provides a hub portal user interface and proxy service for QPod.

As a hub service, `qpod-hub` detect if specific service are installed and provides a homepage GUI for users.
Currently, the following services are supported: 
 - Jupyter Notebook
 - JupyterLab
 - Tensorboard
 - RStudio Server
 - Shiny Server

![Screenshot of QPod](https://i.imgur.com/zEaSliT.jpg "Screenshot of QPod")

## Development

### Under Linux/macOS
```
docker run -it --rm \
    --name=dev_QPod \
    --hostname="docker-develop@" \
    -v `pwd`/:/root/ \
    -v ~/.ssh/:/root/.ssh/:ro \
    -v ~/.gitconfig:/root/.gitconfig:ro \
    -p 8800-8888:8800-8888 \
    qpod /bin/bash
```

### Under Windows
```
docker run -it --rm ^
    --name=dev_QPod  ^
    --hostname="docker-develop@" ^
    -v %cd%/:/root/ ^
    -p 8800-8888:8800-8888 ^
    qpod /bin/bash
```

### Enter into the container and Debug/Install
```
docker exec -it dev_QPod /bin/bash

yarn --cwd ./qpod/base/static/
python -m qpod

python setup.py sdist bdist_wheel
pip install -U dist/*.whl
jupyter notebook
```
