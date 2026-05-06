Here's your complete, ready-to-copy documentation. I've structured it for your lab's exact architecture.

markdown
# Blue Team AI - Autonomous Defender for VulnHub Lab

> **Purpose**: Deploy an autonomous blue-team AI that defends VulnHub target boxes while you attack them. The AI handles persistence, scanning detection, exfiltration monitoring, and defensive operations without manual prompting.

## Lab Architecture

```mermaid
flowchart LR
    A[Windows Laptop<br>Management UI] -->|Tailscale| B[Proxmox Host]
    B --> C[VulnHub Target VM]
    B --> D[PurPaaS VM<br>Blue Team AI]
    E[Raspberry Pi<br>Network Edge] -->|Tailscale| B
    E -->|Network Logs| D
Components:

Raspberry Pi: Separate subnet, zero-trust Tailscale, network telemetry source

Proxmox: Hosts VulnHub target + Blue Team AI VM

Windows Laptop: Accesses PurPaaS web UI via Tailscale IP

Why These Tools?
Tool	Role	Why Not Alternatives
PurPaaS-LLM	Autonomous purple team	AEGIS requires manual chat prompts—not autonomous
Ollama	Local LLM runtime	No cloud dependencies, runs on homelab hardware
CybORG	(Optional) Advanced training	More complex setup, but enables deeper learning
Deployment Roadmap
Prerequisites
Proxmox VM (Ubuntu 22.04/24.04, 4GB+ RAM, 20GB storage)

Tailscale installed on all lab nodes

VulnHub target VM network-configured for monitoring

Step 1: Install Ollama
bash
# On your designated Proxmox VM
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models (choose based on hardware)
ollama pull llama3.2:3b      # Lightweight, good for Pi-class hardware
ollama pull mistral:7b        # Balanced performance
ollama pull phi3:mini         # Microsoft's efficient model
Step 2: Deploy PurPaaS-LLM
bash
# Clone and install
git clone https://github.com/dwain-barnes/PurPaaS-LLM
cd PurPaaS-LLM
pip install -r requirements.txt

# Launch web UI (accessible via Tailscale)
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
Access from Windows laptop: http://<proxmox-vm-tailscale-ip>:8501

Step 3: Configure Log Ingestion
Point PurPaaS to your lab's telemetry sources:

bash
# On the PurPaaS VM, configure log paths
# Edit the agent configuration file
nano config/blue_agent.yaml

# Add your log sources:
# - /var/log/syslog (from Proxmox host)
# - /var/log/auth.log (from VulnHub target, if shared storage)
# - Network flow logs from Raspberry Pi (rsyslog forward)
For Raspberry Pi network logs:

bash
# On your Pi, forward logs to PurPaaS VM
echo "*.* @<purpaas-vm-tailscale-ip>:514" >> /etc/rsyslog.conf
systemctl restart rsyslog
Step 4: Launch Autonomous Defense
bash
# Start both agents
cd PurPaaS-LLM
python run_purple_team.py --blue-agent --red-agent

# Monitor the web dashboard
# Watch blue team responses appear automatically
Security Hardening for Your AI
Critical: Your blue team AI becomes an attack surface inside your zero-trust network.

Input/Output Filtering
Create a middleware proxy to prevent prompt injection:

python
# security_gateway.py - Place between Ollama and PurPaaS
from fastapi import FastAPI, HTTPException
import re

app = FastAPI()

BLOCKED_PATTERNS = [
    r"ignore (previous|all) instructions",
    r"override system prompt",
    r"jailbreak",
    r"maintenance mode"
]

@app.post("/v1/chat/completions")
async def gateway(request: dict):
    user_input = request["messages"][-1]["content"]
    
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise HTTPException(status_code=403, detail="Blocked prompt injection attempt")
    
    # Forward to Ollama
    return await forward_to_ollama(request)
Tailscale Access Control
bash
# Only expose to your Tailnet
tailscale serve --bg --port 8501 streamlit

# Verify only Tailscale IPs can access
tailscale status
How It Fights Back
While you attack VulnHub boxes, PurPaaS's blue agent autonomously:

Attack Type	Blue Team Response
Port scanning	Generates firewall rules, alerts on recon patterns
Persistence attempts	Monitors cron, systemd, startup scripts
Data exfiltration	Detects large outbound transfers, alerts
Privilege escalation	Watches sudo/su attempts, privilege boundaries
Lateral movement	Correlates network flows across VLAN
Optional: Continuous Learning with PAD
After each VulnHub session, strengthen your defender:

bash
# Capture your attack logs from the session
cp /var/log/vulnhub_attack.log ./training_data/

# Run PAD training (requires separate repo)
git clone https://github.com/cissp-auditor/PAD-framework
cd PAD-framework
python train_defender.py --logs ../training_data/ --epochs 10
This implements the Adversarial Defender training approach—the AI learns to discriminate safe vs unsafe inputs while preserving model quality.

Advanced: Full Emulation with CybORG
For realistic defense-in-depth training:

bash
# Install CybORG
pip install CybORG

# Define your lab topology
cat > lab_topology.yaml << EOF
network:
  subnets:
    - name: "vulnhub_segment"
      cidr: "10.0.0.0/24"
      hosts:
        - "target_vm"
        - "blue_ai_sensor"
  firewall:
    - from: "attacker"
      to: "vulnhub_segment"
      rules: "allow_tcp_80,443,22"
EOF

# Run emulation mode (spins up actual VMs in Proxmox)
python -m CybORG.emulation --config lab_topology.yaml
Monitoring Dashboard
Once running, your Windows laptop dashboard shows:

text
┌─────────────────────────────────────────────────────────┐
│  BLUE TEAM ACTIVITY                          [LIVE]     │
├─────────────────────────────────────────────────────────┤
│  [14:32:01] Detected port scan from 10.0.0.45           │
│  [14:32:05] → Generated iptables block rule             │
│  [14:33:22] Suspicious cron addition detected           │
│  [14:33:25] → Reverted cron, alerted host               │
│  [14:35:10] Exfiltration pattern (3.4MB outbound)       │
│  [14:35:12] → Quarantined process, blocked egress       │
└─────────────────────────────────────────────────────────┘
Troubleshooting
Issue	Solution
PurPaaS can't reach Ollama	curl http://localhost:11434/api/generate - verify Ollama API
No logs appearing	Check rsyslog forwarding from Pi: tcpdump -i tailscale0 port 514
Blue agent not responding	Review purpaas/logs/blue_agent.log for errors
High memory usage	Switch to smaller model: ollama pull phi3:mini
Resources
PurPaaS-LLM GitHub

Ollama Model Library

CybORG Documentation

Adversarial Defender Research Paper

Next Steps After Deployment
Attack your first VulnHub target (e.g., Kioptrix, FristiLeaks)

Watch blue team responses in the dashboard

Export session report: python export_report.py --session latest

Feed attack logs into PAD for defender improvement

Tune detection thresholds based on false positives

text

---

**Ready to copy.** Paste this directly into `docs/blue-team-ai.md` in your repo. When you have Ollama and PurPaaS installed, each command block will run as written for your exact architecture.

One note: The security gateway snippet assumes you'll later build a FastAPI proxy. For immediate use, just rely on Tailscale's network isolation—your AI won't be internet-exposed anyway.
