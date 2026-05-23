import os 
import sys
from pathlib import Path
import shutil
import paramiko

from target_config import TARGET_IP, TARGET_PASSWORD, TARGET_USERNAME

SYS_KEYWORDS = {
    "Source Port","Destination Port",  "Timestamps", "UDP payload", "TCP payload", "HTTP", "DNS", "SSL", "TLS", "FTP", "SMTP", "IMAP", "POP3", "sudo", "nano", "vim", "code", "python", "ssh", "scp", "cat", "ls", "cd", "clear", "dir", "type", "more", "less", "head", "tail", "find", "grep", "awk", "sed", "curl", "wget", "ping", "traceroute", "netstat", "ss", "lsof", "ps", "top", "htop", "systemctl", "service", "journalctl", "grep", "curl", "wget", "ping", "traceroute", "netstat", "ss", "lsof", "ps", "top", "htop", "systemctl", "service",
    "firewall", "ufw", "iptables", "nmap", "dns", "dig", "nslookup", "tcpdump", "wireshark", "pyshark", "scapy", "msfconsole", "msfrpc", "metasploit", "powershell", "bash", "zsh", "history", "env", "printenv", "set", "export", "alias", "unalias", "which", "whereis", "locate", "find", "updatedb", "crontab", "at",
    "docker", "kubectl", "helm", "aws", "az", "gcloud", "tailscale", "ollama", "lm studio", "obs",  "xbox", "epic", "gog", "origin", "uplay", "battle.net", "riot client", "blizzard app", "nvidia geforce experience", "amd radeon software", "intel graphics command center"
}
class ShellWalker ():
    """Designed to crawl through shell history files based on user consent preferences. This includes identifying the shell type (e.g., bash, zsh, powershell), analyzing the system path for custom commands, locating the appropriate history file, and extracting command history while respecting any out-of-scope settings specified by the user. The ShellWalker class is intended to operate within the bounds of user consent, ensuring that only authorized data is collected while providing insights into the shell commands executed during the session. The collected shell history can then be used for further analysis in the digestion process and summarized in the report card."""
    def __init__(self, out_of_scope=None):
        self.out_of_scope_items = {
            item.strip().lower() for item in (out_of_scope or []) if item.strip()
        }
    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items
    def _identify_shell(self):
        """Identify the user's shell type based on environment variables or common shell history file locations. This method checks for the presence of specific history files (e.g., .bash_history, .zsh_history, PowerShell history) to determine the shell being used. The identified shell type is returned as a string, which can then be used to locate and extract command history while respecting user consent preferences and out-of-scope settings."""
        if sys.platform.startswith("win"):
            return "powershell"
        elif os.path.exists(os.path.expanduser("~/.bash_history")):
            return "bash"
        elif os.path.exists(os.path.expanduser("~/.zsh_history")):
            return "zsh"
        else:
            return None
    def _locate_history_file(self, shell_type: str) -> str:
        """Locate the appropriate shell history file based on the identified shell type. This method returns the file path to the shell history file, which can then be used to extract command history while respecting user consent preferences and out-of-scope settings. The method handles different shell types (e.g., bash, zsh, powershell) and their corresponding history file locations."""
        if shell_type == "powershell":
            return os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt")
        elif shell_type == "bash":
            return os.path.expanduser("~/.bash_history")
        elif shell_type == "zsh":
            return os.path.expanduser("~/.zsh_history")
        else:
            return ""
    def _extract_command_history(self, history_file: str) -> list:
        """needs to be rewritten with paramiko and ssh connections in mind, instead of local file access"""
        if not os.path.exists(history_file):
            return []
        with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
 # Debugging point to inspect history file contents before extracting commands
            return f.read().splitlines()
    def crabwalk(self):
        """Crawl through the user's shell history based on identified shell type."""
        if self._is_out_of_scope("shell history"):
 # Debugging point to inspect out-of-scope settings before returning
            return []
        shell_type = self._identify_shell()
        if not shell_type:
  # Debugging point to inspect shell identification results before returning
            return []
        history_file = self._locate_history_file(shell_type)
        if not history_file:
            # 
 # Debugging point to inspect history file location before returning
            return []
        command_history = self._extract_command_history(history_file)
 # Debugging point to inspect command_history
        return command_history
    def check_path(self):
        """Check the system PATH environment variable."""
        if self._is_out_of_scope("system path"):
            return []
        path_env = os.environ.get("PATH", "")
        path_dirs = path_env.split(os.pathsep)
        print(f"System PATH directories: {path_dirs}")
        return path_dirs


    def shell_payload(self):
        """Generate a payload containing shell history and system PATH information based on user consent preferences. This method orchestrates the process of crawling shell history and checking the system PATH while respecting any out-of-scope settings specified by the user. The collected shell history and PATH information can then be used for further analysis in the digestion process and summarized in the report card."""
        shell_history = self.crabwalk()
        # Debugging point to inspect shell_history
        system_path = self.check_path()  
        return {
            "shell_history": shell_history,
            "system_path": system_path,
        } #thanks. it was a fun experiment. whats next? 

    def remote_shell_payload(self, hostname, username, password):
        """Generate a payload containing remote shell history and system PATH information based on user consent preferences. This method establishes an SSH connection to the remote host, retrieves the shell history and system PATH information while respecting any out-of-scope settings specified by the user. The collected remote shell history and PATH information can then be used for further analysis in the digestion process and summarized in the report card."""
        if self._is_out_of_scope("remote shell history") or self._is_out_of_scope("remote system path"):
            return {}
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command('echo $SHELL')
            shell_type = stdout.read().decode().strip()
            history_file = self._locate_history_file(shell_type)
            stdin, stdout, stderr = ssh.exec_command(f'cat {history_file}')
            command_history = stdout.read().decode().splitlines()
            stdin, stdout, stderr = ssh.exec_command('echo $PATH')
            path_env = stdout.read().decode().strip()
            path_dirs = path_env.split(os.pathsep)
            ssh.close()
            return {
                "remote_shell_history": command_history,
                "remote_system_path": path_dirs,
            }
        except Exception as e:
            print(f"Error connecting to remote host: {e}")
            return {}

