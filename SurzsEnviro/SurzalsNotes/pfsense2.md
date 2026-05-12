# pfSense API Notes

## 1. Authentication

Authentication is required for all API calls.

### Create a JWT

Source: `[sec1]` / `[sec2]`

```bash
curl -X POST "https://<pf>/api/v2/auth/jwt" \
  -H "Content-Type: application/json" \
  -u "<username>:<password>"
```

### Create an API key

Source: `[sec2]`

```bash
curl -X POST "https://<pf>/api/v2/auth/key" \
  -H "Content-Type: application/json" \
  -u "<username>:<password>" \
  -d '{
        "descr": "automation",
        "hash_algo": "sha256",
        "length_bytes": 24
      }'
```

## 2. Firewall Rules

Core of network environment generation.

### Create a firewall rule

Source: `[sec17]` (`firewall/rule`)

```bash
curl -X POST "https://<pf>/api/v2/firewall/rule" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "interface": "lan",
        "protocol": "tcp",
        "src": "192.168.1.0/24",
        "dst": "any",
        "dst_port": "80",
        "action": "pass"
      }'
```

### List rules

```bash
curl -X GET "https://<pf>/api/v2/firewall/rules" \
  -H "Authorization: Bearer <jwt>"
```

### Apply firewall changes

Source: `[sec17]` (`firewall/apply`)

```bash
curl -X POST "https://<pf>/api/v2/firewall/apply" \
  -H "Authorization: Bearer <jwt>"
```

## 3. NAT

Outbound, port-forward, and 1:1 examples.

### Create a port-forward

Source: `[sec18]` (`firewall/nat/port_forward`)

```bash
curl -X POST "https://<pf>/api/v2/firewall/nat/port_forward" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "interface": "wan",
        "protocol": "tcp",
        "src": "any",
        "dst_port": "8080",
        "target": "192.168.1.10",
        "target_port": "80"
      }'
```

### Set outbound NAT mode

Source: `[sec18]` (`outbound/mode`)

```bash
curl -X PATCH "https://<pf>/api/v2/firewall/nat/outbound/mode" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"mode": "hybrid"}'
```

## 4. Interfaces

VLANs, bridges, GRE, and related interface operations.

### Create a VLAN

Source: `[sec22]` (`interface/vlan`)

```bash
curl -X POST "https://<pf>/api/v2/interface/vlan" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "if": "igb0",
        "tag": 30,
        "descr": "LAB-VLAN30"
      }'
```

### Apply interface changes

Source: `[sec21]` (`interface/apply`)

```bash
curl -X POST "https://<pf>/api/v2/interface/apply" \
  -H "Authorization: Bearer <jwt>"
```

## 5. Routing

Gateways and static routes.

### Create a static route

Source: `[sec23]` (`routing/static_route`)

```bash
curl -X POST "https://<pf>/api/v2/routing/static_route" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "network": "10.50.0.0/24",
        "gateway": "GW_LAB"
      }'
```

## 6. DHCP Server

For auto-building environment subnets.

### Create a DHCP static mapping

Source: `[sec27]` (`dhcp_server/static_mapping`)

```bash
curl -X POST "https://<pf>/api/v2/services/dhcp_server/static_mapping" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "interface": "lan",
        "mac": "aa:bb:cc:dd:ee:ff",
        "ipaddr": "192.168.1.50",
        "hostname": "labnode"
      }'
```

### Apply DHCP changes

Source: `[sec27]` (`dhcp_server/apply`)

```bash
curl -X POST "https://<pf>/api/v2/services/dhcp_server/apply" \
  -H "Authorization: Bearer <jwt>"
```

## 7. DNS Resolver / Forwarder

For environment identity and local naming.

### Create a DNS override

Source: `[sec29]` (`dns_resolver/host_override`)

```bash
curl -X POST "https://<pf>/api/v2/services/dns_resolver/host_override" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "host": "api",
        "domain": "lab.local",
        "ip": "192.168.1.10"
      }'
```

## 8. WireGuard

For remote operator access.

### Create a WireGuard tunnel

