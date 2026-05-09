# Project: Python Network Chatter Environment for a pfSense Lab

## Goal

Build a **Python-first lab traffic generator** that creates **varied, ordinary-looking network chatter** across systems you own or control. The purpose is to simulate the texture of a lived-in network so you can study logs, alerts, packet captures, timing patterns, and detection quality.

This plan is **not** about persistence, hiding attacks, disguising exfiltration, or blending malicious traffic into background noise. It is only about generating realistic, benign protocol activity inside a lab.

---

## Design Principles

1. **Python only**
   - Use Python 3 as the orchestration and implementation layer.
   - Prefer standard library modules first (`socket`, `ssl`, `http.client`, `asyncio`, `time`, `random`, `json`, `logging`, `pathlib`, `threading`, `subprocess` only when truly needed).
   - Add third-party packages only if they clearly improve realism or packet handling.

2. **Benign protocol behavior**
   - Generate traffic that resembles normal clients using common protocols:
     - DNS
     - HTTP / HTTPS
     - NTP
     - mDNS / local discovery
     - SMB-adjacent port touches only if your lab has services expecting them
     - SSH banner checks only if allowed in the lab
   - No credential stuffing, brute force, exploit delivery, persistence, spoofed identities, or covert channels.

3. **Realism through timing and diversity**
   - Focus on cadence, bursts, retries, idle periods, service mix, and day/night rhythm.
   - Make the chatter feel like workstations, browsers, package updaters, printers, phones, and background services are alive.

4. **Controlled and observable**
   - All targets come from an allowlist or discovered lab inventory.
   - All actions are logged locally.
   - Configuration should make it easy to throttle, pause, and inspect each traffic family.

---

## Phase 1: Inventory and Configuration

### Purpose

Define what the environment is allowed to talk to, what kinds of chatter are enabled, and how noisy it should be.

### Python shape

```python
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Target:
    ip: str
    hostname: str | None = None
    roles: List[str] = field(default_factory=list)
    allowed_protocols: List[str] = field(default_factory=list)


@dataclass
class ChatterProfile:
    name: str
    enabled_protocols: List[str]
    base_interval_seconds: tuple[int, int]
    burst_probability: float
    quiet_hours: tuple[int, int]


@dataclass
class LabConfig:
    interface: str
    targets: List[Target]
    profiles: Dict[str, ChatterProfile]
    dns_server: str | None = None
    ntp_server: str | None = None
```

### What this phase should do

- Load a JSON or YAML config describing:
  - allowed targets
  - target roles (`workstation`, `web`, `printer`, `nas`, `phone`, `infra`)
  - enabled chatter families
  - rate limits
  - quiet hours
- Optionally support lightweight discovery to help populate inventory:
  - ARP table reads
  - ping sweep of the lab subnet
  - reverse DNS lookups
- Keep discovery separate from traffic generation so the system can run from static config if preferred.

### Deliverables

- `config.py` or `models.py` for structured configuration
- `config.json` or `config.yaml`
- `inventory.py` for optional target discovery

---

## Phase 2: Traffic Primitives

### Purpose

Create small, protocol-specific actions that each do one ordinary thing well.

These are the building blocks for more realistic workflows.

### Primitive families

#### 1. DNS lookups

Simulate systems resolving common internal and external-style names.

Examples:
- `printer.lab.local`
- `nas.lab.local`
- `updates.lab.local`
- `api.lab.local`

Python shape:

```python
def do_dns_query(server_ip: str, qname: str, qtype: str = "A") -> None:
    """Send a simple DNS query to a lab resolver and log timing/result."""
```

#### 2. HTTP / HTTPS fetches

Simulate lightweight browsing or service polling.

Examples:
- `GET /`
- `GET /health`
- `GET /favicon.ico`
- `HEAD /`
- `GET /api/status`

Python shape:

```python
def do_http_fetch(host: str, port: int, path: str, use_tls: bool = False) -> None:
    """Perform a small HTTP(S) request with a realistic timeout and headers."""
```

