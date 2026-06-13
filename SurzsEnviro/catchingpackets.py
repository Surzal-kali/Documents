import argparse
import os
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path
from statistics import mean, pstdev
from time import sleep
from typing import Any, Callable
import time
try:
    import pyshark
except ModuleNotFoundError:
    pyshark = None

#TODO: Import an easier function to call and resolve event threading and privilige issues. 

_HERE = Path(__file__).resolve().parent
def _require_pyshark():
    if pyshark is None:
        raise ModuleNotFoundError(
            "pyshark is not installed in the active Python environment. "
            "Install dependencies from requirements.md before using PacketSniffer."
        )


@dataclass(frozen=True)
class FlowKey:
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str


class FlowTracker:
    def __init__(self, timeout: int = 300):
        self.flows: dict[FlowKey, dict[str, Any]] = defaultdict(dict)
        self.timeout = timedelta(seconds=timeout)
        self.flow_history: dict[FlowKey, list[dict[str, Any]]] = defaultdict(list)

    def update_flow(self, packet_data: dict[str, Any]) -> FlowKey:
        key = FlowKey(
            src_ip=packet_data.get("src_ip", "0.0.0.0"),
            dst_ip=packet_data.get("dst_ip", "0.0.0.0"),
            src_port=packet_data.get("src_port", 0),
            dst_port=packet_data.get("dst_port", 0),
            protocol=packet_data.get("protocol", "unknown"),
        )

        now = datetime.fromtimestamp(packet_data["timestamp"])

        if key not in self.flows:
            self.flows[key] = {
                "start_time": now,
                "last_seen": now,
                "bytes": 0,
                "packets": 0,
                "direction": "unknown",
            }

        self.flows[key]["last_seen"] = now
        self.flows[key]["bytes"] += packet_data.get("length", 0)
        self.flows[key]["packets"] += 1

        if self.flows[key]["direction"] == "unknown":
            self.flows[key]["direction"] = "outbound"

        self.flow_history[key].append(packet_data)
        return key

    def get_active_flows(self, cutoff: datetime | None = None) -> list[dict[str, Any]]:
        cutoff = cutoff or (datetime.now() - self.timeout)
        active = []

        for key, flow in list(self.flows.items()):
            if flow["last_seen"] >= cutoff:
                active.append(
                    {
                        "key": key,
                        "duration": (flow["last_seen"] - flow["start_time"]).total_seconds(),
                        **flow,
                    }
                )
            else:
                del self.flows[key]

        return active

    def get_flow_history(self, key: FlowKey) -> list[dict[str, Any]]:
        return self.flow_history.get(key, [])


