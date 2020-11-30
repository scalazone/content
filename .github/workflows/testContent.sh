#!/usr/bin/env bash

set -e -o pipefail -u

CONTENT_DIR=$(pwd)

cd checks
pip3 install -U pytest
pip3 install dataclasses

export CONTENT_DIR
python3 -m pytest -rP