Source: `[sec43]` / `[sec44]`

```bash
curl -X POST "https://<pf>/api/v2/vpn/wireguard/tunnel" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "lab-wg",
        "interface": "wan",
        "port": 51820
      }'
```

## 9. System-Level

DNS, hostname, and tunables.

### Set system DNS

Source: `[sec39]` (`system/dns`)

```bash
curl -X PATCH "https://<pf>/api/v2/system/dns" \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"dnsserver": ["1.1.1.1", "9.9.9.9"]}'
```

---

# Network Rules

## Profile 1: Classic 3-Tier Enterprise

**Philosophy:** Hierarchical trust. Users -> Web -> Database. Default allow with restrictive inter-tier rules.

### LAN (Trusted Users - `192.168.1.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP/UDP | LAN net | * | LAN address | 53 | Allow internal DNS |
| 2 | PASS | TCP | LAN net | * | OPT1 net | 80,443 | Web access to DMZ |
| 3 | PASS | TCP | LAN net | * | OPT1 net | 22,3389 | SSH/RDP to DMZ management |
| 4 | PASS | TCP/UDP | LAN net | * | WAN net | 53,123 | DNS/NTP to firewall |
| 5 | PASS | * | LAN net | * | Any | * | General internet access |
| 6 | BLOCK | * | LAN net | * | OPT2 net | * | No direct database access |

### OPT1 (DMZ / Untrusted - `172.19.44.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP | Any | * | OPT1 address | 80,443 | Public web traffic |
| 2 | PASS | TCP | OPT1 net | * | OPT2 net | 3306,5432 | Web -> Database (MySQL/Postgres) |
| 3 | PASS | ICMP | OPT1 net | * | OPT2 net | * | Database health checks |
| 4 | BLOCK | * | OPT1 net | * | LAN net | * | DMZ cannot touch internal users |
| 5 | PASS | * | OPT1 net | * | WAN net | * | Allow DMZ updates (optional) |

### OPT2 (Database / Sensitive - `172.22.91.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP | OPT1 net | * | OPT2 net | 3306,5432 | Allow DMZ web -> database |
| 2 | PASS | TCP | LAN net | * | OPT2 net | 22 | IT admin SSH from LAN |
| 3 | PASS | TCP | LAN net | * | OPT2 net | 3389,5900 | Remote desktop from LAN |
| 4 | BLOCK | * | OPT2 net | * | Any | * | Database cannot initiate outbound |
| 5 | BLOCK | * | Any | * | OPT2 net | * | Default deny inbound |

## Profile 2: Zero-Trust Microsegmented

**Philosophy:** Never trust, always verify. Default deny all inter-VLAN traffic. Explicit allow only.

### Floating rule (apply to all interfaces, place at top)

| # | Action | Proto | Interface | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|---|
| 0 | BLOCK | * | LAN, OPT1, OPT2 | Any | * | RFC1918 (private IPs) | * | Default: block all inter-VLAN |

**Create alias:** `RFC1918 = 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16`  
**Create alias:** `Admin_WKSTN_IP = your jump box IP (for example, 192.168.1.50)`

### LAN (Trusted Users - `192.168.1.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP/UDP | Admin_WKSTN_IP | * | OPT1 net | 22,443 | Jump host -> DMZ management |
| 2 | PASS | TCP/UDP | Admin_WKSTN_IP | * | OPT2 net | 22,3306 | Jump host -> DB access |
| 3 | PASS | * | LAN net | * | WAN net | * | Internet only (no internal access) |
| 4 | PASS | TCP/UDP | LAN net | * | LAN address | 53 | Internal DNS |
| 5 | BLOCK | * | LAN net | * | Any | * | Catch-all block |

### OPT1 (DMZ / Untrusted - `172.19.44.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP | Any | * | OPT1 address | 80,443 | Public HTTP/HTTPS |
| 2 | PASS | TCP | OPT1 net (web server IP) | * | OPT2 net (DB IP) | 3306 | Web server -> specific DB |
| 3 | PASS | ICMP | OPT1 net | * | Admin_WKSTN_IP | * | Health check replies only |
| 4 | BLOCK | * | OPT1 net | * | Any | * | Default block |

