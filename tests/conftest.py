import pytest
from src import dns_server
from src.tcp_tools import EchoServer


@pytest.fixture(scope="module")
def dns():
    server = dns_server.start()
    yield server.server.server_address[1]
    server.stop()


@pytest.fixture()
def echo():
    server = EchoServer()
    yield server
    server.close()
