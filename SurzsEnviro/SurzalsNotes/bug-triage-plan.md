# Bug Triage Report: SurzsEnviro Toolkit

### Issue #13: netrunning.py — Inconsistent SSH Timeout

**File**: netrunning.py:100  
**Type**: Medium (Stability)  
**Status**: ACTUAL BUG  
**Description**: Some SSH operations have `timeout=5`; others have no timeout. Inconsistent behavior leads to unpredictable hangs.  
**Recommendation**: Define a timeout constant and apply consistently

---

### Issue #14: whatprocess.py — Array Bounds Checking Missing

**File**: whatprocess.py:50-51, 95-96  
**Type**: Medium (Runtime Stability)  
**Status**: ACTUAL BUG  
**Description**: Code accesses array indices without checking bounds. Malformed input causes IndexError.  
**Example**: `split_output[n]` without verifying `n < len(split_output)`  
**Recommendation**: Add bounds checks or use slicing with defaults

---

### Issue #15: whatprocess.py — Inverted Logic in Cron Scheduling

**File**: whatprocess.py:32-35  
**Type**: Medium (Logic Error)  
**Status**: ACTUAL BUG  
**Description**: Cron logic ignores the `schedule` parameter when the command already contains cron syntax. Condition inverted—should check if schedule is None/empty, not if it exists.  
**Recommendation**: Verify conditional logic matches intent

---

### Issue #16: whatprocess.py — /tmp Hardcoding with Race Condition

**File**: whatprocess.py:112  
**Type**: Medium (Security/Stability)  
**Status**: ACTUAL BUG  
**Description**: Hardcoded `/tmp/cron_output.txt` creates race condition (multiple processes writing same file) and symlink attack vector. No use of tempfile module.  
**Recommendation**: Use `tempfile.NamedTemporaryFile()` for secure temporary file handling

---

## Cross-Module Analysis

### Import Dependencies

- **Missing modules**: fileshuttle, dacore prevent module loading
- **Impact**: publicface.py and randomcode.py cannot be instantiated
- **Status**: ACTUAL BUG — requires investigation/resolution

### Configuration & Automation

- **Interactive prompting**: target_config.py blocks non-interactive use
- **Impact**: Cannot use toolkit in CI/CD, automated workflows, or headless environments
- **Status**: ACTUAL BUG — breaks automation workflows

### Intentional Offensive Design

- SSH AutoAddPolicy (lab MITM testing)
- HTTPS verification disabled (self-signed cert testing)
- Hardcoded test credentials (lab fallback)
- Shell injection patterns (penetration testing simulation)
- Unvalidated network parameters (rapid enumeration)

### File Handling Issues

- /tmp hardcoding instead of tempfile module — ACTUAL BUG
- No cleanup of temporary files — ACTUAL BUG
- Race conditions on shared temp files — ACTUAL BUG

---

## Recommended Priority Actions

### CRITICAL — Fix These First (Blocking Issues)

1. **Resolve missing imports**: Check if fileshuttle.py and dacore.py should exist or if imports should be removed

### HIGH — Fix These Next (Stability/Hangs)

3. **Array bounds checking**: Add validation before array access in whatprocess.py

### MEDIUM — Fix When Convenient (Logic/Race Conditions)

1. **Cron logic**: Fix inverted condition in whatprocess.py
2. **Temp file handling**: Use tempfile module instead of hardcoded /tmp paths

