# Repo Scope Audit

## Scope rubric

This repository should stay a **terminal-first operator workspace**, not a packaged application framework.

A file should stay only if it directly supports one of these jobs:

1. **REPL bootstrap** - starts or populates the integrated terminal session.
2. **CLI adapter** - wraps real external tools and normalizes command execution or output.
3. **Parser/state helper** - adds reusable parsing, logging, or lightweight session state.
4. **Knowledge access** - improves note lookup or operator memory inside the terminal.
5. **Workflow helper** - automates a common freelance assessment sequence without turning the repo into an app.

A file should be merged, slimmed down, or removed when it mainly adds:

- app-like facades
- duplicate abstractions
- custom crypto layers
- one-off experiments
- Python wrappers that do not add much beyond bash, PowerShell, or a direct CLI invocation

## Keep when / cut when

| Rule | Keep when | Cut when |
| --- | --- | --- |
| **Bootstrap** | It helps start or populate the operator REPL/session. | It invents a second main app. |
| **CLI adapter** | It wraps real external tools and normalizes execution/output. | It reimplements what shell plus small helpers already do. |
| **Parser/state helper** | It adds reusable parsing, logging, or session state. | It is thin ceremony over one command. |
| **Knowledge access** | It improves note lookup or operator memory inside the terminal. | It duplicates another loader or index. |
| **Workflow module** | It automates a common freelance assessment sequence. | It bundles too many unrelated capabilities. |

## File-by-file recommendations

### Keep

- `bootstrap.py`
- `.github/copilot-instructions.md`
- `SurzsEnviro/bootstrap.py`
- `SurzsEnviro/computerspeak.py`
- `SurzsEnviro/catchingpackets.py`
- `SurzsEnviro/metasploiting.py`
- `SurzsEnviro/shellwalking.py`

### Merge

- `SurzsEnviro/enumeration.py` - fold into a narrower local inspection/helper layer.
- `SurzsEnviro/libraryclass.py` - fold into the root note/bootstrap flow.
- `SurzsEnviro/historystuff.py` - fold into `shellwalking.py` or logging/history helpers.
- `SurzsEnviro/payloads/computerspeak.py` - stop maintaining a second shell adapter.

### Slim down

- `requirements.md` - keep the dependency list, but move toward a normal `requirements.txt`.
- `SurzsEnviro/target_config.py` - keep config, reduce import-time prompting.
- `SurzsEnviro/netrunning.py` - narrow to practical wrappers around external tools.
- `SurzsEnviro/whatprocess.py` - keep only useful operator automation bits.
- `SurzsEnviro/packetcraft.py` - keep only the packet helpers that are truly used.
- `SurzsEnviro/pfsense.py` - keep only if firewall API work is part of real client workflows.
- `SurzsEnviro/payloads/WIP/conquer.py` - keep only if scheduled operator automation is core.

### Remove

- `SurzsEnviro/publicface.py`
- `SurzsEnviro/ideapad.py`
- `ideapad20.py`
- `SurzsEnviro/zerotrust.py`
- `SurzsEnviro/sleepbaby.py`
- `SurzsEnviro/securepacketing.py`
- `SurzsEnviro/payloads/catchingshells.py`
- `SurzsEnviro/packetscripts/target_config.py`
- `SurzsEnviro/.github/copilot-instructions.md`

## Best cleanup order

1. Make `bootstrap.py` and `SurzsEnviro/bootstrap.py` the unquestioned center.
2. Delete duplicate or stale config and instruction files.
3. Collapse tiny helpers like `historystuff`, `libraryclass`, and parts of `enumeration` into one knowledge/inspection layer.
4. Reduce `netrunning` and `whatprocess` to thin automation over real CLI tools.
5. Remove the crypto, secure-packet, and facade side branch entirely.

## Target identity after cleanup

The result should be:

- one operator console
- a handful of strong CLI adapters
- lightweight parsing and session helpers
- integrated notes and memory access
- no fake application layer

That keeps the repository aligned with its intended role as a **script-forward integrated terminal instance for web and threat freelance assessments**.
