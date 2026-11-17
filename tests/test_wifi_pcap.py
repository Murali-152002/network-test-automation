import pytest
from scapy.all import wrpcap, RadioTap
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeReq
from src.wifi_analysis import frame_counts, beacon_ssids, beacon_intervals_ms

BSSID = "aa:bb:cc:00:00:01"


def beacon(ssid, t):
    pkt = (RadioTap() / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff",
                              addr2=BSSID, addr3=BSSID)
           / Dot11Beacon(beacon_interval=100) / Dot11Elt(ID=0, info=ssid))
    pkt.time = t
    return pkt


def probe(t):
    pkt = (RadioTap() / Dot11(type=0, subtype=4, addr1="ff:ff:ff:ff:ff:ff",
                              addr2="11:22:33:44:55:66", addr3="ff:ff:ff:ff:ff:ff")
           / Dot11ProbeReq() / Dot11Elt(ID=0, info=b""))
    pkt.time = t
    return pkt


@pytest.fixture()
def capture(tmp_path):
    path = tmp_path / "sample.pcap"
    frames = [beacon(b"lab-ap", 1000.0), probe(1000.05),
              beacon(b"lab-ap", 1000.1024), beacon(b"lab-ap", 1000.2048)]
    wrpcap(str(path), frames)
    return str(path)


def test_frame_counts(capture):
    counts = frame_counts(capture)
    assert counts["beacon"] == 3
    assert counts["probe_request"] == 1


def test_ssid_extracted(capture):
    assert beacon_ssids(capture) == {"lab-ap"}


def test_beacon_interval_close_to_102ms(capture):
    intervals = beacon_intervals_ms(capture, BSSID)
    assert len(intervals) == 2
    assert all(abs(i - 102.4) < 5 for i in intervals)
