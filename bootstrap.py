# Documents/bootstrap.py
import code
import os
import subprocess
import tempfile
import sys
from SurzsEnviro.bootstrap import load_env
from Exploit_Notes.bootstrap import load_notes


def _open_in_editor_readonly(text: str):
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


code.interact(local=namespace)
