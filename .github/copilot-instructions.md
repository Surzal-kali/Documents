# Copilot Instructions for SurzsEnviro

## Commands

- Install dependencies: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Run the main facade/orchestration entry point: `python3 publicface.py`
- Run orchestration preflight only: `python3 orchestrator.py`
- Run the Tenfold scheduler/stager loop: `python3 conquer.py`
- There is no committed `tests/` directory, no `pytest`/`unittest` suite, and no repo-level lint configuration (`ruff`, `flake8`, `pylint`, `black`, `mypy`) in this repository right now. Do not invent standard test or lint commands, and there is no repo-defined single-test command yet.

## High-level architecture

- This is a flat, script-first Python codebase, not a packaged module tree. Files import each other directly from the repository root (for example `from netrunning import NetRunning`), so future changes should preserve root-level imports and direct `python3 <file>.py` execution unless the repo is intentionally repackaged.
- `target_config.py` is the shared configuration boundary. It reads core values such as `MSF_PASS`, `TARGET_USERNAME`, `TARGET_RANGE`, `TARGET_IP`, `TARGET_INTERFACE`, `TARGET_PASSWORD`, and `WORDLIST_PATH` from environment variables and prompts interactively when they are unset. Because many modules import `target_config` at module load time, imports can trigger prompts before any real work starts.
- `computerspeak.py` is the common shell/logging layer. `ComputerSpeak.execute_command()` picks Bash vs PowerShell, runs subprocesses, and appends command/output logs to `SurzalsNotes/SurzalsTexts/command_log.txt`. Many other modules use `ComputerSpeak` instead of calling subprocesses directly.
- `publicface.py` is the main facade that wires the subsystems together. Constructing `publicface.publicface` instantiates the network, process, file, shell, packet, scheduler, and orchestrator helpers, creates a Metasploit RPC client, and immediately calls `Orchestrator.preflight()`.
- `orchestrator.py` is the lightweight startup/preflight layer. Its `preflight()` method dynamically imports the attack and collection modules, inspects `/bin` through `FileShuttle.list_directory()`, classifies entries, and writes findings to `rawbin.txt`.
- Network and exploitation capabilities are split across `netrunning.py`, `metasploiting.py`, `catchingpackets.py`, and parts of `dacore.py`. Local collection and host-inspection utilities live in `fileshuttle.py`, `enumeration.py`, `shellwalking.py`, and `whatprocess.py`.
- `conquer.py` is a newer, separate subsystem centered on `Tenfold`. It stages approved scripts from `~/.conquer/source` (or `%PROGRAMDATA%\Conquer\source` on Windows) into a working directory, syncs selected repo dependencies, tracks scheduled runs in `execution.json`, and keeps runtime logs in `debug_log.txt`.

## Key conventions

- Preserve direct-script execution patterns. Several modules have `if __name__ == "__main__"` blocks and are meant to run from the repository root without package installation.
- Follow the existing short helper aliases in nearby code: `cs`, `fs`, `nr`, `wp`, `fc`, `sw`, `ps`, `Or`, `tf`, and `cc`. New code that touches those areas should stay consistent with that local style.
- Reuse the existing helper boundaries instead of adding parallel abstractions: `ComputerSpeak` for shell execution/logging, `FileShuttle` for file operations, `NetRunning` for scanning/network helpers, and `metasploiting.py` for Metasploit RPC access.
- Watch for import-time side effects. Importing modules that transitively pull in `target_config.py` can prompt for configuration, and instantiating `publicface.publicface` also triggers orchestration work immediately.
- Expect artifacts to be written into the repo root or user-scoped runtime folders rather than a dedicated temp directory. Existing code writes files such as `rawbin.txt`, `packet_analysis.txt`, `loud_scan_results.txt`, captured `.pcap` files, `SurzalsNotes/SurzalsTexts/command_log.txt`, and `~/.conquer/**` state.
- Treat `randomcode.py`, `dacore.py`, and `catchingshells.py` as legacy or experimental scripts alongside the newer `conquer.py` scheduler. When extending behavior, prefer keeping existing wiring intact instead of assuming there is a single polished entry point.
