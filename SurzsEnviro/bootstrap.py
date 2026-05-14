import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
import SurzsEnviro

# Allow bare imports (e.g. `from computerspeak import ...`) inside SurzsEnviro modules
# to resolve when this package is loaded from a parent directory.
_enviro_path = str(Path(__file__).parent)
if _enviro_path not in sys.path:
    sys.path.insert(0, _enviro_path)

def load_env():
    namespace = {}

    # Discover and import all modules under SurzsEnviro
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        SurzsEnviro.__path__, SurzsEnviro.__name__ + "."
    ): #remember to keep names consistent with the actual package structure, and unique so there is no conflicts.
        module = importlib.import_module(module_name)
        short = module_name.split(".")[-1]
        namespace[short] = module

        # Optionally expose top-level functions/classes
        for attr in dir(module):
            if not attr.startswith("_"):
                namespace[attr] = getattr(module, attr)

    # Hot reload helper
    def reload_all():
        for name, module in list(namespace.items()):
            if hasattr(module, "__file__"):
                importlib.reload(module)

    namespace["reload_all"] = reload_all
    return namespace