#### 3. Time sync behavior

Simulate periodic NTP checks from endpoints or infrastructure-like systems.

Python shape:

```python
def do_ntp_check(server_ip: str) -> None:
    """Send an NTP client request and record response timing."""
```

#### 4. Local discovery traffic

Simulate common local-network chatter patterns.

Examples:
- mDNS service queries
- occasional NBNS-style lookups
- printer discovery

Python shape:

```python
def do_local_discovery(multicast_group: str, payload_type: str) -> None:
    """Emit a constrained discovery packet for a lab-safe discovery workflow."""
```

#### 5. Service banner checks

Only if the target service is expected and allowed.

Examples:
- connect to TCP/22 and read an SSH banner
- connect to TCP/80 or 443 and close after a header fetch

Python shape:

```python
def do_banner_touch(ip: str, port: int, timeout: float = 2.0) -> None:
    """Open a short-lived socket, observe banner/acceptance, then close cleanly."""
```

### Deliverables

- `protocols/dns_noise.py`
- `protocols/http_noise.py`
- `protocols/ntp_noise.py`
- `protocols/discovery_noise.py`
- `protocols/banner_noise.py`

---

## Phase 3: Traffic Patterns

### Purpose

Turn single protocol actions into believable behavior over time.

### Pattern 1: Jittered timing

Avoid fixed, robotic intervals.

```python
def jittered_sleep(low: float, high: float) -> None:
    """Sleep for a random duration within a bounded range."""
```

### Pattern 2: Bursts

Occasionally create short windows of increased activity, like:
- a browser opening several assets
- a health-check loop
- a printer waking up
- a package cache refresh

```python
def run_burst(actions: list, duration_seconds: int) -> None:
    """Execute a temporary, denser sequence of normal actions."""
```

### Pattern 3: Diurnal rhythm

Traffic should shift over the day:
- **Business hours:** more HTTP, DNS, printer, and local discovery
- **Evening:** lighter browsing and periodic checks
- **Night:** sparse DNS, NTP, and health polling

```python
def current_activity_multiplier(now_hour: int) -> float:
    """Return a scaling factor based on time of day."""
```

### Pattern 4: Role-based behavior

Each synthetic host role should act differently:

- **Workstation**
  - DNS lookups
  - web requests
  - occasional printer discovery
  - software-update style polling

- **Printer**
  - service advertisement
  - occasional status endpoint checks

- **NAS / file host**
  - steady background service presence
  - NTP
  - lightweight HTTP admin polling if enabled

- **Phone / IoT-like**
  - short, bursty, periodic calls
  - discovery traffic
  - sparse HTTP(S) keepalives

### Deliverables

- `patterns.py`
- `profiles.py`

---

## Phase 4: Session and Workflow Simulation

### Purpose

Group primitives into short, ordinary sequences that look more like actual device behavior.

### Example workflow shapes

#### Browser-ish sequence

1. Resolve hostname
2. Open TCP connection
3. Fetch `/`
4. Fetch `/favicon.ico`
5. Fetch one API/status path
6. Pause

#### Update-check sequence

1. Resolve update host
2. HTTPS `HEAD` or small `GET`
3. Wait
4. Retry later with jitter

#### Printer discovery sequence

1. mDNS or discovery query
2. HTTP status page touch
3. Idle for a long period

#### Infrastructure heartbeat

1. NTP sync
2. DNS resolve
3. HTTP health endpoint
4. Sleep until next cycle

### Python shape

```python
class Workflow:
    def __init__(self, name: str):
        self.name = name

    def run_once(self, context) -> None:
        raise NotImplementedError
```

### Deliverables

- `workflows/browserish.py`
- `workflows/update_check.py`
- `workflows/printerish.py`
- `workflows/heartbeat.py`

---

## Phase 5: Scheduler and Runtime

### Purpose

Run many small workflows without everything firing at once.

### Python approach

