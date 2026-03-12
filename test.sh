#!/usr/bin/env bash
set -e

git clone --depth 1 https://github.com/facebookresearch/vjepa2.git vjepa2 || echo "Clone failed"
ls -la vjepa2/ | grep -E 'setup.py|pyproject.toml|src' || echo "Key files missing after clone!"
pip install -e ./vjepa2 || echo "Editable install failed"
python -c "import sys; print(sys.path)"  # see paths
python -c "from src.models.attentive_pooler import AttentiveClassifier; print('Import OK')" || echo "Import test failed"
pip install -r requirements.txt