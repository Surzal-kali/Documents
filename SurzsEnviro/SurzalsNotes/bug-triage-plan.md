## Problem
The codebase has been heavily refactored and shrunk, but the current issue tracking is mostly scattered TODOs and inline comments. The goal is to produce a real bug triage across the full refactor surface, separating blocking defects from cleanup work and turning them into a ranked, actionable backlog.

## Proposed approach
1. Inventory the live entry points and dependencies so triage matches the actual runtime surface.
2. Identify defects that block imports, startup, or core flows, then capture the rest of the visible logic, security, and cleanup issues separately.
3. Convert findings into a severity-ranked bug list with clear reproduction notes and remediation targets.
4. Keep TODO comments out of the triage source of truth unless they map to a concrete bug.

## Todos
- Map the main runtime paths and module dependencies.
- Find broken imports, missing modules, and import-time side effects.
- Review core helpers for obvious runtime and logic defects.
- Group findings by severity and user impact.
- Write the triage backlog in a structured format for follow-up work.

## Notes
- The repository is a flat, script-first Python codebase with direct root-level imports.
- Some modules are referenced but not present at the repo root, so import failures are part of the triage surface.
- There is no repo-level test suite or lint config to lean on, so triage will likely start with static review and import smoke checks.
- This phase is documentation-only: triage findings will be captured in markdown or text artifacts, with no code changes.

## Quick findings from a brief glance
- `fileshuttle.py` is imported by several modules but does not appear to exist at the repo root, which will break `publicface.py`, `whatprocess.py`, and `randomcode.py`.
- `randomcode.py` calls `ori.preflight()`, but `orchestrator.py` only shows `orchestrate()`, so that call path looks broken.
- `target_config.py` prompts at import time, which can block any script that imports it in automation or test-like contexts.
- `shellwalking.py` imports `computerspeak as cs` and then instantiates `cs()`, which looks like a module/class mismatch.
- `NetRunning.brute_scan()` passes a `scripts=` argument into `scan_network()`, but `scan_network()` does not accept that parameter.
- `NetRunning.create_server()` binds the port before launching `http.server` on the same port, so the subprocess likely cannot start.
- `NetRunning.web_payload()` returns from inside a `with socketserver.TCPServer(...)` block, so the server is likely torn down immediately.
- `whatprocess.py` contains a nested `kill_process_by_name()` definition under `remove_cron_job()`, which makes it unreachable as a method.
- `publicface.py` constructs a Metasploit RPC client during initialization, so just creating the facade has heavy side effects.
- In `publicface.py`, those side effects are specific: the constructor eagerly instantiates `NetRunning`, `FileCrawler`, `WhatProcess`, `ComputerSpeak`, `ShellWalker`, `PacketSniffer`, `Tenfold`, and `Orchestrator`, then opens a Metasploit RPC client immediately. That means object creation can prompt for config, touch external services, and fail before any public method is used.
- The `Orchestrator` import/initialization is part of that same chain because `orchestrator.py` imports `target_config.py`, which prompts for missing environment values at import time.
- `trace_route()` also creates a `FileShuttle` instance it never uses, so the helper is doing extra work even on a simple route lookup.
- `catchingshells.py` is still a raw reverse-shell prototype with no argument validation or error handling.
