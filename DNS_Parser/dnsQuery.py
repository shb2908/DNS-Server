import struct
from dataclasses import dataclass
from DNS_Parser.dnsHeader import DNSHeader
from DNS_Parser.dnsQuestion import DNSQuestion

@dataclass
class DNSQuery:
  header: DNSHeader
  questions: list[DNSQuestion]
  @classmethod
  def parse(cls, payload : bytes):  
    header = DNSHeader.unpack(payload[:12])
    questions: list[DNSQuestion] = []
    unprocessed = payload[12:]
    for _ in range(header.qdcount):
      question, unprocessed = DNSQuestion.unpack(unprocessed, payload)
      questions.append(question)
    return cls(header, questions)