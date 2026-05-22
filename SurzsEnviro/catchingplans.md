# core/flow_tracker.py
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

@dataclass
class FlowKey:
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str

    def __hash__(self):
        return hash((self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.protocol))

class FlowTracker:
    def __init__(self, timeout: int = 300):
        self.flows: Dict[FlowKey, Dict] = defaultdict(dict)
        self.timeout = timedelta(seconds=timeout)
        self.flow_history: Dict[FlowKey, List[Dict]] = defaultdict(list)

    def update_flow(self, packet_data: Dict):
        key = FlowKey(
            src_ip=packet_data.get('src_ip', '0.0.0.0'),
            dst_ip=packet_data.get('dst_ip', '0.0.0.0'),
            src_port=packet_data.get('src_port', 0),
            dst_port=packet_data.get('dst_port', 0),
            protocol=packet_data.get('protocol', 'unknown')
        )

        now = datetime.fromtimestamp(packet_data['timestamp'])

        # Initialize flow if new
        if key not in self.flows:
            self.flows[key] = {
                'start_time': now,
                'last_seen': now,
                'bytes': 0,
                'packets': 0,
                'direction': 'unknown'
            }

        # Update flow stats
        self.flows[key]['last_seen'] = now
        self.flows[key]['bytes'] += packet_data.get('length', 0)
        self.flows[key]['packets'] += 1

        # Track direction (first packet determines direction)
        if self.flows[key]['direction'] == 'unknown':
            if packet_data.get('src_ip') == key.src_ip:
                self.flows[key]['direction'] = 'outbound'
            else:
                self.flows[key]['direction'] = 'inbound'

        # Store packet in history
        self.flow_history[key].append(packet_data)

    def get_active_flows(self, cutoff: Optional[datetime] = None) -> List[Dict]:
        cutoff = cutoff or (datetime.now() - self.timeout)
        active = []

        for key, flow in list(self.flows.items()):
            if flow['last_seen'] >= cutoff:
                active.append({
                    'key': key,
                    'duration': (flow['last_seen'] - flow['start_time']).total_seconds(),
                    **flow
                })
            else:
                del self.flows[key]

        return active

    def get_flow_history(self, key: FlowKey) -> List[Dict]:
        return self.flow_history.get(key, [])
# core/anomaly_detector.py
from typing import Dict, List, Callable
import numpy as np
from collections import deque

class AnomalyDetector:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.flow_rates: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.thresholds = {
            'byte_rate': 1000000,  # 1MB/s
            'packet_rate': 1000,   # 1000 packets/s
            'new_flows': 50        # 50 new flows in window
        }

    def update_metrics(self, flows: List[Dict]):
        for flow in flows:
            key = f"{flow['key'].protocol}_{flow['key'].src_ip}"
            self.flow_rates[key].append(flow['bytes'])

    def detect_anomalies(self) -> Dict[str, List[Dict]]:
        anomalies = {
            'high_byte_rate': [],
            'high_packet_rate': [],
            'new_flow_spike': []
        }

        # Check byte rates
        for key, rates in self.flow_rates.items():
            if len(rates) >= self.window_size:
                mean = np.mean(rates)
                std = np.std(rates)
                if mean + 3*std > self.thresholds['byte_rate']:
                    anomalies['high_byte_rate'].append({
                        'flow_key': key,
                        'rate': mean,
                        'threshold': self.thresholds['byte_rate']
                    })

        # Check packet rates (would need packet counts in real implementation)
        # Similar logic to byte rate check

        # Check new flow spikes (would need flow creation tracking)
        # anomalies['new_flow_spike'].append(...)

        return anomalies
# core/engine.py (updated)
from core.flow_tracker import FlowTracker, FlowKey
from core.anomaly_detector import AnomalyDetector
from typing import Dict, List, Optional, Protocol
import pyshark
from pyshark.packet.packet import Packet

class Dissector(Protocol):
    def dissect(self, packet: Packet) -> Dict:
        ...

@dataclass
class DissectionResult:
    packet_id: str
    protocol: str
    data: Dict
    timestamp: float
    is_anomaly: bool = False
    flow_info: Optional[Dict] = None

class DissectionEngine:
    def __init__(self):
        self.dissectors: Dict[str, Dissector] = {}
        self.flow_tracker = FlowTracker()
        self.anomaly_detector = AnomalyDetector()

    def register_dissector(self, protocol: str, dissector: Dissector):
        self.dissectors[protocol] = dissector

    def process_packet(self, packet: Packet) -> Optional[DissectionResult]:
        protocol = packet.highest_layer
        if protocol not in self.dissectors:
            return None

        packet_data = self.dissectors[protocol].dissect(packet)
        packet_data['protocol'] = protocol
        packet_data['timestamp'] = float(packet.sniff_timestamp)

        # Update flow tracking
        self.flow_tracker.update_flow(packet_data)

        # Get active flows
        active_flows = self.flow_tracker.get_active_flows()

        # Update anomaly detection
        self.anomaly_detector.update_metrics(active_flows)

        # Detect anomalies (simplified)
        anomalies = self.anomaly_detector.detect_anomalies()
        is_anomaly = any(anomalies.values())

        return DissectionResult(
            packet_id=packet.number,
            protocol=protocol,
            data=packet_data,
            timestamp=packet_data['timestamp'],
            is_anomaly=is_anomaly,
            flow_info=next((f for f in active_flows if f['key'].protocol == protocol), None)
        )

    def process_capture(self, cap: pyshark.FileCapture | pyshark.LiveCapture) -> List[DissectionResult]:
        results = []
        for packet in cap:
            if result := self.process_packet(packet):
                results.append(result)
        return results

    def get_flow_analysis(self) -> Dict:
        return {
            'active_flows': self.flow_tracker.get_active_flows(),
            'anomalies': self.anomaly_detector.detect_anomalies()
        }
