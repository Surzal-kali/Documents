import sys
from pathlib import Path

# Add your project root to Python's import path
project_root = Path.home()
sys.path.insert(0, str(project_root))

# Load SurzsEnviro environment
from SurzsEnviro.bootstrap import load_env
ns = load_env()

# Inject into IPython namespace
get_ipython().push(ns)

# nano ~/.ipython/profile_default/startup/00-surzsenviro.py
