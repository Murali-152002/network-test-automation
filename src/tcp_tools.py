"""TCP helpers: a local echo server and port/latency checks."""
import socket
import statistics
import threading
import time


class EchoServer:
    def __init__(self, host="127.0.0.1"):
        self.sock = socket.socket()
        self.sock.bind((host, 0))
        self.sock.listen(5)
        self.port = self.sock.getsockname()[1]
        self._stop = False
        self._t = threading.Thread(target=self._run, daemon=True)
        self._t.start()

    def _run(self):
        self.sock.settimeout(0.2)
        while not self._stop:
            try:
                conn, _ = self.sock.accept()
            except (socket.timeout, OSError):
                continue
            with conn:
                data = conn.recv(1024)
                if data:
                    conn.sendall(data)

    def close(self):
        self._stop = True
        self._t.join(timeout=1)
        self.sock.close()


def port_open(host, port, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def echo_roundtrip(host, port, payload=b"ping"):
    with socket.create_connection((host, port), timeout=1) as s:
        s.sendall(payload)
        return s.recv(1024)


def connect_latencies_ms(host, port, samples=20):
    out = []
    for _ in range(samples):
        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=1):
            pass
        out.append((time.perf_counter() - start) * 1000)
    return out


def connect_samples(host, port, samples=20, timeout=3):
    """Like connect_latencies_ms, but a failed connect is counted, not raised."""
    latencies, failures = [], 0
    for _ in range(samples):
        start = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                pass
        except OSError:
            failures += 1
            continue
        latencies.append((time.perf_counter() - start) * 1000)
    return latencies, failures


def p95(values):
    return statistics.quantiles(values, n=20)[-1]


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port
