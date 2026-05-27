import re
import os
import sys

DEFAULTS = {
    "MSF_PASS": "",
    "TARGET_USERNAME": "",
    "TARGET_RANGE": "",
    "TARGET_IP": "",
    "TARGET_INTERFACE": "",
    "TARGET_PASSWORD": "",
    "WORDLIST_PATH": "./wordlist.txt",
    "SELF_IP_RE": "",
    "ZAP_PASS": "",
}

SENSITIVE_VARS = {"MSF_PASS", "TARGET_PASSWORD", "ZAP_PASS"}
CONFIG_SOURCES = {}


def env(variable_name: str, default: str = "", prompt: bool = False) -> str:
    value = os.getenv(variable_name)
    if value not in (None, ""):
        return value
    if prompt and sys.stdin.isatty():
        entered = input(
            f"[*] Please enter a value for {variable_name} (default: '{default}'): "
        ).strip()
        if entered:
            return entered
    return default


def _resolve_config(prompt: bool = False) -> tuple[dict[str, str], dict[str, str]]:
    config = {}
    sources = {}
    for name, default in DEFAULTS.items():
        env_value = os.getenv(name)
        if env_value not in (None, ""):
            config[name] = env_value
            sources[name] = "env"
            continue

        if prompt and sys.stdin.isatty():
            entered = input(
                f"[*] Please enter a value for {name} (default: '{default}'): "
            ).strip()
            if entered:
                config[name] = entered
                sources[name] = "prompt"
                continue

        config[name] = default
        sources[name] = "default" if default else "unset"
    return config, sources


def _display_value(name: str, value: str) -> str:
    if name in SENSITIVE_VARS:
        return "<set>" if value else "<unset>"
    return value if value else "<unset>"


def describe_runtime_scope(config: dict[str, str], sources: dict[str, str]) -> str:
    lines = ["[*] Active target_config runtime scope:"]
    for name in DEFAULTS:
        lines.append(f"    {name} [{sources[name]}] = {_display_value(name, config[name])}")
    return "\n".join(lines)


def _apply_config(config: dict[str, str], sources: dict[str, str]):
    globals().update(config)
    CONFIG_SOURCES.clear()
    CONFIG_SOURCES.update(sources)


def load_config(prompt: bool = False, announce: bool = True) -> dict[str, str]:
    config, sources = _resolve_config(prompt=prompt)
    if announce:
        print(describe_runtime_scope(config, sources))
    return config


def prompt_for_missing() -> dict[str, str]:
    config, sources = _resolve_config(prompt=True)
    _apply_config(config, sources)
    print(describe_runtime_scope(config, sources))
    return config


_CONFIG, _CONFIG_SOURCES = _resolve_config(prompt=False)
_apply_config(_CONFIG, _CONFIG_SOURCES)
print(describe_runtime_scope(_CONFIG, _CONFIG_SOURCES))
MSF_PASS = _CONFIG["MSF_PASS"]
TARGET_USERNAME = _CONFIG["TARGET_USERNAME"]
TARGET_RANGE = _CONFIG["TARGET_RANGE"]
TARGET_IP = _CONFIG["TARGET_IP"]
TARGET_INTERFACE = _CONFIG["TARGET_INTERFACE"]
TARGET_PASSWORD = _CONFIG["TARGET_PASSWORD"]
WORDLIST_PATH = _CONFIG["WORDLIST_PATH"]
SELF_IP_RE = _CONFIG["SELF_IP_RE"]
ZAP_PASS = _CONFIG["ZAP_PASS"]
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
