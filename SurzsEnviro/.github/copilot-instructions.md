# Copilot instructions for SurzsEnviro

## Build, test, and lint

- Install dependencies with `python3 -m pip install -r requirements.txt`. `REQUIREMENTS.MD` currently mirrors the same dependency list.
- There is no repo-root build pipeline, lint config, or automated test suite checked in here.
- There is no dedicated single-test command at the repo root; verification is mostly script-level.
- The cleanest runnable smoke checks in the current codebase are:
  - `python3 catchingpackets.py --help`
  - `python3 catchingpackets.py sniff --interface wlan0 --packet-count 10 --sniff-time 10 --output-file captured_packets.pcap`
  - `python3 catchingpackets.py analyze captured_packets.pcap --analysis-file packet_analysis.txt`
  - `python3 throwinshells.py`
  - `python3 catchingshells.py <server-host>`

## High-level architecture

- This repo is best understood as a **LotL dev-simulation toolkit** for practicing offensive workflows by hand in code, plus notes for a complementary blue-team/simulation environment. It is not a single packaged app with one entrypoint.
- The root Python files are the active toolkit. `Code-repos/` is a separate stash of external/reference projects and examples; the root modules do not use it as an internal package tree.
- `publicface.py` is the closest thing to a top-level facade. Its constructor wires together the main subsystems (`NetRunning`, `FileCrawler`, `WhatProcess`, `ShellWalker`, `PacketSniffer`, `Tenfold`, `Orchestrator`) and also opens a Metasploit RPC client plus runs `Orchestrator.preflight()`. Instantiating it has real side effects.
- `computerspeak.py` is the shared shell-execution and logging layer. Most other modules rely on it for command execution and message output. On Unix it shells through `/bin/bash -l -c`; on Windows it uses PowerShell. Command output is logged to `SurzalsNotes/SurzalsTexts/command_log.txt`.
- `target_config.py` is the runtime configuration hub for `MSF_PASS`, target host/range/interface/user/password values, the wordlist path, and shared regex constants. Because it calls `env(...)` at import time, configuration lookup is interactive by default.
- The toolkit is split by capability, with overlapping but distinct modules:
  - `netrunning.py` covers network scans, SSH connection checks, payload serving, brute-force helpers, and searchsploit/nmap/masscan wrappers.
  - `metasploiting.py` wraps `pymetasploit3` and centralizes Metasploit RPC actions.
  - `enumeration.py`, `shellwalking.py`, `fileshuttle.py`, and `whatprocess.py` handle host enumeration, shell history inspection, file movement, and process/service/cron manipulation.
  - `dacore.py` is older heavy-duty lab automation logic for scanning, foothold follow-up, and artifact collection.
  - `catchingpackets.py` is the most self-contained CLI and handles live capture plus pcap analysis.
  - `throwinshells.py` and `catchingshells.py` are a simple operator/server and client pair for shell transport experiments.
- `conquer.py` is one subsystem inside that larger toolkit: an async script staging/execution runtime that syncs scripts from `~/.conquer/source` (or `%PROGRAMDATA%/Conquer/source` on Windows), merges an `execution.json` manifest, copies a fixed set of core dependency modules, and runs approved extensions on a schedule.
- `SurzalsNotes/` is not just scratch text. It contains project-direction documents for the surrounding simulation environment, especially the living-off-the-land notes in `aptstuff.md` and the bounded blue-team opponent design in `blueteamopponent.md`.
- `payloads/` contains copied deployment-oriented variants of some runtime modules. These are separate files, not generated artifacts.

## Key conventions

- Expect **import-time prompting** from `target_config.py`. For non-interactive runs, set environment variables before importing modules that depend on it: `MSF_PASS`, `TARGET_RANGE`, `TARGET_INTERFACE`, `TARGET_IP`, `TARGET_USERNAME`, `TARGET_PASSWORD`, and `WORDLIST_PATH`.
- Preserve the repo’s **cross-platform shelling pattern**. Existing code usually branches on the OS and routes execution through `ComputerSpeak` instead of calling `subprocess` directly in each module.
- Treat `publicface.publicface()` as a heavy bootstrap object, not a passive data structure. It triggers Metasploit and orchestration setup immediately.
- Artifact output is intentionally local and visible. The code writes to root-level text files, `SurzalsNotes/SurzalsTexts`, and `~/.conquer/working` rather than hiding outputs in temp directories.
- `conquer.Tenfold` has an implicit packaging contract for staged scripts: if a staged script imports another local module, that dependency must already exist in the working directory or be added to `Tenfold.DEFAULT_CORE_DEPS`.
- `payloads/` files can drift from the root versions. If a change affects deployable runtime behavior, check whether the corresponding file under `payloads/` also needs the same update.
- `catchingpackets.PacketSniffer` resolves relative output files relative to `catchingpackets.py`, not relative to the caller’s current working directory.
- A lot of the older modules mix return values with logging/printing side effects. Before “cleaning up” a function signature, check whether downstream code depends on the printed/logged behavior rather than on a structured return value.
