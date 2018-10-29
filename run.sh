#!/usr/bin/env bash

docker build -t quietcool-python . && docker run -it quietcool-python python -i test.py
