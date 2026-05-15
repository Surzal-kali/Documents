import importlib
import inspect
import os
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
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            print(f"[!] Skipping {module_name}: {e}")
            continue
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
    
    def add_script(name: str, content):
        # 1. Raw string — write as-is
        if isinstance(content, str):
            source = content
        elif callable(content):
            # 2. inspect — works for file-backed functions
            try:
                source = inspect.getsource(content)
            except OSError:
                # 3. dill fallback — decompiles from bytecode (handles live console functions)
                try:
                    import dill
                    source = dill.source.getsource(content)
                except Exception as e:
                    print(f"[!] Could not extract source: {e}")
                    return
        else:
            print(f"[!] content must be a string or callable, got {type(content)}")
            return

        filepath = os.path.join(os.getcwd(), name)
        with open(filepath, "w") as f:
            f.write(source)
        print(f"[+] Saved → {filepath}")

    namespace["reload_all"] = reload_all
    namespace["add_script"] = add_script
    return namespace
