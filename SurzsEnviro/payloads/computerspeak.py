from pathlib import Path
import sys

_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from computerspeak import ComputerSpeak

__all__ = ["ComputerSpeak"]