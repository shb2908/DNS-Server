from DNS_Parser.dnsQuery import DNSQuery
from DNS_Parser.dnsHeader import DNSHeader
from DNS_Parser.dnsQuestion import DNSQuestion
from DNS_Parser.dnsAnswer import DNSAnswer
import Zone_Handler.zoneHandler as zoneHandler

class DNSResponse:
  
  @classmethod
  def get_records(cls,question:DNSQuestion):
    domain = question.name
    question_type = question.type_
    num_bytes = (int.bit_length(question_type) + 7) // 8

    if question_type is None and len(domain) == 0:
      return {}
    qt = ""
    try:
      qt = zoneHandler.QUESTION_TYPES[int.to_bytes(num_bytes, byteorder='big')]
    except KeyError:
      qt = "a"
    zone = zoneHandler.get_zone(domain)
    if zone is None:
      return []  # empty list ensure a domain we don't have returns correct data
    return zone[qt]
  
  @staticmethod
  def build_from(query: DNSQuery):
    response = b""
    ancount=0;
    answer  = b""
    for question in query.questions:
      record = DNSResponse.get_records(question)
      ancount+=len(record)
      #print(record)
      for r in record:
        answer += DNSAnswer(
          name=question.name,
          type_=question.type_,
          class_=question.class_,
          ttl=r["ttl"],
          rdlength=4,
          rdata=r["value"],
        ).pack()

    

    response += DNSHeader(
      id_=query.header.id_,
      qr=1,
      opcode=query.header.opcode,
      aa=0,
      tc=0,
      rd=query.header.rd,
      ra=0,
      z=0,
      rcode=(0 if query.header.opcode == 0 else 4),
      qdcount=query.header.qdcount,
      ancount=ancount,
      nscount=0,
      arcount=0,
    ).pack()
        
    for question in query.questions:
      response += question.pack()
    
    return response+answer