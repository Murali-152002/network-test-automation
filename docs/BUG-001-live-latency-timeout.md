# Bug report BUG-001

**Title:** Live latency test aborts on a single connect timeout
**Date:** 2026-11-17
**Area:** Latency
**Test case ID:** LIVE-4

## Steps to reproduce
1. Run `pytest -v` on a normal home Wi-Fi connection.
2. LIVE-4 makes 20 TCP connects to github.com:443 with a 1 second timeout.

## Expected result
The test judges the 20 samples (p95 under 500 ms) and tolerates an occasional slow or dropped connect, as real networks do.

## Actual result
One connect timed out after 1 second. `connect_latencies_ms` raised `TimeoutError`, so the whole test failed with 22 passed and 1 failed. The other 19 samples were never evaluated.

## Evidence
`TimeoutError: timed out` at `src/tcp_tools.py` line 54 (`socket.create_connection`). All 7 other live tests passed in the same run.

## Severity
Minor: a flaky test, not a product defect.

## Root cause
The helper treated any failed connect as a fatal error instead of a data point.

## Fix
Added `connect_samples()`, which counts failed connects and returns them with the latencies. LIVE-4 now allows at most 1 failure in 20 connects, uses a 3 second timeout, and checks p95 under 500 ms on the successful samples.

## Status
Fixed. Retest passed on 2026-11-17: 23 passed, 0 failed.
