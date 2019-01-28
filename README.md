# QPod Hub Package

## Introduction

The `qpod_hub` package provides a hub portal user interface and proxy service for QPod.

As a hub service, `qpod_hub` detect if specific service are installed and provides a homepage GUI for users.
Currently, the following services are supported: 
 - Jupyter Notebook
 - JupyterLab
 - Tensorboard
 - RStudio Server
 - Shiny Server

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
pip install dist/*.whl
jupyter notebook
```
