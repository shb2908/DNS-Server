import struct
from dataclasses import dataclass

@dataclass
class DNSHeader:
  """
  Basically this section is the starting part of dns packet. This sec is almost same for dns request and response.
  It have total length of 12 bytes. 
  RFC Name	              Descriptive Name	      Length	            Description
  -ID	                    Packet Identifier	      16 bits	            A random identifier is assigned to query packets. Response packets must reply with the same id. This is needed to differentiate responses due to the stateless nature of UDP.
  -QR	                    Query Response	        1 bit	              0 for queries, 1 for responses.
  -OPCODE	                Operation Code	        4 bits	            Typically always 0, see RFC1035 for details.
  -AA	                    Authoritative Answer	  1 bit	              Set to 1 if the responding server is authoritative - that is, it "owns" - the domain queried.
  -TC	                    Truncated Message	      1 bit	              Set to 1 if the message length exceeds 512 bytes. Traditionally a hint that the query can be reissued using TCP, for which the length limitation doesn't apply.
  -RD	                    Recursion Desired	      1 bit	              Set by the sender of the request if the server should attempt to resolve the query recursively if it does not have an answer readily available.
  -RA	                    Recursion Available	    1 bit	              Set by the server to indicate whether or not recursive queries are allowed.
  -Z	                    Reserved	              3 bits	            Originally reserved for later use, but now used for DNSSEC queries.
  -RCODE	                Response Code	          4 bits	            Set by the server to indicate the status of the response, i.e. whether or not it was successful or failed, and in the latter case providing details about the cause of the failure.
  -QDCOUNT	              Question Count	        16 bits	            The number of entries in the Question Section
  -ANCOUNT	              Answer Count	          16 bits	            The number of entries in the Answer Section
  -NSCOUNT	              Authority Count	        16 bits	            The number of entries in the Authority Section
  -ARCOUNT	              Additional Count	      16 bits	            The number of entries in the Additional Section
  """
  id_: int
  qr: int
  opcode: int
  aa: int
  tc: int
  rd: int
  ra: int
  z: int
  rcode: int
  qdcount: int
  ancount: int
  nscount: int
  arcount: int
  def pack(self) -> bytes:
    flags = (
      (self.qr << 15)
      | (self.opcode << 11)
      | (self.aa << 10)
      | (self.tc << 9)
      | (self.rd << 8)
      | (self.ra << 7)
      | (self.z << 4)
      | self.rcode
    )
    return struct.pack(
      ">HHHHHH",
      self.id_,
      flags,
      self.qdcount,
      self.ancount,
      self.nscount,
      self.arcount,
    )
  
  @classmethod
  def unpack(cls, data: bytes):
    id_, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", data)
    qr = flags >> 15
    opcode = (flags >> 11) & 0b1111
    aa = (flags >> 10) & 0b1
    tc = (flags >> 9) & 0b1
    rd = (flags >> 8) & 0b1
    ra = (flags >> 7) & 0b1
    z = (flags >> 4) & 0b111
    rcode = flags & 0b1111
    return cls(
      id_,
      qr,
      opcode,
      aa,
      tc,
      rd,
      ra,
      z,
      rcode,
      qdcount,
      ancount,
      nscount,
      arcount,
    )