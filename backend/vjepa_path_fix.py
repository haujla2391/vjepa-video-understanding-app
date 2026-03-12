import sys
import os

# This file must be imported FIRST in app.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Force-add vjepa2 folder if it exists (clone case)
vjepa2_path = os.path.join(project_root, 'vjepa2')
if os.path.exists(vjepa2_path) and vjepa2_path not in sys.path:
    sys.path.insert(0, vjepa2_path)

# Optional: add site-packages fallback for git+https install
try:
    import site
    for p in site.getsitepackages():
        candidate = os.path.join(p, 'vjepa2')
        if os.path.exists(candidate) and candidate not in sys.path:
            sys.path.insert(0, candidate)
except:
    pass