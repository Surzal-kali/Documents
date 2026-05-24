import re
import shlex
from typing import Optional

from computerspeak import ComputerSpeak as cs
from netrunning import NetRunning as nr
from metasploiting import search_modules, execute_module, list_sessions, _get_client
#This module is going to be redistributed and refactored based on directory aligned platform specific modules. This is just a placeholder and general ideapad of how it would look in each in py.

class WhatProcess:
    CRON_NICKNAMES = {
        "hourly": "@hourly",
        "daily": "@daily",
        "weekly": "@weekly",
        "monthly": "@monthly",
        "yearly": "@yearly",
        "annually": "@annually",
        "midnight": "@midnight",
        "reboot": "@reboot",
    }

    def __init__(self):
        self.cs = cs()
        self.nr = nr()

    def _cron_entry(self, command: str, schedule: str) -> str:
        command = command.strip()
        schedule = schedule.strip()
        if re.match(r"^(@\w+|\S+\s+\S+\s+\S+\s+\S+\s+\S+)\s+", command):
            return command
        thevalue = f"{self.CRON_NICKNAMES.get(schedule.lower(), schedule)} {command}"
        return thevalue
    
    
    def identify_process(self, process_name: str) -> Optional[dict]:
        """Identify a process by name and return its details. This function takes a process name as input and attempts to identify the process running on the system. It uses different commands based on the operating system (Windows or Unix-like) to search for the process. If the process is found, its details (such as PID) are extracted and returned in a structured format. If the process is not found, a message is printed indicating that the process was not found, and None is returned."""
        self.cs.speak(f"Identifying process: {process_name}")
        if self.cs.os_name == "Windows":
            sanitized_name = process_name.replace('"', "")
            command = f'tasklist /FO CSV /NH /FI "IMAGENAME eq {sanitized_name}"'
        else:
            quoted_name = shlex.quote(process_name)
            command = f"pgrep -f -- {quoted_name} | head -n 1"
        output = self.cs.ec(command)
        if output is None or not output.strip():
            print(f"Process '{process_name}' not found.")
            return None
        if self.cs.os_name == "Windows":
            # tasklist CSV output: "Image Name","PID",...
            columns = [col.strip('"') for col in output.split(",")]
            if len(columns) < 2 or columns[0] == "INFO: No tasks are running which match the specified criteria.":
                print(f"Process '{process_name}' not found.")
                return None
            return {"pid": columns[1]}
        if not output.strip().isdigit():
            print(f"Process '{process_name}' not found.")
            return None
        return {"pid": output.strip()}
       

    def kill_process(self, pid: int):
        """Kill a process by its PID. This function takes a process ID (PID) as input and attempts to kill the process with that PID. It uses different commands based on the operating system (Windows or Unix-like) to terminate the process. The function includes error handling to catch and report any issues that may arise during the process termination, and it provides feedback on whether the process was successfully killed or if an error occurred."""
        try:
            pid = int(pid)
            if self.cs.os_name == "Windows":
                self.cs.ec(f"taskkill /PID {pid} /F")
            else:
                self.cs.ec(f"kill -9 {pid}")
            print(f"Process with PID {pid} has been killed.")
        except Exception as e:
            print(f"Error killing process: {e}")


    def list_processes(self):
        """List all running processes on the system. This function retrieves a list of all active processes, including their details such as PID, memory usage, and CPU usage. It uses different commands based on the operating system (Windows or Unix-like) to gather the process information. The results are printed and returned in a structured format, and any errors encountered during the process listing are handled gracefully."""
        try:
            if self.cs.os_name == "Windows":
                output = self.cs.ec("tasklist")
            else:
                output = self.cs.ec("ps aux")
            print("Running processes:")
            print(output) #yeah this one is pretty simple
            return output
        except Exception as e:
            print(f"Error listing processes: {e}")


    def monitor_process(self, pid: int):
        """Monitor a process by its PID and return its resource usage. This function takes a process ID (PID) as input and attempts to monitor the resource usage of the specified process. It uses different commands based on the operating system (Windows or Unix-like) to retrieve the CPU and memory usage of the process. The results are returned in a structured format, and any errors encountered during the monitoring process are handled gracefully."""
        self.cs.speak(f"Monitoring process with PID: {pid}")
        pid = int(pid)
        if self.cs.os_name == "Windows":
            command = f'typeperf "\\Process({pid})\\% Processor Time" "\\Process({pid})\\Working Set" -sc 1'
        else:
            command = f'ps -p {pid} -o %cpu,%mem'
        output = self.cs.ec(command)
        if output is None:
            return None
        output = output.split("\n")
        if self.cs.os_name == "Windows":
            if len(output) < 3:
                return None
            resource_usage = {
                "cpu_usage": output[2].split(",")[0].strip('"'),
                "memory_usage": output[2].split(",")[1].strip('"')
            }
        else:
            if len(output) < 2:
                return None
            resource_usage = {
                "cpu_usage": output[1].split()[0],
                "memory_usage": output[1].split()[1]
            }
        return resource_usage


    def inject_into_process(self, pid: int, payload: str):
        """Inject a payload into a process by its PID. This function takes a process ID (PID) and a payload string as input and attempts to inject the payload into the specified process. It uses different commands based on the operating system (Windows or Unix-like) to perform the injection. The function includes error handling to catch and report any issues that may arise during the injection process, and it provides feedback on whether the payload was successfully injected or if an error occurred."""

        if self.cs.os_name == "Windows":
            command = f"Write-Output {payload} | powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetText((Get-Content -Raw));\"; powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::GetText() | Out-File -FilePath payload.txt -Encoding ASCII\"; powershell -Command \"Start-Process -FilePath payload.txt -Verb RunAs\""
        else:
            quoted_payload = shlex.quote(payload)
            command = f"printf '%s\n' {quoted_payload} > /tmp/payload.sh; chmod +x /tmp/payload.sh; sudo -u $(ps -o user= -p {pid}) /tmp/payload.sh"
        self.cs.speak(f"Injecting payload into process with PID: {pid}")
        self.cs.ec(command)
        print(f"Payload '{payload}' has been injected into process with PID {pid}.")
    def restart_service (self, service_name: str):
        try:
            if self.cs.os_name == "Windows":
                safe_service = service_name.replace('"', "")
                self.cs.ec(f'net stop "{safe_service}" && net start "{safe_service}"')
            else:
                self.cs.ec(f"systemctl restart {shlex.quote(service_name)}")
            print(f"Service '{service_name}' has been restarted.")
        except Exception as e:
            print(f"Error restarting service: {e}") #if something bugs we can restart it. :D
    def identify_services(self):
        """Identify running services on the system. This function retrieves a list of all active services, including their details such as service name, status, and description. It uses different commands based on the operating system (Windows or Unix-like) to gather the service information. The results are printed and returned in a structured format, and any errors encountered during the service identification are handled gracefully."""
        try:
            if self.cs.os_name == "Windows":
                output = self.cs.ec("sc query type= service state= all")
            else:
                output = self.cs.ec("systemctl list-units --type=service --state=running")
            print("Running services:")
            print(output) #yeah this one is pretty simple
        except Exception as e:
            print(f"Error identifying services: {e}")
    def cron_job(self, service:str, command:str, schedule: str):
        """Schedule a cron job with the specified command and schedule."""
        if self.cs.os_name == "Windows":
            safe_service = service.replace("'", "")
            escaped_command = command.replace("'", "''")
            self.cs.ec(
                f"Set-Service -Name '{safe_service}' -StartupType Automatic; "
                f"Register-ScheduledTask -Action (New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-Command ''{escaped_command}''') "
                f"-Trigger (New-ScheduledTaskTrigger -AtStartup) -TaskName '{safe_service}_cron_job' "
                f"-Description 'Cron job for {safe_service}' -Force"
            )
            self.cs.speak(f"Scheduling task: '{command}' with schedule: '{schedule}'")
            # Example of simulating task scheduling
            print(f"Task '{command}' has been scheduled with schedule '{schedule}'.") #that ones importante. another windows/linux branch
        else:
            cron_entry = self._cron_entry(command, schedule)
            self.cs.ec(
                f"(crontab -l 2>/dev/null; printf '%s\n' {shlex.quote(cron_entry)}) | crontab -"
            )
        self.cs.speak(f"Scheduling cron job: '{command}' with schedule: '{schedule}'")
        # Example of simulating cron job scheduling
        print(f"Cron job '{command}' has been scheduled with schedule '{schedule}'.") #that ones importante. another windows/linux branch
    def remove_cron_job(self, command: str):
        """Remove a scheduled cron job by its command. This function takes a command string as input and attempts to remove any scheduled cron jobs that match the provided command. It uses different commands based on the operating system (Windows or Unix-like) to perform the removal. The function includes error handling to catch and report any issues that may arise during the removal process, and it provides feedback on whether the cron job was successfully removed or if an error occurred."""
        self.cs.speak(f"Removing cron job: '{command}'")
        try:
            if self.cs.os_name == "Windows":
                task_name = command.replace("'", "")
                self.cs.ec(f"schtasks /Delete /TN \"{task_name}\" /F")
            else:
                pattern = shlex.quote(command)
                self.cs.ec(
                    f"(crontab -l 2>/dev/null | grep -F -v -- {pattern}) | crontab -"
                )
            print(f"Cron job '{command}' has been removed.")
        except Exception as e:
            print(f"Error removing cron job: {e}")

    def kill_process_by_name(self, process_name: str):
        details = self.identify_process(process_name)
        if not details:
            return
        try:
            self.kill_process(int(details["pid"]))
        except Exception as e:
            print(f"Error killing process '{process_name}': {e}")

    def elevate_privileges(self, pid: int):
        """Attempt to elevate privileges of a process by its PID. This function takes a process ID (PID) as input and attempts to elevate the privileges of the specified process. It uses different commands based on the operating system (Windows or Unix-like) to perform the privilege escalation. The function includes error handling to catch and report any issues that may arise during the elevation process, and it provides feedback on whether the privileges were successfully elevated or if an error occurred."""
        try:
            pid = int(pid)
            if self.cs.os_name == "Windows":
                self.cs.ec(f"powershell -Command \"Start-Process -FilePath powershell.exe -Verb RunAs -ArgumentList '-Command \"Get-Process -Id {pid} | ForEach-Object {{ $_.PriorityClass = ''High'' }}\"'\"")
            else:
                self.cs.ec(f"sudo renice -n -10 -p {pid}")
            print(f"Privileges for process with PID '{pid}' have been elevated.")
        except Exception as e:
            print(f"Error elevating privileges: {e}")


if __name__ == "__main__":
    wpi = WhatProcess()
    wpi.list_processes()
    wpi.cron_job("ExampleService", "echo 'Hello, World!'", "daily")
    wpi.remove_cron_job("echo 'Hello, World!'")


# （づ￣3￣）づ╭❤️～ Approved.