if __name__ == "__main__":
    shell_walker = ShellWalker()
    payload = shell_walker.remote_shell_payload(TARGET_IP, TARGET_USERNAME, TARGET_PASSWORD)  # Replace with actual remote host details
    print(payload)


def historycall(file: str):
    path = Path(file).expanduser()
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        rawc = handle.read()
    cleanc = rawc.split("---------------------------------------")[-1]
    print(cleanc)
    return cleanc


def build_file_preview(file_path: str):
    selected = Path(file_path).expanduser()
    size_bytes = selected.stat().st_size
    preview = ""
    try:
        if selected.is_file():
            preview = selected.read_text(encoding="utf-8", errors="ignore")[:300]
    except Exception as e:
        preview = f"Could not read file content: {type(e).__name__}: {str(e)}"

    return {
        "enumeration_folder_path": str(selected),
        "enumeration_folder_name": selected.name,
        "enumeration_folder_size_bytes": size_bytes,
        "enumeration_preview": preview,
        "enumeration_details": {},
    }


def crawl_local_files(folder: str | None = None):
    selected_folder = folder
    if selected_folder is None:
        selected_folder = input("Enter the path of the folder to crawl: ").strip()
    if not selected_folder or not os.path.isdir(selected_folder):
        raise ValueError(f"Invalid folder path: {selected_folder}")

    collected_data = []
    for root, _, files in os.walk(selected_folder):
        for name in files:
            file_path = os.path.join(root, name)
            collected_data.append(build_file_preview(file_path))
    print(f"Collected metadata and previews for {len(collected_data)} files from {selected_folder}.")
    return collected_data


MAX_COPY_DEPTH = 2


def filecopy(source_dir, target_bin):
    if not source_dir:
        print("[filecopy] No source directory provided.")
        return

    source = Path(source_dir)
    if not source.is_dir():
        print(f"[filecopy] Source is not a directory: {source_dir}")
        return

    target = Path(target_bin) / source.name
    try:
        for item in source.rglob("*"):
            depth = len(item.relative_to(source).parts)
            if depth > MAX_COPY_DEPTH:
                continue
            dest = target / item.relative_to(source)
            if item.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
    except Exception as e:
        print(f"[filecopy] Error copying {source_dir} to {target_bin}: {e}")

# TODO TRIAGE {priority:P1} {area:remote-shell} {status:open}
# [ ] Normalize remote shell value from echo $SHELL (for example /bin/bash -> bash) before history lookup.
# [ ]Make remote PATH parsing remote-OS aware instead of using local os.pathsep unconditionally.
# [ ] Add SSH port parameter with default fallback.
# [ ] Replace broad exception handling with specific auth/timeout/transport/command failure paths.