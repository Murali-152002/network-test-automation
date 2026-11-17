"""Keep only beacons from your own network, so nobody else's data goes on GitHub.
Usage: python scripts/filter_capture.py captures/raw.pcap "YourWifiName" """
import sys
from scapy.all import rdpcap, wrpcap
from scapy.layers.dot11 import Dot11Beacon, Dot11Elt

src, ssid = sys.argv[1], sys.argv[2].encode()
keep = []
for pkt in rdpcap(src):
    if pkt.haslayer(Dot11Beacon):
        elt = pkt.getlayer(Dot11Elt)
        if elt is not None and elt.ID == 0 and elt.info == ssid:
            keep.append(pkt)
wrpcap("captures/real_beacons.pcap", keep)
print(f"Kept {len(keep)} beacons for '{sys.argv[2]}' -> captures/real_beacons.pcap")
