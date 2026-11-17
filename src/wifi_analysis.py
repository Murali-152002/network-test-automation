"""Analyse 802.11 management frames in a pcap."""
from collections import Counter
from scapy.all import rdpcap
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeReq


def frame_counts(pcap_path):
    counts = Counter()
    for pkt in rdpcap(pcap_path):
        if pkt.haslayer(Dot11Beacon):
            counts["beacon"] += 1
        elif pkt.haslayer(Dot11ProbeReq):
            counts["probe_request"] += 1
        elif pkt.haslayer(Dot11):
            counts["other"] += 1
    return counts


def beacon_ssids(pcap_path):
    ssids = set()
    for pkt in rdpcap(pcap_path):
        if pkt.haslayer(Dot11Beacon):
            elt = pkt.getlayer(Dot11Elt)
            if elt is not None and elt.ID == 0:
                ssids.add(elt.info.decode(errors="replace"))
    return ssids


def beacon_intervals_ms(pcap_path, bssid):
    times = [float(p.time) for p in rdpcap(pcap_path)
             if p.haslayer(Dot11Beacon) and p[Dot11].addr3 == bssid]
    return [round((b - a) * 1000, 1) for a, b in zip(times, times[1:])]


def bssids_with_beacons(pcap_path):
    counts = Counter()
    for pkt in rdpcap(pcap_path):
        if pkt.haslayer(Dot11Beacon):
            counts[pkt[Dot11].addr3] += 1
    return counts