**Note:** Rule `#2` should use specific source and destination IPs, not whole subnets.

### OPT2 (Database / Sensitive - `172.22.91.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP | OPT1 net (specific web IP) | * | OPT2 net (specific DB IP) | 3306 | DB listener for web server |
| 2 | PASS | TCP | Admin_WKSTN_IP | * | OPT2 net | 22 | Admin SSH from jump host |
| 3 | BLOCK | * | OPT2 net | * | Any | * | DB cannot initiate anything |
| 4 | BLOCK | * | Any | * | OPT2 net | * | Default deny inbound |

## Profile 3: Cloud-Hybrid Enterprise

**Philosophy:** Cloud-first routing. On-prem DMZ is legacy; OPT2 is the cloud gateway.

### Assumptions

- Cloud VPC: `10.200.0.0/24`
- Site-to-site VPN on OPT2
- Gateway `OPT2_GW` configured in **System > Routing**

### LAN (Corporate Users - `192.168.1.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Gateway | Description |
|---|---|---|---|---|---|---|---|---|
| 1 | PASS | * | LAN net | * | WAN net | * | Default | Internet direct breakout |
| 2 | PASS | * | LAN net | * | 10.200.0.0/24 | * | OPT2_GW | Route to cloud via VPN |
| 3 | PASS | TCP | LAN net | * | OPT1 net | 22,3389 | Default | Legacy DMZ management |
| 4 | BLOCK | * | LAN net | * | OPT2 net | * | Default | No access to VPN gateway itself |
| 5 | BLOCK | * | Any | * | LAN net | * | Default | Default deny |

### OPT1 (Legacy On-Prem DMZ - `172.19.44.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | TCP | Any | * | OPT1 address | 80,443 | Public legacy web traffic |
| 2 | PASS | TCP | OPT1 net | * | WAN net | * | Allow DMZ to update packages |
| 3 | PASS | TCP | OPT1 net | * | 10.200.0.0/24 | 443 | Legacy app -> cloud API |
| 4 | BLOCK | * | OPT1 net | * | LAN net | * | DMZ cannot touch users |
| 5 | BLOCK | * | Any | * | OPT1 net | * | Default deny inbound |

### OPT2 (Cloud Gateway / VPN - `172.22.91.0/24`)

| # | Action | Proto | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|---|
| 1 | PASS | * | LAN net | * | 10.200.0.0/24 | * | Route internal -> cloud |
| 2 | PASS | * | OPT1 net | * | 10.200.0.0/24 | 443 | Legacy DMZ -> cloud API |
| 3 | PASS | * | 10.200.0.0/24 | * | LAN net | * | Cloud -> on-prem resources |
| 4 | PASS | UDP | Any | * | OPT2 address | 500,4500 | IPSec VPN endpoint |
| 5 | BLOCK | * | OPT2 net | * | Any | * | Gateway cannot initiate |
| 6 | BLOCK | * | Any | * | OPT2 net | * | Default deny inbound |

## Quick Reference

| Feature | Classic | Zero-Trust | Cloud-Hybrid |
|---|---|---|---|
| Default stance | Allow with restrictions | Deny all inter-VLAN | Allow with cloud routing |
| LAN -> DMZ | Yes (`80/443/22`) | No, except jump host | Yes, management only |
| DMZ -> DB | Yes (`3306`) | Yes, specific IPs only | N/A |
| LAN -> DB | Blocked | Blocked, except jump host | N/A |
| Cloud routing | No | No | Yes (`10.200.0.0/24` via `OPT2`) |
| Floating block rule | No | Yes (`RFC1918`) | No |
| Special aliases needed | No | Yes (`Admin_WKSTN_IP`, web/db IPs) | No, but VPN required |


# pfSense REST API Cheat Sheet

Simple manual reference for writing `curl` or Python requests against a pfSense-style REST API.

