# a DNS Answer is part of the DNS response, which provides the requested information regarding a domain name. 
# This "answer" section contains Resource Records (RRs) that give details about the domain queried.

# import struct
# from dataclasses import dataclass

# @dataclass
# class DNSAnswer:
#     """
#     Represents a DNS Answer Section.
#     """
#     name: str       # Domain name in the answer
#     type_: int      # Record type (e.g., 1 for "A")
#     class_: int     # Record class (e.g., 1 for "IN")
#     ttl: int        # Time-to-live value
#     rdata: str      # IPv4 address as a string (e.g., "192.168.1.1")

#     def pack(self) -> bytes:
#         """Pack the DNS answer into binary format."""
#         # Encode the name as a sequence of labels
#         parts = self.name.split(".")
#         name = b"".join(len(p).to_bytes(1, "big") + p.encode("ascii") for p in parts)
#         name += b"\x00"  # Null-terminated

#         # Convert the IPv4 address into binary format
#         try:
#             rdata = struct.pack("!BBBB", *[int(part) for part in self.rdata.split(".")])
#         except ValueError as e:
#             raise ValueError(f"Invalid IPv4 address: {self.rdata}") from e

#         # RDLENGTH is always 4 for an "A" record
#         rdlength = 4

#         # Pack all the fields together
#         return (
#             name
#             + struct.pack("!HHIH", self.type_, self.class_, self.ttl, rdlength)
#             + rdata
#         )

#123

import struct
from dataclasses import dataclass

@dataclass
class DNSAnswer:
    """
    Represents a DNS Answer Section.
    """
    name: str       # Domain name in the answer
    type_: int      # Record type (e.g., 1 for "A")
    class_: int     # Record class (e.g., 1 for "IN")
    ttl: int        # Time-to-live value
    rdata: str      # IPv4 address as a string (e.g., "192.168.1.1")

    def pack(self) -> bytes:
        """Pack the DNS answer into binary format."""
        # Encode the name as a sequence of labels
        parts = self.name.split(".")
        name = b"".join(len(p).to_bytes(1, "big") + p.encode("ascii") for p in parts)
        name += b"\x00"  # Null-terminated

        # Convert the IPv4 address into binary format
        try:
            rdata = struct.pack("!BBBB", *[int(part) for part in self.rdata.split(".")])
        except ValueError as e:
            raise ValueError(f"Invalid IPv4 address: {self.rdata}") from e

        # RDLENGTH is always 4 for an "A" record
        rdlength = 4

        # Pack all the fields together
        return (
            name
            + struct.pack("!HHIH", self.type_, self.class_, self.ttl, rdlength)
            + rdata
        )

    @classmethod
    def unpack(cls, data, offset):
        """
        Unpacks a DNS Answer Section from the given data at the specified offset.
        """
        # Unpack the name (domain name)
        name, offset = cls.parse_name(data, offset)

        # Unpack the rest of the fields (type, class, ttl, rdlength)
        type_, class_, ttl, rdlength = struct.unpack("!HHIH", data[offset:offset+10])
        offset += 10

        # Unpack the resource data (IPv4 address)
        rdata = data[offset:offset+rdlength]
        ip_address = ".".join(str(byte) for byte in rdata)  # Convert to human-readable IP
        offset += rdlength

        return cls(name, type_, class_, ttl, ip_address), offset

    @staticmethod
    def parse_name(data, offset):
        """
        Unpacks the domain name from the DNS response, supporting domain name compression.
        """
        labels = []
        while True:
            length = data[offset]
            offset += 1
            if length == 0:
                break
            labels.append(data[offset:offset+length].decode("utf-8"))
            offset += length
        return ".".join(labels), offset
