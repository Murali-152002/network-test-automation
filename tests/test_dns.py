from src.dns_server import query


def test_known_name_resolves(dns):
    reply = query("app.test", dns)
    assert [str(r.rdata) for r in reply.rr] == ["10.0.0.10"]


def test_ttl_matches_record(dns):
    assert query("db.test", dns).rr[0].ttl == 60


def test_unknown_name_returns_nxdomain(dns):
    reply = query("missing.test", dns)
    assert reply.header.rcode == 3  # NXDOMAIN
    assert not reply.rr


def test_lookup_is_case_insensitive(dns):
    assert query("APP.TEST", dns).rr