> **Important:** pfSense API paths and payload fields can vary by version and installed API package. Use this sheet for the request shape, then confirm exact endpoint names on your firewall at `https://<pfsense>/api/docs/` or `https://<pfsense>/api/v1/docs/`.

---

## Base Pattern

```text
https://<pfsense-host>/api/v1/<section>/<resource>/<optional-id>
```

Examples:

```text
https://fw.lab/api/v1/interface
https://fw.lab/api/v1/firewall/alias
https://fw.lab/api/v1/firewall/rule
https://fw.lab/api/v1/system/info
```

---

## Common HTTP Verbs

| Verb | Typical use | Shape |
|---|---|---|
| `GET` | list or fetch | `/api/v1/<section>/<resource>` or `/api/v1/<section>/<resource>/<id>` |
| `POST` | create | `/api/v1/<section>/<resource>` |
| `PUT` | replace/update | `/api/v1/<section>/<resource>/<id>` |
| `PATCH` | partial update | `/api/v1/<section>/<resource>/<id>` |
| `DELETE` | remove | `/api/v1/<section>/<resource>/<id>` |

---

## Auth Patterns

### Bearer key + secret

This matches the pattern already used in `pfsense.py` in this repo:

```http
Authorization: Bearer <api_key>:<api_secret>
```

### Bearer token

Some installations use a single token:

```http
Authorization: Bearer <token>
```

### Basic auth

Some setups still allow:

```bash
-u "<username>:<password>"
```

---

## Standard Headers

```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer <api_key>:<api_secret>
```

If your pfSense cert is self-signed, add `-k` to `curl`.

---

## cURL Skeletons

### GET list

```bash
curl -k \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Accept: application/json" \
  "https://$PF/api/v1/<section>/<resource>"
```

### GET single object

```bash
curl -k \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Accept: application/json" \
  "https://$PF/api/v1/<section>/<resource>/<id>"
```

### POST create

```bash
curl -k -X POST \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "example",
    "description": "created from curl"
  }' \
  "https://$PF/api/v1/<section>/<resource>"
```

### PUT update

```bash
curl -k -X PUT \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "example",
    "description": "updated value"
  }' \
  "https://$PF/api/v1/<section>/<resource>/<id>"
```

### DELETE remove

```bash
curl -k -X DELETE \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Accept: application/json" \
  "https://$PF/api/v1/<section>/<resource>/<id>"
```

---

## Python `requests` Skeleton

```python
import json
import requests

PF = "fw.lab"
BASE = f"https://{PF}/api/v1"
HEADERS = {
    "Authorization": "Bearer <api_key>:<api_secret>",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

resp = requests.get(f"{BASE}/<section>/<resource>", headers=HEADERS, verify=False)
print(resp.status_code)
print(resp.json())
```

POST example:

```python
payload = {
    "name": "example",
    "description": "created from python",
}

resp = requests.post(
    f"{BASE}/<section>/<resource>",
    headers=HEADERS,
    data=json.dumps(payload),
    verify=False,
)
print(resp.status_code)
print(resp.json())
```

---

## Common Resource Shapes

These are the patterns you will usually work with most.

## System

```text
GET /api/v1/system/info
GET /api/v1/system/status
```

Use this first to confirm auth and base URL.

## Interfaces

```text
GET /api/v1/interface
GET /api/v1/interface/<name>
PUT /api/v1/interface/<name>
```

Typical identifiers: `wan`, `lan`, `opt1`.

## Firewall aliases

```text
GET    /api/v1/firewall/alias
GET    /api/v1/firewall/alias/<name>
POST   /api/v1/firewall/alias
PUT    /api/v1/firewall/alias/<name>
DELETE /api/v1/firewall/alias/<name>
```

Typical payload:

```json
{
  "name": "LAB_HOSTS",
  "type": "host",
  "address": "192.168.1.10 192.168.1.11",
  "descr": "Lab targets"
}
```

Some APIs use `content` instead of `address`, and `description` instead of `descr`.

## Firewall rules

```text
GET    /api/v1/firewall/rule
GET    /api/v1/firewall/rule/<id>
POST   /api/v1/firewall/rule
PUT    /api/v1/firewall/rule/<id>
DELETE /api/v1/firewall/rule/<id>
```

