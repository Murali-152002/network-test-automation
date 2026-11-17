"""Print a summary of a capture. Usage: python scripts/analyze_capture.py captures/raw.pcap"""
import sys
sys.path.insert(0, ".")
from src.wifi_analysis import frame_counts, beacon_ssids, bssids_with_beacons

path = sys.argv[1]
print("Frame counts:", dict(frame_counts(path)))
print("SSIDs seen in beacons:", sorted(beacon_ssids(path)))
print("Beacons per access point (BSSID):")
for bssid, n in bssids_with_beacons(path).most_common(10):
    print(f"  {bssid}  {n}")
