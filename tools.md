| Section | Tools | Notes |
|---|---|---|
| **Recon & Discovery** | `nmap`, `masscan`, `subfinder`, `amass`, `httpx`, `waybackurls`, `katana`, `ffuf`, `gobuster` | Pipe-friendly, rate-limited, scriptable. `httpx` + `ffuf` chain naturally. IDE terminal + `jq` for response filtering. |
| **Vulnerability Scanning** | `nuclei`, `trivy`, `testssl.sh`, `hakrawler`, `gau` | `nuclei` uses YAML templates (version-controlled). `trivy` outputs JSON/SBOM. All support `--json`, `--file`, `--quiet`. |
| **Web/API Fuzzing & Auth** | `curl`/`httpie`, `ffuf`, `kiterunner`, `zap-cli` | `zap-cli` wraps OWASP ZAP headless mode. `ffuf` supports wordlists, filters, and JSON output. Easy to alias in `~/.zshrc`. |
| **SAST (Code Security)** | `semgrep`, `bandit`, `gosec`, `detect-secrets`, `gitleaks` | `semgrep` is config-driven, fast, and outputs JSON/SARIF. Rule files live in Git. IDE supports LSP for config validation. |
| **SCA & SBOM** | `syft`, `grype`, `cyclonedx-cli`, `pip-audit`/`npm-audit` | `syft` generates SPDX/CycloneDX JSON. `grype` scans for CVEs. Both are pipeline-native. Output → `jq` → custom risk matrix. |
| **Reporting & Mapping** | `jq`, `yq`, `pandoc`, `markdownlint`, `gh` | Chain JSON → CVSS scoring → ATT&CK mapping → Markdown/HTML. Use `pandoc` for PDF. `gh` integrates with repo issues/PRs. |