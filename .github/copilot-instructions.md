# Copilot instructions for this repository

## Build, test, and lint

- Install Python dependencies from the repo root with `python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.md`. The dependency list is checked in as `requirements.md`, not `requirements.txt`.
- There is no committed repo-level build pipeline, lint configuration, or automated test suite in this repository. `black`, `ruff`, and `pyright` are installed from `requirements.md`, but there is no checked-in config or standard repo command that wires them together.
- There is no dedicated single-test command because there is no checked-in test runner.
- The most reliable script-level smoke checks from the repo root are:
  - `python3 SurzsEnviro/catchingpackets.py --help`
  - `python3 - <<'PY'
from SurzsEnviro.bootstrap import load_env
ns = load_env()
print("speak" in ns, "reload_all" in ns, "add_script" in ns)
PY`
  - `python3 bootstrap.py` to launch the interactive console; use `exit()` to leave it cleanly

## High-level architecture

- The repo has two main parts that are meant to work together: the `SurzsEnviro/` Python toolkit and the `Exploit_Notes/` markdown knowledge base. The root `bootstrap.py` script loads both into one interactive console so operators can use code and notes in the same session.
- `SurzsEnviro/` is a script-first toolkit, not a normal packaged module tree. Inside that directory, modules use bare imports like `from computerspeak import ComputerSpeak`; the root `SurzsEnviro/bootstrap.py` injects the directory into `sys.path` so those imports still resolve when loaded from the repo root.
- `SurzsEnviro/bootstrap.py` is the dynamic loader. `load_env()` walks the `SurzsEnviro` namespace, imports every module it can, and exposes modules plus top-level symbols into the REPL namespace. It also binds REPL shortcuts like `reload_all()`, `add_script()`, `cs`, `speak()`, and `ec()`, so imports are part of the runtime bootstrap, not just static organization.
- `Exploit_Notes/bootstrap.py` is the note-access boundary. It indexes markdown files and exposes direct note helpers like `notes_list()`, `notes_search()`, and `notes_open()` into the interactive console.
- `SurzsEnviro/target_config.py` is the shared runtime configuration boundary. It stays environment-first by default, prints the active runtime scope values at import time for guardrails, and exposes `prompt_for_missing()` for workflows that really do want interactive prompting.
- `SurzsEnviro/computerspeak.py` is the common shell/logging layer. Other modules lean on it for cross-platform command execution and for logging command output to `SurzsEnviro/SurzalsNotes/SurzalsTexts/command_log.txt`; `whatprocess.py` and `metasploiting.py` build directly on that wrapper instead of shelling out on their own.
- `ComputerSpeak.speak()` is the quick note/log helper for the framework; the bootstrap loader exposes it directly in the REPL as `speak()`.
- `SurzsEnviro/catchingpackets.py` is the most self-contained CLI entry point. It owns live packet capture, pcap analysis, flow tracking, and anomaly reporting, and it resolves relative output paths against the `SurzsEnviro/` directory.
- `SurzsEnviro/netrunning.py`, `packetcraft.py`, `whatprocess.py`, `shellwalking.py`, and `metasploiting.py` are operator helpers around network scanning, packet crafting, process/service control, shell-history collection, and Metasploit RPC access. They are designed to be imported into the shared REPL namespace rather than composed through a packaged API layer.

## Key conventions

- Preserve the repo's two import styles: use package-qualified imports from the repo root (`from SurzsEnviro...`) and keep the existing bare imports inside `SurzsEnviro/` modules unless the whole loading model is being changed intentionally.
- Treat import-time behavior as part of the runtime contract. `target_config.py` announces active scope on import, and `load_env()` depends on module imports having side effects that populate the REPL namespace.
- Avoid accidental import-time prompts. `target_config.py` is environment-first; call `prompt_for_missing()` only when an interactive workflow really needs prompting for missing values.
- Prefer existing helper boundaries over new wrappers: `ComputerSpeak` for shell execution/logging, `NetRunning` for network helpers, `WhatProcess` for process/service scheduling actions, `ShellWalker` for shell-history collection, `PacketCraft` for crafted packet generation, `PacketSniffer` for capture/analysis, and `Pfsense` for pfSense API calls.
- The normal operator workflow is REPL-first. If you change how helpers are exposed or reloaded, preserve `reload_all()`, `notes_reindex()`, and the direct top-level helper exports that `bootstrap.py` makes available.
- Short local aliases are part of the code style in this toolkit (`cs`, `nr`, `wp`, `fc`, `sw`, `ps`, `tf`). Match them when editing nearby code.
- Treat runtime outputs as intentional local artifacts. This code writes into `SurzsEnviro/` and `SurzsEnviro/SurzalsNotes/SurzalsTexts/` instead of hiding artifacts in temp directories.
- Keep `Exploit_Notes/` path semantics stable. The notes loader indexes markdown files recursively and `notes_open()` expects paths relative to the `Exploit_Notes/` root.
- Many older helpers mix return values with `print()` or `ComputerSpeak` side effects. Before refactoring a function to be "cleaner," check whether callers rely on its console/log behavior as much as its return value.
