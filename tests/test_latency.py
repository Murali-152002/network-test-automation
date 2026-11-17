from src.tcp_tools import connect_latencies_ms, p95


def test_connect_latency_p95_under_200ms_locally(echo):
    samples = connect_latencies_ms("127.0.0.1", echo.port, samples=20)
    assert len(samples) == 20
    assert p95(samples) < 200
