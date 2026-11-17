from src.tcp_tools import port_open, echo_roundtrip, free_port


def test_open_port_detected(echo):
    assert port_open("127.0.0.1", echo.port)


def test_closed_port_detected():
    assert not port_open("127.0.0.1", free_port())


def test_echo_returns_same_bytes(echo):
    assert echo_roundtrip("127.0.0.1", echo.port, b"hello") == b"hello"


def test_echo_handles_binary_payload(echo):
    payload = bytes(range(256))
    assert echo_roundtrip("127.0.0.1", echo.port, payload) == payload
