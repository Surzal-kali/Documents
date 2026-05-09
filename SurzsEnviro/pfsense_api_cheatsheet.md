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