Use one of:

- `asyncio` for many lightweight network tasks
- `threading` if the code stays mostly blocking and simple

For this project, `asyncio` is a good long-term fit if you want many concurrent, low-cost chatter tasks.

### Runtime responsibilities

- start selected chatter families
- randomize start offsets
- maintain per-profile pacing
- enforce quiet hours
- cap concurrent activity
- support pause / resume / stop

### Python shape

```python
class ChatterRuntime:
    def __init__(self, config: LabConfig):
        self.config = config

    async def run(self) -> None:
        """Launch enabled workflows and keep them scheduled."""
```

### Deliverables

- `runtime.py`
- `scheduler.py`

---

## Phase 6: Logging, Metrics, and Safety Controls

### Purpose

Make the generator easy to inspect and safe to run repeatedly.

### Logging

Record:
- timestamp
- source profile / role
- target IP or host
- protocol
- action
- result
- latency
- error / timeout

Suggested output:
- console summary logs
- newline-delimited JSON log file for later parsing

### Metrics

Track:
- requests per protocol
- successes vs timeouts
- active workflows
- chatter rate by hour

### Safety controls

- allowlist-only targeting
- configurable concurrency cap
- maximum requests per minute
- dry-run mode
- per-protocol enable/disable switches
- graceful stop on signal

### Deliverables

- `logging_setup.py`
- `metrics.py`
- `safety.py`

---

## Phase 7: Command-Line Shape

### Purpose

Keep operation simple while you experiment.

### Example CLI

```text
python3 chatter.py run --config config.json
python3 chatter.py status --config config.json
python3 chatter.py dry-run --config config.json
python3 chatter.py sample-profile workstation
```

### Suggested commands

- `run`
- `dry-run`
- `status`
- `list-targets`
- `sample-profile`
- `validate-config`

### Deliverables

- `chatter.py`
- `cli.py`

---

## Recommended Module Layout

```text
SurzsEnviro/
  chatter.py
  cli.py
  config.py
  inventory.py
  runtime.py
  scheduler.py
  patterns.py
  profiles.py
  logging_setup.py
  metrics.py
  safety.py
  protocols/
    dns_noise.py
    http_noise.py
    ntp_noise.py
    discovery_noise.py
    banner_noise.py
  workflows/
    browserish.py
    update_check.py
    printerish.py
    heartbeat.py
```

---

## Implementation Roadmap

### Stage 1: Foundation

Build:
- config loading
- target inventory
- logging
- one DNS primitive
- one HTTP primitive

Success looks like:
- you can run a single profile against a tiny lab allowlist
- logs clearly show what happened and when

### Stage 2: Realism

Add:
- jitter
- bursts
- role-based profiles
- diurnal scaling
- basic local discovery traffic

Success looks like:
- packet capture shows uneven, mixed, non-robotic traffic
- different target roles produce different protocol blends

### Stage 3: Workflow behavior

Add:
- browser-ish sequences
- update-check loops
- heartbeat workflows
- runtime scheduler

Success looks like:
- captures and logs show short, believable sessions instead of isolated one-off packets

### Stage 4: Control and polish

Add:
- CLI commands
- dry-run mode
- metrics output
- config validation
- better pacing controls

Success looks like:
- the environment is easy to start, tune, observe, and stop cleanly

---

## First Build Order

If you want the shortest path to something useful, build in this order:

1. Config loader
2. DNS primitive
3. HTTP primitive
4. Jittered scheduler
5. Workstation profile
6. Logging and dry-run mode
7. Add discovery, NTP, and workflow sequences

---

## Key Notes

- Keep the first version **small and observable**.
- Realism comes more from **timing, variety, and sequencing** than from raw packet volume.
- Avoid spoofing and avoid generating traffic your lab services would treat as hostile.
- Prefer **ordinary client behavior** over low-level packet crafting unless you have a specific lab reason to go deeper.
- Treat every traffic family as a feature flag so you can compare captures with and without it.
