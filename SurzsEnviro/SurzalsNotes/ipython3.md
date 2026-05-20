# Ipython3 REPL SETTINGS

## Prompt

```python
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
```

## Important Note: This setup assumes that the `SurzsEnviro` environment is properly configured and that the `bootstrap` module contains the necessary logic to load the environment. Make sure to adjust the path and import statements as needed based on your project structure.

always remember to save it in ~/.ipython/profile_default/startup/surz_env.py so that it runs every time you start an IPython session.
