import argparse
import os
from pathlib import Path
from typing import Any

try:
    import pyshark
except ModuleNotFoundError:
    pyshark = None


_HERE = Path(__file__).resolve().parent
# TODO: Combine with packetcraft once finished.
# [ ] Add more advanced packet analysis features, such as protocol-specific parsing, anomaly detection, and integration with threat intelligence feeds to enhance the capabilities of the PacketSniffer class. This could include support for identifying specific attack patterns, extracting indicators of compromise (IOCs), and providing actionable insights based on the captured network traffic.
# [ ] Implement a user-friendly interface for the PacketSniffer class, allowing users to easily configure capture settings, view real-time packet summaries, and access detailed analysis results. This could involve creating a command-line interface (CLI) with clear options and help messages, as well as providing options for customizing the output format and filtering criteria for captured packets. At the very least, while it still uses pyshark and outputs pcap, we can at least give a documented and colored .md variant. or even csv.
def _require_pyshark():
    if pyshark is None:
        raise ModuleNotFoundError(
            "pyshark is not installed in the active Python environment. "
            "Install dependencies from requirements.txt before using PacketSniffer."
        )


class PacketSniffer:
    def __init__(self, interface: str | None = None):
        self.interface = interface or os.getenv("TARGET_INTERFACE", "wlan0")

    def _resolve_path(self, path_value: str) -> Path:
        path = Path(path_value)
        if not path.is_absolute():
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
        """Capture packets to a pcap file and print a short per-packet summary."""
        _require_pyshark()
        assert pyshark is not None
        if packet_count <= 0:
            raise ValueError("packet_count must be greater than 0.")
        if sniff_time <= 0:
            raise ValueError("sniff_time must be greater than 0.")

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
                print(f"Packet Timestamp: {packet.sniff_time}")
                print(f"Packet Length: {packet.length} bytes")
                if hasattr(packet, "ip"):
                    print(f"Source IP: {packet.ip.src}")
                    print(f"Destination IP: {packet.ip.dst}")
                print("-" * 40)
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
                    output_handle.write(f"Packet Timestamp: {packet.sniff_time}\n")
                    output_handle.write(f"Packet Length: {packet.length} bytes\n")
                    output_handle.write(
                        f"Top Layer: {getattr(packet, 'highest_layer', 'UNKNOWN')}\n"
                    )
                    if hasattr(packet, "ip"):
                        output_handle.write(f"Source IP: {packet.ip.src}\n")
                        output_handle.write(f"Destination IP: {packet.ip.dst}\n")
                    output_handle.write("-" * 40 + "\n")
        finally:
            capture.close()

        print(f"Packet analysis written to {analysis_path}")
        return str(analysis_path)


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
