"""Small local DNS server used as the system under test."""
import threading
from dnslib import DNSRecord, RR, QTYPE, RCODE, A
from dnslib.server import DNSServer, BaseResolver

RECORDS = {
    "app.test.": ("10.0.0.10", 300),
    "db.test.": ("10.0.0.20", 60),
}


class StaticResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        name = str(request.q.qname).lower()
        if request.q.qtype == QTYPE.A and name in RECORDS:
            ip, ttl = RECORDS[name]
            reply.add_answer(RR(name, QTYPE.A, rdata=A(ip), ttl=ttl))
        else:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply


def start(port=0, address="127.0.0.1"):
    server = DNSServer(StaticResolver(), port=port, address=address)
    server.start_thread()
    return server


def query(name, port, address="127.0.0.1", timeout=2):
    data = DNSRecord.question(name).send(address, port, timeout=timeout)
    return DNSRecord.parse(data)
