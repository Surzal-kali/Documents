import os
from pathlib import Path
import subprocess  
import platform
import time
#cause this will be so much fun for automation! we can figure out so much about each host :D

class ComputerSpeak:
    """So I understand you can just use shutil, but its alot easier, in my brain, to just wrap it in python. I keep, and only use for logging purposes and special chains."""
    def __init__(self):
        """Initialize the ComputerSpeak class and detect the operating system."""
        self.os_name = platform.system()
        self.log_path = Path(__file__).resolve().parent / "SurzalsNotes" / "SurzalsTexts" / "command_log.txt"
        if self.os_name not in ["Windows", "Linux", "Darwin"]:
            raise NotImplementedError(f"Unsupported operating system: {self.os_name}")
        else: # Debugging point to inspect OS detection results
            self.command_prefix = self.get_command_prefix()
    #k this module is kind of imporante. it also doesn't work 
    
    def get_command_prefix(self):
            """Return the appropriate command prefix based on the operating system."""
            if "TERMUX_VERSION" in os.environ:
                return "/bash -c"
            #note this feature does nothing right now, android still errors as its not fully implemented.
            
            if self.os_name in ["Linux", "Darwin"]:
                return "/bin/bash -l -c "
            if self.os_name == "Windows":
                return "powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "
            raise NotImplementedError(f"Unsupported operating system: {self.os_name}")


    def _write_log(self, command: str, output: str): 
        """Write the executed command and its output to a log file with a timestamp."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"{timestamp} - Executed: {command}\nOutput: {output}\n{'-'*40}\n"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

    def _build_command_args(self, command: str):
        """Build a subprocess argument list from the detected command prefix."""
        if self.os_name == "Windows":
            command = "$ErrorActionPreference = 'Stop'; " + command
            return ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", command]
        elif self.os_name in ["Linux", "Darwin"]:
            return ["/bin/bash", "-l", "-c", command]
        else:
            raise NotImplementedError(f"Unsupported operating system: {self.os_name}")

    def ec(self, command: str):
        """Execute a command on the system and log the output."""
        try:
            args = self._build_command_args(command)
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            self._write_log(command, output)
            return output
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.strip() if e.stderr else str(e)
            print(f"Command failed ({e.returncode}): {error_output}")
            self._write_log(command, f"ERROR ({e.returncode}): {error_output}")
            return None
     


    def fuzz_command(self, command_template: str, fuzz_values: list):
        """Fuzz a command by replacing a placeholder with different values and executing it."""
        for value in fuzz_values:
            command = command_template.replace("FUZZ", value)
            print(f"Fuzzing with value: {value}")
            self.ec(command)
    def fuzz_command_loop(self, command_template: str, fuzz_values: list, iterations: int):
        for i in range(iterations):
            for value in fuzz_values:
                command = command_template.replace("FUZZ", value)
                print(f"Iteration {i+1}/{iterations}, Fuzzing with value: {value}")
                self.ec(command)
                time.sleep(1)  # Sleep to avoid overwhelming the system; adjust as needed

    def speak(self, message: str):
        """Print and log a quick note without shelling out."""
        note = str(message)
        print(note)
        self._write_log("speak()", note)
        return note

if __name__ == "__main__":
    csi = ComputerSpeak()
    csi.speak("Hello, this is a test message from ComputerSpeak!")

    #need to build this out for YOU my ai assistant specifically to bridge the gap between python and shell commands. its going to be a bit rough around the edges but it should work for the most part. we can always refactor later if we need to. (it is my fav function despite being a subproccess wrapper)