class AnomalyDetector:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.flow_byte_rates: dict[str, deque[int]] = defaultdict(
            lambda: deque(maxlen=window_size)
        )
        self.flow_packet_rates: dict[str, deque[int]] = defaultdict(
            lambda: deque(maxlen=window_size)
        )
        self.thresholds = {
            "byte_rate": 1_000_000,
            "packet_rate": 1000,
        }

    def update_metrics(self, flows: list[dict[str, Any]]) -> None:
        for flow in flows:
            flow_key = flow["key"]
            key = f"{flow_key.protocol}_{flow_key.src_ip}_{flow_key.dst_ip}"
            duration = max(flow.get("duration", 0.0), 1.0)
            byte_rate = int(flow.get("bytes", 0) / duration)
            packet_rate = int(flow.get("packets", 0) / duration)
            self.flow_byte_rates[key].append(byte_rate)
            self.flow_packet_rates[key].append(packet_rate)

    def _is_spike(self, values: deque[int], hard_threshold: int) -> bool:
        if len(values) < max(5, self.window_size // 4):
            return False
        current = values[-1]
        avg = mean(values)
        std = pstdev(values)
        dynamic_threshold = avg + (3 * std)
        return current > hard_threshold or current > dynamic_threshold

    def detect_anomalies(self) -> dict[str, list[dict[str, Any]]]:
        anomalies: dict[str, list[dict[str, Any]]] = {
            "high_byte_rate": [],
            "high_packet_rate": [],
        }

        for key, rates in self.flow_byte_rates.items():
            if self._is_spike(rates, self.thresholds["byte_rate"]):
                anomalies["high_byte_rate"].append(
                    {
                        "flow_key": key,
                        "rate": rates[-1],
                        "threshold": self.thresholds["byte_rate"],
                    }
                )

        for key, rates in self.flow_packet_rates.items():
            if self._is_spike(rates, self.thresholds["packet_rate"]):
                anomalies["high_packet_rate"].append(
                    {
                        "flow_key": key,
                        "rate": rates[-1],
                        "threshold": self.thresholds["packet_rate"],
                    }
                )

        return anomalies


@dataclass
class DissectionResult:
    packet_id: str
    protocol: str
    data: dict[str, Any]
    timestamp: float
    is_anomaly: bool = False
    flow_info: dict[str, Any] | None = None


class DissectionEngine:
    def __init__(self):
        self.dissectors: dict[str, Callable[[Any], dict[str, Any]]] = {}
        self.flow_tracker = FlowTracker()
        self.anomaly_detector = AnomalyDetector()

    def register_dissector(self, protocol: str, dissector: Callable[[Any], dict[str, Any]]) -> None:
        self.dissectors[protocol] = dissector

    def _default_dissect(self, packet: Any) -> dict[str, Any]:
        data: dict[str, Any] = {
            "length": int(getattr(packet, "length", 0) or 0),
        }
        if hasattr(packet, "ip"):
            data["src_ip"] = getattr(packet.ip, "src", "0.0.0.0")
            data["dst_ip"] = getattr(packet.ip, "dst", "0.0.0.0")
        else:
            data["src_ip"] = "0.0.0.0"
            data["dst_ip"] = "0.0.0.0"

        if hasattr(packet, "tcp"):
            data["src_port"] = int(getattr(packet.tcp, "srcport", 0) or 0)
            data["dst_port"] = int(getattr(packet.tcp, "dstport", 0) or 0)
        elif hasattr(packet, "udp"):
            data["src_port"] = int(getattr(packet.udp, "srcport", 0) or 0)
            data["dst_port"] = int(getattr(packet.udp, "dstport", 0) or 0)
        else:
            data["src_port"] = 0
            data["dst_port"] = 0

        return data

    def process_packet(self, packet: Any) -> DissectionResult:
        protocol = str(getattr(packet, "highest_layer", "UNKNOWN")).upper()
        dissector = self.dissectors.get(protocol, self._default_dissect)
        packet_data = dissector(packet)
        packet_data["protocol"] = protocol
        packet_data["timestamp"] = float(getattr(packet, "sniff_timestamp", 0.0) or 0.0)

        tracked_key = self.flow_tracker.update_flow(packet_data)
        active_flows = self.flow_tracker.get_active_flows()
        self.anomaly_detector.update_metrics(active_flows)
        anomalies = self.anomaly_detector.detect_anomalies()

        is_anomaly = any(anomalies.values())
        flow_info = next((flow for flow in active_flows if flow["key"] == tracked_key), None)
    
        return DissectionResult(
            packet_id=str(getattr(packet, "number", "0")),
            protocol=protocol,
            data=packet_data,
            timestamp=packet_data["timestamp"],
            is_anomaly=is_anomaly,
            flow_info=flow_info,
        )

    def get_flow_analysis(self) -> dict[str, Any]:
        return {
            "active_flows": self.flow_tracker.get_active_flows(),
            "anomalies": self.anomaly_detector.detect_anomalies(),
        }


class PacketSniffer:
    def __init__(self, interface: str | None = None):
        self.interface = interface or os.getenv("TARGET_INTERFACE", "wlan0")
        self.engine = DissectionEngine()

    def _get_layer_field(self, packet: Any, layer_name: str, field_name: str) -> Any | None:
        layer = getattr(packet, layer_name, None)
        if layer is None:
            return None
        return getattr(layer, field_name, None)

    def _get_layer_option(self, packet: Any, layer_name: str, option_name: str) -> Any | None:
        layer = getattr(packet, layer_name, None)
        if layer is None:
            return None
        try:
            return layer.option_value(option_name)
        except AttributeError:
            return None

    def wait_for_new_device(self, timeout: int = 30) -> dict[str, str] | None:
        """Wait for a new device to connect to the network.
        Returns a dict {'ip': str|None, 'mac': str|None, 'proto': 'arp'|'bootp'|...}
        or None if nothing was seen within `timeout`.
        """
        _require_pyshark()
        assert pyshark is not None
        capture = pyshark.LiveCapture(interface=self.interface, bpf_filter="arp or (udp and port 67)")
        start_time = datetime.now()
        try:
            for packet in capture.sniff_continuously():
                if (datetime.now() - start_time).total_seconds() > timeout:
                    break

                arp_layer_present = getattr(packet, "arp", None) is not None
                arp_op = self._get_layer_field(packet, "arp", "op")
                if arp_op == "1" or (arp_op is None and arp_layer_present):
                    new_device_ip = (
                        self._get_layer_field(packet, "arp", "psrc")
                        or self._get_layer_field(packet, "ip", "src")
                    )
                    new_device_mac = (
                        self._get_layer_field(packet, "arp", "hwsrc")
                        or self._get_layer_field(packet, "eth", "src")
                    )
                    if not new_device_ip and not new_device_mac:
                        continue
                    return {"ip": new_device_ip, "mac": new_device_mac, "proto": "arp"}

                if self._get_layer_option(packet, "bootp", "message-type") == "discover":
                    new_device_mac = (
                        self._get_layer_field(packet, "eth", "src")
                        or self._get_layer_field(packet, "bootp", "chaddr")
                    )
                    if not new_device_mac:
                        continue
                    return {"ip": None, "mac": new_device_mac, "proto": "bootp"}
        finally:
            capture.close()

        return None
    

    
    def _resolve_path(self, path_value: str) -> Path:
        path = Path(path_value)
        if not path.is_absolute():
            cwd_path = Path.cwd() / path
            if cwd_path.exists() or (
                path.parts and path.parts[0] == _HERE.name and cwd_path.parent.exists()
            ):
                path = cwd_path
            else:
                path = _HERE / path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def start_sniffing(
        self,
        packet_count: int = 300,
        sniff_time: int = 600,
        filter: str = "",
        output_file: str = "captured_packets.pcap",
    ) -> str:
        """Capture packets to a pcap file and print live flow/anomaly summaries."""
        _require_pyshark()
        assert pyshark is not None
        if packet_count <= 0:
            raise ValueError("packet_count must be greater than 0.")
        if sniff_time <= 0:
            raise ValueError("sniff_time must be greater than 0.")

        self.engine = DissectionEngine()

        save_path = self._resolve_path(output_file)
        capture = None

        try:
            capture_kwargs: dict[str, Any] = {
                "interface": self.interface,
                "output_file": str(save_path),
            }
            if filter:
                capture_kwargs["bpf_filter"] = filter

            capture = pyshark.LiveCapture(**capture_kwargs)
            print(f"Capturing on {self.interface}... Press Ctrl+C to stop early.")
            capture.sniff(packet_count=packet_count, timeout=sniff_time)

            for packet in capture:
                result = self.engine.process_packet(packet)
                print(f"Packet Timestamp: {packet.sniff_time}")
                print(f"Packet Length: {packet.length} bytes")
                print(f"Top Layer: {result.protocol}")
                if hasattr(packet, "ip"):
                    print(f"Source IP: {packet.ip.src}")
                    print(f"Destination IP: {packet.ip.dst}")
                if result.flow_info is not None:
                    key = result.flow_info["key"]
                    print(
                        "Flow: "
                        f"{key.src_ip}:{key.src_port} -> {key.dst_ip}:{key.dst_port} ({key.protocol})"
                    )
                    print(
                        f"Flow Stats: packets={result.flow_info['packets']} "
                        f"bytes={result.flow_info['bytes']} "
                        f"duration={result.flow_info['duration']:.2f}s"
                    )
                if result.is_anomaly:
                    print("Anomaly: potential rate spike detected")
                print("-" * 40)

            flow_analysis = self.engine.get_flow_analysis()
            print("Flow Analysis Summary")
            print(f"Active flows: {len(flow_analysis['active_flows'])}")
            print(
                f"High byte-rate alerts: {len(flow_analysis['anomalies']['high_byte_rate'])}"
            )
            print(
                f"High packet-rate alerts: {len(flow_analysis['anomalies']['high_packet_rate'])}"
            )
        finally:
            if capture is not None:
                capture.close()

        print(f"Captured packets saved to {save_path}")
        return str(save_path)

    def analyze_capture(
        self,
        capture_path: str,
        analysis_file: str = "packet_analysis.txt",
    ) -> str:
        """Read a pcap file and write a plain-text summary of each packet."""
        _require_pyshark()
        assert pyshark is not None
        source_path = self._resolve_path(capture_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Capture file not found: {source_path}")

        analysis_path = self._resolve_path(analysis_file)
        capture = pyshark.FileCapture(input_file=str(source_path), keep_packets=False)

        try:
            with analysis_path.open("w", encoding="utf-8") as output_handle:
                for packet in capture:
                    result = self.engine.process_packet(packet)
                    output_handle.write(f"Packet Timestamp: {packet.sniff_time}\n")
                    output_handle.write(f"Packet Length: {packet.length} bytes\n")
                    output_handle.write(
                        f"Top Layer: {getattr(packet, 'highest_layer', 'UNKNOWN')}\n"
                    )
                    if hasattr(packet, "ip"):
                        output_handle.write(f"Source IP: {packet.ip.src}\n")
                        output_handle.write(f"Destination IP: {packet.ip.dst}\n")
                    if result.flow_info is not None:
                        output_handle.write(
                            "Flow: "
                            f"{result.flow_info['key'].src_ip}:{result.flow_info['key'].src_port} -> "
                            f"{result.flow_info['key'].dst_ip}:{result.flow_info['key'].dst_port} "
                            f"({result.flow_info['key'].protocol})\n"
                        )
                        output_handle.write(
                            f"Flow Stats: packets={result.flow_info['packets']} "
                            f"bytes={result.flow_info['bytes']} "
                            f"duration={result.flow_info['duration']:.2f}s\n"
                        )
                    if result.is_anomaly:
                        output_handle.write("Anomaly: potential rate spike detected\n")
                    output_handle.write("-" * 40 + "\n")

                flow_analysis = self.engine.get_flow_analysis()
                output_handle.write("\n=== Flow Analysis Summary ===\n")
                output_handle.write(
                    f"Active flows: {len(flow_analysis['active_flows'])}\n"
                )
                output_handle.write(
                    f"High byte-rate alerts: {len(flow_analysis['anomalies']['high_byte_rate'])}\n"
                )
                output_handle.write(
                    f"High packet-rate alerts: {len(flow_analysis['anomalies']['high_packet_rate'])}\n"
                )
        finally:
            capture.close()

        print(f"Packet analysis written to {analysis_path}")
        return str(analysis_path)
    
    def start_thread(self):
        import threading
        thread = threading.Thread(target=self.start_sniffing, daemon=True)
        thread.start()
        sleep(300)  # Give the thread a moment to start
        return thread

def main() -> int:
    parser = argparse.ArgumentParser(description="Capture and analyze network packets.")
    subparsers = parser.add_subparsers(dest="command")

    sniff_parser = subparsers.add_parser("sniff", help="Capture live traffic to a pcap file.")
    sniff_parser.add_argument("--interface", default=None, help="Network interface to capture on.")
    sniff_parser.add_argument("--packet-count", type=int, default=300, help="Max packets to capture.")
    sniff_parser.add_argument("--sniff-time", type=int, default=600, help="Capture timeout in seconds.")
    sniff_parser.add_argument("--filter", default="", help="Optional BPF filter string.")
    sniff_parser.add_argument(
        "--output-file",
        default="captured_packets.pcap",
        help="PCAP output file path.",
    )

    analyze_parser = subparsers.add_parser("analyze", help="Write a text summary from a pcap file.")
    analyze_parser.add_argument("capture_path", help="Path to a pcap file.")
    analyze_parser.add_argument(
        "--analysis-file",
        default="packet_analysis.txt",
        help="Text output file path.",
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    sniffer = PacketSniffer(interface=getattr(args, "interface", None))

    if args.command == "sniff":
        sniffer.start_sniffing(
            packet_count=args.packet_count,
            sniff_time=args.sniff_time,
            filter=args.filter,
            output_file=args.output_file,
        )
        return 0

    if args.command == "analyze":
        sniffer.analyze_capture(
            capture_path=args.capture_path,
            analysis_file=args.analysis_file,
        )
        return 0

    parser.print_help()
    return 1



if __name__ == "__main__":
    raise SystemExit(main())
