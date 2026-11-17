"""Live tests against the real internet. Run with: pytest -m live -v"""
import pytest
from src.dns_server import query
from src.tcp_tools import port_open, connect_samples, p95

pytestmark = pytest.mark.live
RESOLVERS = ["1.1.1.1", "8.8.8.8"]


@pytest.mark.parametrize("resolver", RESOLVERS)
def test_public_resolver_answers_github(resolver):
    reply = query("github.com", 53, address=resolver, timeout=3)
    assert reply.header.rcode == 0
    assert any(r.rtype == 1 for r in reply.rr)  # at least one A record


@pytest.mark.parametrize("resolver", RESOLVERS)
def test_public_resolver_nxdomain(resolver):
    reply = query("this-name-does-not-exist-12345.com", 53, address=resolver, timeout=3)
    assert reply.header.rcode == 3


@pytest.mark.parametrize("host,port", [("github.com", 443), ("1.1.1.1", 53), ("8.8.8.8", 53)])
def test_remote_port_reachable(host, port):
    assert port_open(host, port, timeout=3)


def test_connect_latency_to_github():
    latencies, failures = connect_samples("github.com", 443, samples=20, timeout=3)
    assert failures <= 1  # allow one transient timeout in 20 connects
    assert p95(latencies) < 500
