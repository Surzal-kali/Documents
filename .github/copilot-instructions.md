# Copilot instructions for this repository

## Build, test, and lint

- Install Python dependencies from the repo root with `python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.md`. The dependency list is checked in as `requirements.md`, not `requirements.txt`.
- There is no committed repo-level build pipeline, lint configuration, or automated test suite in this repository.
- There is no dedicated single-test command because there is no checked-in test runner.
- The most reliable script-level smoke checks from the repo root are:
  - `python3 SurzsEnviro/catchingpackets.py --help`
  - `python3 SurzsEnviro/catchingpackets.py analyze SurzsEnviro/captured_packets.pcap --analysis-file SurzsEnviro/packet_analysis.txt`
  - `python3 bootstrap.py`
  - `python3 SurzsEnviro/payloads/WIP/conquer.py`

## High-level architecture

- The repo has two main parts that are meant to work together: the `SurzsEnviro/` Python toolkit and the `Exploit_Notes/` markdown knowledge base. The root `bootstrap.py` script loads both into one interactive console so operators can use code and notes in the same session.
- `SurzsEnviro/` is a script-first toolkit, not a normal packaged module tree. Inside that directory, modules use bare imports like `from computerspeak import ComputerSpeak`; the root `SurzsEnviro/bootstrap.py` injects the directory into `sys.path` so those imports still resolve when loaded from the repo root.
- `SurzsEnviro/bootstrap.py` is the dynamic loader. `load_env()` walks the `SurzsEnviro` namespace, imports every module it can, and exposes modules plus top-level symbols into the REPL namespace. That means imports are part of the runtime bootstrap, not just static organization.
- `Exploit_Notes/bootstrap.py` is the note-access boundary. It indexes markdown files and exposes direct note helpers like `notes_list()`, `notes_search()`, and `notes_open()` into the interactive console.
- `SurzsEnviro/target_config.py` is the shared runtime configuration boundary. It stays environment-first by default, prints the active runtime scope values each run for guardrails, and exposes `prompt_for_missing()` for workflows that really do want interactive prompting.
- `SurzsEnviro/computerspeak.py` is the common shell/logging layer. Other modules lean on it for cross-platform command execution and for logging command output to `SurzsEnviro/SurzalsNotes/SurzalsTexts/command_log.txt`.
- `ComputerSpeak.speak()` is the quick note/log helper for the framework; the bootstrap loader exposes it directly in the REPL as `speak()`.
- `SurzsEnviro/catchingpackets.py` is the most self-contained CLI entry point. It owns live packet capture, pcap analysis, flow tracking, and anomaly reporting, and it resolves relative output paths against the `SurzsEnviro/` directory.
- `SurzsEnviro/payloads/WIP/conquer.py` is a separate long-running scheduler/stager subsystem. It syncs approved scripts from `~/.conquer/source` (or `%PROGRAMDATA%/Conquer/source` on Windows), merges `execution.json`, copies a fixed dependency set into a working directory, and records runtime logs in `debug_log.txt`.

## Key conventions

- Preserve the repo's two import styles: use package-qualified imports from the repo root (`from SurzsEnviro...`) and keep the existing bare imports inside `SurzsEnviro/` modules unless the whole loading model is being changed intentionally.
- Avoid accidental import-time prompts. `target_config.py` is environment-first; call `prompt_for_missing()` only when an interactive workflow really needs prompting for missing values.
- Prefer existing helper boundaries over new wrappers: `ComputerSpeak` for shell execution/logging, `NetRunning` for network helpers, `WhatProcess` for process/service scheduling actions, `ShellWalker` for shell-history collection, and `PacketSniffer` for capture/analysis work.
- Short local aliases are part of the code style in this toolkit (`cs`, `nr`, `wp`, `fc`, `sw`, `ps`, `tf`). Match them when editing nearby code.
- Treat runtime outputs as intentional local artifacts. This code writes into `SurzsEnviro/`, `SurzsEnviro/SurzalsNotes/SurzalsTexts/`, and `~/.conquer/working` instead of hiding artifacts in temp directories.
- `SurzsEnviro/payloads/` contains hand-maintained deployment-oriented copies, not generated files. If behavior changes in a root runtime module, check whether the corresponding payload copy should change too.
- Many older helpers mix return values with `print()` or `ComputerSpeak` side effects. Before refactoring a function to be "cleaner," check whether callers rely on its console/log behavior as much as its return value.
