import base64
import importlib
import inspect
import keyword
import marshal
import os
import pickle
import pkgutil
import sys
from pathlib import Path
import SurzsEnviro

# Allow bare imports (e.g. `from computerspeak import ...`) inside SurzsEnviro modules
# to resolve when this package is loaded from a parent directory.
_enviro_path = str(Path(__file__).parent)
if _enviro_path not in sys.path:
    sys.path.insert(0, _enviro_path)


def _serialized_callable_name(content) -> str:
    name = getattr(content, "__name__", "") or "saved_callable"
    if not name.isidentifier() or keyword.iskeyword(name):
        return "saved_callable"
    return name


def _build_serialized_callable_script(content):
    import dill

    export_name = _serialized_callable_name(content)
    payload = base64.b64encode(dill.dumps(content, recurse=True)).decode("ascii")
    return (
        "import base64\n"
        "import dill\n\n"
        f"{export_name} = dill.loads(base64.b64decode({payload!r}))\n"
    )


def _pickle_to_b64(value):
    return base64.b64encode(pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)).decode(
        "ascii"
    )


def _build_stdlib_callable_script(content):
    if not inspect.isfunction(content):
        raise TypeError(
            "stdlib fallback only supports Python functions; pass a string or install dill"
        )

    export_name = _serialized_callable_name(content)
    module_globals = {}
    pickled_globals = {}
    for name in content.__code__.co_names:
        if name not in content.__globals__ or name == "__builtins__":
            continue
        value = content.__globals__[name]
        if inspect.ismodule(value):
            module_globals[name] = value.__name__
            continue
        pickled_globals[name] = value

    closure_specs = []
    for cell in content.__closure__ or ():
        value = cell.cell_contents
        if inspect.ismodule(value):
            closure_specs.append(("module", value.__name__))
        else:
            closure_specs.append(("pickle", _pickle_to_b64(value)))

    code_payload = base64.b64encode(marshal.dumps(content.__code__)).decode("ascii")
    defaults_payload = _pickle_to_b64(content.__defaults__)
    kwdefaults_payload = _pickle_to_b64(content.__kwdefaults__)
    annotations_payload = _pickle_to_b64(content.__annotations__)
    globals_payload = _pickle_to_b64(pickled_globals)
    closure_payload = _pickle_to_b64(closure_specs)

    return (
        "import base64\n"
        "import importlib\n"
        "import marshal\n"
        "import pickle\n"
        "import types\n\n"
        "def _make_cell(value):\n"
        "    def inner():\n"
        "        return value\n"
        "    return inner.__closure__[0]\n\n"
        f"_module_globals = {module_globals!r}\n"
        f"_globals = pickle.loads(base64.b64decode({globals_payload!r}))\n"
        "_globals.update(\n"
        "    {name: importlib.import_module(module_name) for name, module_name in _module_globals.items()}\n"
        ")\n"
        '_globals["__builtins__"] = __builtins__\n'
        f"_closure_specs = pickle.loads(base64.b64decode({closure_payload!r}))\n"
        "_closure = tuple(\n"
        "    _make_cell(importlib.import_module(value) if kind == 'module' else pickle.loads(base64.b64decode(value)))\n"
        "    for kind, value in _closure_specs\n"
        ")\n"
        f"{export_name} = types.FunctionType(\n"
        f"    marshal.loads(base64.b64decode({code_payload!r})),\n"
        "    _globals,\n"
        f"    {content.__name__!r},\n"
        f"    pickle.loads(base64.b64decode({defaults_payload!r})),\n"
        "    _closure or None,\n"
        ")\n"
        f"{export_name}.__kwdefaults__ = pickle.loads(base64.b64decode({kwdefaults_payload!r}))\n"
        f"{export_name}.__annotations__ = pickle.loads(base64.b64decode({annotations_payload!r}))\n"
    )

def pinspect(obj):
	a=inspect.getsource(obj)
	print(a)


def load_env():
    namespace = {}

    # Discover and import all modules under SurzsEnviro
    for _, module_name, _ in pkgutil.walk_packages(
        SurzsEnviro.__path__, SurzsEnviro.__name__ + "."
    ): #remember to keep names consistent with the actual package structure, and unique so there is no conflicts.
        try:
            module = importlib.import_module(module_name)
        except ImportError as err:
            print(f"[!] Skipping {module_name}: {err}")
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
            source = None
            # 2. inspect — works for file-backed functions
            try:
                source = inspect.getsource(content)
            except OSError:
                pass
            
            # 3. dill source fallback — sometimes works for dynamically defined callables
            if source is None:
                try:
                    import dill
                    source = dill.source.getsource(content)
                except Exception:
                    pass
            
            # 4. dill serialization — captures closures and dynamic functions
            if source is None:
                try:
                    source = _build_serialized_callable_script(content)
                except ImportError:
                    pass
            
            # 5. stdlib serialization fallback — no external deps
            if source is None:
                try:
                    source = _build_stdlib_callable_script(content)
                except Exception as err:
                    print(f"[!] Could not serialize callable: {err}")
                    return
        else:
            print(f"[!] content must be a string or callable, got {type(content)}")
            return

        filepath = os.path.join(os.getcwd(), name)
        with open(filepath, "w") as f:
            f.write(source)
        print(f"[+] Saved → {filepath}")
    namespace["pinspect"] = pinspect
    namespace["reload_all"] = reload_all
    namespace["add_script"] = add_script
    return namespace
