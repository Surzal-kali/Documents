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
