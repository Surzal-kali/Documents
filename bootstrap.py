# Documents/bootstrap.py
import code
import os
import subprocess
import tempfile
import sys
from SurzsEnviro.bootstrap import load_env
from Exploit_Notes.bootstrap import load_notes

CHEATSHEET=""" 
===========================
 SurzsEnviro Interactive Console
===========================

SurzsEnviro (Python Modules)
-----------------------------------

List everything loaded:
    dir()print

Call any function directly:
    function_name(args)

Access a module directly:
    module_name
    module_name.function(args)

Reload ALL modules after edits:
    reload_all()

Reload ONE module:
    reload("module_name")

Inspect modules and functions:
    help(module_name)
    help(function_name)
    dir(module_name)

Store state in variables:

    result = function_name(args)

-----------------------------------

 exploit-notes (Markdown Knowledge Base)

-----------------------------------

List all notes (recursive):
    notes_list()

Search notes by keyword:
    notes_search("keyword")

Open a note:
    print(notes_open("Category/file.md"))

Reindex notes after adding new files:
    notes_reindex()
"""


def open_notes(text: str):
	editor = os.getenv("VISUAL") or os.getenv("EDITOR") or "less"
	# Write to a temp file and make it read-only so editors open it as view-only
	tf = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
	try:
		tf.write(text)
		tf.flush()
		tf.close()
		os.chmod(tf.name, 0o400)
		# Launch editor; pass file as argument. If editor is a simple pager like less, it works.
		cmd = editor.split() + [tf.name]
		try:
			subprocess.run(cmd)
		except FileNotFoundError:
			# Fallback to less if the chosen editor is not available
			subprocess.run(["less", tf.name])
	finally:
		try:
			os.remove(tf.name)
		except Exception:
			pass


namespace = {}
namespace.update(load_env())
namespace.update(load_notes())
namespace["CHEATSHEET"] = CHEATSHEET


code.interact(local=namespace)
