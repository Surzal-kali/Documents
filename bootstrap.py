import argparse
import code
import os
import readline
import rlcompleter
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

DOCUMENTS_ROOT = Path(__file__).resolve().parent
NOTES_ROOT = DOCUMENTS_ROOT / "Exploit_Notes"
documents_root_str = str(DOCUMENTS_ROOT)
if documents_root_str not in sys.path:
    sys.path.insert(0, documents_root_str)

from SurzsEnviro.bootstrap import load_env

CHEATSHEET=""" 
===========================
 SurzsEnviro Interactive Console
===========================

Lightweight standalone mode:
    python3 bootstrap.py

Optional richer shell when IPython is installed:
    python3 bootstrap.py --shell ipython

SurzsEnviro (Python Modules)
-----------------------------------

List everything loaded:
    dir() will print all variables, functions, and modules in the current namespace.

Call any function directly:
    function_name(args)

Access a module directly:
    module_name
    module_name.function(args)

Reload ALL modules after edits:
    reload_all()

Inspect modules and functions:
    help(module_name)
    help(function_name)
    dir(module_name)
    pinspect(module_name) for complete code introspection

Quick notes and shell helpers:
    speak("remember this target path")
    ec("pwd")

Store state in variables:

    result = function_name(args)

-----------------------------------

 exploit-notes (Markdown Knowledge Base)

-----------------------------------

Browse the notes directory directly:
    NOTES_ROOT
    list(NOTES_ROOT.rglob("*.md"))

Read a note with Python or IPython:
    print((NOTES_ROOT / "Category/file.md").read_text())
"""
def module_aware_completer(namespace):
    # Try to use Jedi if available
    try:
        from jedi import Interpreter
        JEDI_AVAILABLE = True
    except ImportError:
        JEDI_AVAILABLE = False
        print("Note: Install 'jedi' for better autocompletion (pip install jedi)")
    
    # Fallback completer (your original logic)
    fallback_completer = rlcompleter.Completer(namespace)
    
    def fallback_complete(text, state):
        if "." in text:
            module_name, _, attr_prefix = text.rpartition(".")
            module = namespace.get(module_name)
            if module:
                attrs = [a for a in dir(module) if a.startswith(attr_prefix)]
                if state < len(attrs):
                    return f"{module_name}.{attrs[state]}"
                return None
        return fallback_completer.complete(text, state)
    
    if not JEDI_AVAILABLE:
        return fallback_complete
    
    # Jedi-powered completer
    def jedi_complete(text, state):
        if state == 0:
            try:
                # Use Jedi Interpreter against your live namespace
                interpreter = Interpreter(text, [namespace, namespace])
                completions = interpreter.complete()
                
                # Store matches for subsequent state calls
                jedi_complete.matches = []
                for c in completions:
                    name = c.name
                    # Handle dotted completions like module.attr
                    if "." in text:
                        base, _ = text.rsplit(".", 1)
                        full = f"{base}.{name}"
                    else:
                        full = name
                    
                    if full.startswith(text):
                        jedi_complete.matches.append(full)
                
                # Also include fallback results (catches edge cases Jedi misses)
                # But deduplicate
                fallback_matches = []
                for i in range(100):  # Arbitrary limit
                    fb = fallback_complete(text, i)
                    if fb is None:
                        break
                    if fb not in jedi_complete.matches:
                        fallback_matches.append(fb)
                jedi_complete.matches.extend(fallback_matches)
                
            except Exception:
                # Jedi can fail on malformed code; fall back gracefully
                jedi_complete.matches = []
                for i in range(100):
                    fb = fallback_complete(text, i)
                    if fb is None:
                        break
                    jedi_complete.matches.append(fb)
        
        if state < len(jedi_complete.matches):
            return jedi_complete.matches[state]
        return None
    
    return jedi_complete

def open_notes(text: str):
    editor = os.getenv("VISUAL") or os.getenv("EDITOR") or "less"
    # Write to a temp file and make it read-only so editors open it as view-only
    temp_file = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
    try:
        temp_file.write(text)
        temp_file.flush()
        temp_file.close()
        os.chmod(temp_file.name, 0o400)
        # Launch editor; pass file as argument. If editor is a simple pager like less, it works.
        command = shlex.split(editor) + [temp_file.name]
        try:
            subprocess.run(command)
        except FileNotFoundError:
            # Fallback to less if the chosen editor is not available
            subprocess.run(["less", temp_file.name])
    finally:
        try:
            os.remove(temp_file.name)
        except Exception:
            pass


def build_namespace():
    namespace = {"DOCUMENTS_ROOT": DOCUMENTS_ROOT, "NOTES_ROOT": NOTES_ROOT}
    namespace.update(load_env())
    namespace["CHEATSHEET"] = CHEATSHEET
    namespace["open_notes"] = open_notes
    return namespace


def configure_plain_repl(namespace):
    readline.parse_and_bind("tab: complete")
    readline.set_completer(module_aware_completer(namespace))


def launch_plain_repl(namespace):
    code.interact(local=namespace, banner=CHEATSHEET)


def launch_ipython_repl(namespace):
    from IPython import start_ipython

    print(CHEATSHEET)
    start_ipython(argv=[], user_ns=namespace, display_banner=False)


def launch_repl(namespace=None, shell="plain"):
    if namespace is None:
        namespace = build_namespace()

    if shell == "ipython":
        launch_ipython_repl(namespace)
        return
    if shell == "auto":
        try:
            launch_ipython_repl(namespace)
            return
        except ImportError:
            pass

    configure_plain_repl(namespace)
    launch_plain_repl(namespace)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Launch the standalone Documents console."
    )
    parser.add_argument(
        "--shell",
        choices=("plain", "ipython", "auto"),
        default="plain",
        help="REPL backend to use. Defaults to the lightweight plain shell.",
    )
    args = parser.parse_args(argv)
    launch_repl(shell=args.shell)


if __name__ == "__main__":
    main()
