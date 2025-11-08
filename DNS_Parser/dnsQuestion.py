import struct
from dataclasses import dataclass

@dataclass
class DNSQuestion:
  """
  This Section of dns contains question details.
  The question section contains a list of questions (usually just 1) that the sender wants to ask the receiver. This section is present in both query and reply packets.

  Each question has the following structure:

  Name: A domain name, represented as a sequence of "labels"
  Type: 2-byte int; the type of record (1 for an A record, 5 for a CNAME record etc., full list here)
  Class: 2-byte int; usually set to 1
  """
  name: str
  type_: int
  class_: int
  def pack(self):
    name = (
      b"".join(
        len(p).to_bytes(1, "big") + p.encode("ascii")
        for p in self.name.split(".")
      )
      + b"\x00"
    )
    return name + struct.pack("!HH", self.type_, self.class_)
  
  @classmethod
  def unpack(cls, data: bytes, payload: bytes):
    parts = []
    while True:
      length = data[0]
      if length == 0:
        data = data[1:]
        break
      elif (length & 0b11000000 == 0b11000000):  # Check if the first two bits are set
        pointer = struct.unpack("!H", data[:2])[0]
        pointer &= 0b0011111111111111  # Clear the first two bits
        data = data[2:]
        name = cls.unpack(payload[pointer:], payload)[0].name
        parts.append(name)
        return cls(".".join(parts), *struct.unpack("!HH", data[:4])), data[4:]
      else:
        parts.append(data[1 : length + 1].decode("ascii"))
        data = data[length + 1 :]
    name = ".".join(parts)
    type_, class_ = struct.unpack("!HH", data[:4])
    data = data[4:]
    return cls(name, type_, class_), data
