# Documents/bootstrap.py
import code
from SurzsEnviro.bootstrap import load_env
from Exploit_Notes.bootstrap import load_notes

namespace = {}
namespace.update(load_env())
namespace.update(load_notes())

code.interact(local=namespace)
