# Test Plan: network-test-automation

## Scope
Functional and basic performance tests for three small network components, all run locally:
1. A DNS server (`src/dns_server.py`) that answers A records from a static table.
2. TCP behavior: port open/closed detection, echo round trip, connect latency (`src/tcp_tools.py`).
3. 802.11 analysis (`src/wifi_analysis.py`) on a pcap of beacon and probe-request frames generated in the test.

Out of scope: real radio captures, throughput testing, security testing.

## Test cases
| ID | Area | What is checked | Expected result |
|----|------|-----------------|-----------------|
| DNS-1 | DNS | Query a known name | A record 10.0.0.10 returned |
| DNS-2 | DNS | TTL of `db.test` | 60 seconds |
| DNS-3 | DNS | Query an unknown name | NXDOMAIN, no answer records |
| DNS-4 | DNS | Query in upper case | Same answer as lower case |
| TCP-1 | TCP | Port with a listener | Reported open |
| TCP-2 | TCP | Port with no listener | Reported closed |
| TCP-3 | TCP | Send text, read reply | Same bytes returned |
| TCP-4 | TCP | Send all 256 byte values | Same bytes returned |
| LAT-1 | Latency | 20 connects to local server | p95 under 200 ms |
| WIFI-1 | 802.11 | Count frame types | 3 beacons, 1 probe request |
| WIFI-2 | 802.11 | Read SSID from beacons | `lab-ap` |
| WIFI-3 | 802.11 | Beacon spacing | About 102.4 ms between beacons |

## Entry and exit criteria
Entry: dependencies installed (`pip install -r requirements.txt`).
Exit: all tests pass in CI on every push; any failure gets a bug report (see `BUG_REPORT_TEMPLATE.md`).

## Environment
Python 3.11, pytest, dnslib, scapy. GitHub Actions on ubuntu-latest.

## Live and real-capture tests
| ID | Area | What is checked | Expected result |
|----|------|-----------------|-----------------|
| LIVE-1 | DNS | github.com via 1.1.1.1 and 8.8.8.8 | NOERROR with an A record |
| LIVE-2 | DNS | Nonexistent name via both resolvers | NXDOMAIN |
| LIVE-3 | TCP | Connect to github.com:443, 1.1.1.1:53, 8.8.8.8:53 | Port open |
| LIVE-4 | Latency | 20 connects to github.com:443 | p95 under 500 ms |
| REAL-1 | 802.11 | Real capture of my own network | At least one beacon and one SSID |
| REAL-2 | 802.11 | Beacon spacing in the real capture | Median 80-130 ms (APs normally send about every 102.4 ms) |

Live tests run on my machine with `pytest -m live`; CI runs `pytest -m "not live"`.
