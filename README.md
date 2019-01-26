# QPod Hub Package

## Introduction

A Portal UI and proxy service for QPod.

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

yarn --cwd ./qpod_hub/base/static/
python -m qpod_hub

python setup.py bdist_wheel
pip install dist/*.whl
jupyter notebook
```
