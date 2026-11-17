"""Tests on a real 802.11 capture. Skipped until captures/real_beacons.pcap exists."""
import os
import statistics
import pytest
from src.wifi_analysis import frame_counts, beacon_ssids, bssids_with_beacons, beacon_intervals_ms

PCAP = os.path.join(os.path.dirname(__file__), "..", "captures", "real_beacons.pcap")
pytestmark = pytest.mark.skipif(not os.path.exists(PCAP), reason="no real capture yet")


def test_capture_contains_beacons():
    assert frame_counts(PCAP)["beacon"] > 0


def test_capture_has_an_ssid():
    assert len(beacon_ssids(PCAP)) >= 1


def test_beacon_interval_is_typical():
    bssid, n = bssids_with_beacons(PCAP).most_common(1)[0]
    assert n >= 3
    median = statistics.median(beacon_intervals_ms(PCAP, bssid))
    assert 80 <= median <= 130  # APs normally send a beacon about every 102.4 ms
