"""Measure real TCP connect latency and DNS lookup time. Writes results/latency.csv and results/latency.png"""
import csv
import statistics
import sys
import time
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.tcp_tools import connect_latencies_ms
from src.dns_server import query

TCP_TARGETS = [("github.com", 443), ("1.1.1.1", 53), ("8.8.8.8", 53)]
DNS_RESOLVERS = ["1.1.1.1", "8.8.8.8"]
N = 30


def dns_times_ms(resolver):
    out = []
    for _ in range(N):
        t = time.perf_counter()
        query("github.com", 53, address=resolver, timeout=3)
        out.append((time.perf_counter() - t) * 1000)
    return out


def row(name, vals):
    q = statistics.quantiles(vals, n=20)
    return [name, round(min(vals), 1), round(statistics.median(vals), 1), round(q[-1], 1), round(max(vals), 1)]


rows = []
for host, port in TCP_TARGETS:
    try:
        rows.append(row(f"TCP connect {host}:{port}", connect_latencies_ms(host, port, N)))
    except OSError as e:
        print(f"skipped {host}:{port}: {e}")
for r in DNS_RESOLVERS:
    try:
        rows.append(row(f"DNS lookup via {r}", dns_times_ms(r)))
    except OSError as e:
        print(f"skipped DNS {r}: {e}")

with open("results/latency.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["test", "min_ms", "median_ms", "p95_ms", "max_ms"])
    w.writerows(rows)

for r in rows:
    print(f"{r[0]:32} min {r[1]:7} median {r[2]:7} p95 {r[3]:7} max {r[4]:7} (ms)")

fig, ax = plt.subplots(figsize=(8, 4))
ax.barh([r[0] for r in rows], [r[2] for r in rows], xerr=[[0] * len(rows), [r[3] - r[2] for r in rows]], capsize=3)
ax.set_xlabel("milliseconds (bar = median, whisker = p95)")
ax.set_title(f"Measured on my machine, {N} samples each")
plt.tight_layout()
plt.savefig("results/latency.png", dpi=150)