Typical payload shape:

```json
{
  "interface": "lan",
  "action": "pass",
  "protocol": "tcp",
  "source": {
    "address": "lan"
  },
  "destination": {
    "address": "any",
    "port": "443"
  },
  "descr": "Allow LAN HTTPS out"
}
```

Some APIs flatten fields instead:

```json
{
  "interface": "lan",
  "type": "pass",
  "ipprotocol": "inet",
  "protocol": "tcp",
  "src": "lan",
  "dst": "any",
  "dstport": "443",
  "descr": "Allow LAN HTTPS out"
}
```

## NAT / port forward

```text
GET    /api/v1/firewall/nat/port_forward
POST   /api/v1/firewall/nat/port_forward
PUT    /api/v1/firewall/nat/port_forward/<id>
DELETE /api/v1/firewall/nat/port_forward/<id>
```

Typical payload shape:

```json
{
  "interface": "wan",
  "protocol": "tcp",
  "destination": "wanip",
  "destination_port": "8443",
  "target": "192.168.1.50",
  "local_port": "443",
  "descr": "Forward 8443 to internal host"
}
```

## DHCP / leases

```text
GET /api/v1/dhcp/lease
GET /api/v1/dhcp/lease/<id>
```

## Gateways / routing

```text
GET /api/v1/routing/gateway
GET /api/v1/routing/gateway/<name>
POST /api/v1/routing/gateway
PUT /api/v1/routing/gateway/<name>
DELETE /api/v1/routing/gateway/<name>
```

---

## Apply / Reload Patterns

Configuration APIs often separate **edit** from **apply**.

Common shapes:

```text
POST /api/v1/firewall/apply
POST /api/v1/system/reload
POST /api/v1/interface/reconfigure
```

If you create or change rules and do not see the result live, look for an `apply`, `reload`, `reconfigure`, or `service/restart` endpoint in the docs.

---

## Good Workflow When You Do Not Know the Payload Yet

1. `GET` the collection endpoint first.
2. Copy one existing object.
3. Trim it to the minimum fields you need.
4. `POST` or `PUT` that reduced JSON.
5. If the object changes but behavior does not, call the matching `apply` endpoint.

---

## Error-Check Pattern

When something fails, check these first:

1. Wrong path: singular vs plural resource names vary.
2. Wrong identifier: some endpoints want `id`, others want `name`.
3. Wrong auth format: token vs `key:secret`.
4. Missing JSON header.
5. Missing apply step after config edit.

Quick debug form:

```bash
curl -k -i \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Accept: application/json" \
  "https://$PF/api/v1/<section>/<resource>"
```

---

## Ready-to-Edit Snippets

### List interfaces

```bash
curl -k \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  "https://$PF/api/v1/interface"
```

### Get system info

```bash
curl -k \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  "https://$PF/api/v1/system/info"
```

### Create alias

```bash
curl -k -X POST \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "LAB_HOSTS",
    "type": "host",
    "address": "192.168.1.10 192.168.1.11",
    "descr": "Lab targets"
  }' \
  "https://$PF/api/v1/firewall/alias"
```

### Create basic pass rule

```bash
curl -k -X POST \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "interface": "lan",
    "action": "pass",
    "protocol": "tcp",
    "source": { "address": "lan" },
    "destination": { "address": "any", "port": "443" },
    "descr": "Allow LAN HTTPS out"
  }' \
  "https://$PF/api/v1/firewall/rule"
```

### Apply firewall changes

```bash
curl -k -X POST \
  -H "Authorization: Bearer $API_KEY:$API_SECRET" \
  "https://$PF/api/v1/firewall/apply"
```

---

## Tiny Mental Model

```text
GET    = show me what exists
POST   = create new thing
PUT    = replace existing thing
PATCH  = change part of existing thing
DELETE = remove thing
```

```text
Write path first:
/api/v1/<domain>/<resource>/<id?>

Then add:
- auth header
- json header
- payload
- apply step if needed
```


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
