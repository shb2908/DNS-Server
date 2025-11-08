import threading

from DNS_Parser.dnsQuery import DNSQuery
from DNS_Parser.dnsResponse import DNSResponse

class ClientHandler(threading.Thread):
    """
    Class to handle multiple client DNS requests
    """

    def __init__(self, address, data, sock):
        threading.Thread.__init__(self)
        self.client_address = address
        self.dnsQuery = DNSQuery.parse(data)
        self.sock = sock

    def run(self):
        resp = DNSResponse.build_from(self.dnsQuery)
        self.sock.sendto(resp, self.client_address)
        print("Request from {0} for {1}".format(self.client_address, self.dnsQuery.questions[0].name))