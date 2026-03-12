#!/usr/bin/env bash
set -e  # exit on error

if [ ! -d "vjepa2" ]; then
  git clone --depth 1 https://github.com/facebookresearch/vjepa2.git vjepa2
fi

pip install -e ./vjepa2
pip install -r requirements.txt