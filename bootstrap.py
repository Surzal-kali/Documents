# Documents/bootstrap.py
import code
from SurzsEnviro.bootstrap import load_env
from 

namespace = {}
namespace.update(load_env())
namespace.update(load_notes())

code.interact(local=namespace)
