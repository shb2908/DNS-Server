# import socket

# HOST = 'localhost'
# PORT = 9999
# PKT_SIZE = 8
# c = socket.socket()
# c.connect((HOST, PORT))

# import socket

# HOST = '127.0.0.1'  # Server address (localhost)
# PORT = 8053         # Server port (same as in the server)
# PKT_SIZE = 8        # Packet size for communication

# def main():
#     try:
#         # Create a socket and connect to the server
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#             client_socket.connect((HOST, PORT))
#             print(f"Connected to {HOST}:{PORT}")

#             while True:
#                 # Prompt user for input
#                 message = input("Enter message to send to the server (or 'exit' to quit): ")
                
#                 if message.lower() == 'exit':
#                     print("Closing connection.")
#                     break
                
#                 # Ensure the message fits the PKT_SIZE
#                 if len(message) > PKT_SIZE:
#                     print(f"Message too long. Please limit to {PKT_SIZE} characters.")
#                     continue
                
#                 # Send the message
#                 padded_message = message.ljust(PKT_SIZE)  # Pad the message to PKT_SIZE
#                 client_socket.sendall(padded_message.encode('utf-8'))
#                 print(f"Sent: {message}")
                
#                 # Receive and display the server's response
#                 response = client_socket.recv(PKT_SIZE).decode('utf-8').strip()
#                 print(f"Server response: {response}")

#     except ConnectionRefusedError:
#         print(f"Unable to connect to {HOST}:{PORT}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

# import socket

# HOST = '127.0.0.1'  # Server address
# PORT = 8053          # Server port
# PKT_SIZE = 8         # Packet size for communication

# def main():
#     try:
#         # Create a UDP socket
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
#             # No need to connect for UDP; you send directly to the server
#             print(f"Sending to {HOST}:{PORT}")
            
#             while True:
#                 # Prompt user for input
#                 message = input("Enter message to send to the server (or 'exit' to quit): ")
                
#                 if message.lower() == 'exit':
#                     print("Closing connection.")
#                     break
                
#                 # Ensure the message fits the PKT_SIZE
#                 if len(message) > PKT_SIZE:
#                     print(f"Message too long. Please limit to {PKT_SIZE} characters.")
#                     continue
                
#                 # Send the message to the server
#                 padded_message = message.ljust(PKT_SIZE)  # Pad the message to PKT_SIZE
#                 client_socket.sendto(padded_message.encode('utf-8'), (HOST, PORT))
#                 print(f"Sent: {message}")
                
#                 # Receive and display the server's response
#                 response, server_address = client_socket.recvfrom(PKT_SIZE)
#                 print(f"Server response: {response.decode('utf-8').strip()}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

# import socket

# HOST = '127.0.0.1'  # Server address
# PORT = 8053          # Server port

# def main():
#     try:
#         # Create a UDP socket
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
#             # No need to connect for UDP; you send directly to the server
#             print(f"Sending to {HOST}:{PORT}")
            
#             while True:
#                 # Prompt user for input
#                 message = input("Enter message to send to the server (or 'exit' to quit): ")
                
#                 if message.lower() == 'exit':
#                     print("Closing connection.")
#                     break
                
#                 # Send the message to the server (no size limitation)
#                 client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
#                 print(f"Sent: {message}")
                
#                 # Receive and display the server's response
#                 # Set a larger buffer size for receiving the response
#                 response, server_address = client_socket.recvfrom(1024)  # Adjust buffer size as needed
#                 print(f"Server response: {response.decode('utf-8').strip()}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()
# 12345
# import socket
# import struct

# # DNS query constants
# DNS_HEADER_FORMAT = '!HHHHHH'  # 6 unsigned short integers (12 bytes)
# DNS_QUERY_TYPE = 1  # A record (IPv4 address)
# DNS_QUERY_CLASS = 1  # IN (Internet)

# # DNS Server details
# HOST = '127.0.0.1'  # Server address
# PORT = 8053          # Server port

# def create_dns_query(domain):
#     """Creates a DNS query message for the given domain."""
    
#     # DNS Header (12 bytes)
#     transaction_id = 1234  # Arbitrary transaction ID
#     flags = 0x0100         # Standard query
#     questions = 1          # Number of questions
#     answer_rr = 0          # No answers
#     authority_rr = 0       # No authority
#     additional_rr = 0      # No additional records
    
#     # Pack the DNS header
#     header = struct.pack(DNS_HEADER_FORMAT, transaction_id, flags, questions, answer_rr, authority_rr, additional_rr)
    
#     # Convert the domain into DNS query format
#     labels = domain.split('.')
#     query = b''
#     for label in labels:
#         query += struct.pack('!B', len(label)) + label.encode('utf-8')
#     query += b'\0'  # Null byte to end the domain part
    
#     # Add query type and class (A record, IN class)
#     query += struct.pack('!HH', DNS_QUERY_TYPE, DNS_QUERY_CLASS)
    
#     return header + query

# def main():
#     try:
#         # Create a UDP socket
#         with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
#             print(f"Sending to {HOST}:{PORT}")
            
#             # Create a DNS query for 'google.com'
#             domain = "google.com"
#             dns_query = create_dns_query(domain)
            
#             # Send the DNS query
#             client_socket.sendto(dns_query, (HOST, PORT))
#             print(f"Sent DNS query for domain: {domain}")
            
#             # Receive and display the server's response
#             response, server_address = client_socket.recvfrom(1024)  # Adjust buffer size as needed
#             print(f"Server response: {response}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

import socket
import struct
from DNS_Parser.dns_answer import DNSAnswer  # Import the DNSAnswer class from the DNS_Parser directory

def create_dns_query(domain):
    """Creates a DNS query message for the given domain."""
    
    # DNS Header (12 bytes)
    transaction_id = 1234  # Arbitrary transaction ID
    flags = 0x0100         # Standard query
    questions = 1          # Number of questions
    answer_rr = 0          # No answers
    authority_rr = 0       # No authority
    additional_rr = 0      # No additional records
    
    # Pack the DNS header
    header = struct.pack('!HHHHHH', transaction_id, flags, questions, answer_rr, authority_rr, additional_rr)
    
    # Convert the domain into DNS query format
    labels = domain.split('.')
    query = b''
    for label in labels:
        query += struct.pack('!B', len(label)) + label.encode('utf-8')
    query += b'\0'  # Null byte to end the domain part
    
    # Add query type and class (A record, IN class)
    query += struct.pack('!HH', 1, 1)  # Type = 1 (A record), Class = 1 (IN)
    
    return header + query


def parse_dns_response(response_data):
    offset = 12  # Skip the DNS header (12 bytes)
    answers = []

    # Parse the number of answers (from the header)
    num_answers = struct.unpack("!H", response_data[6:8])[0]
    for _ in range(num_answers):
        answer, offset = DNSAnswer.unpack(response_data, offset)
        answers.append(answer)

    return answers


def main():
    try:
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            HOST = '127.0.0.1'  # Server address
            PORT = 8053  # Server port

            print(f"Sending to {HOST}:{PORT}")

            # Create a DNS query for 'google.com'
            domain = "google.com"
            dns_query = create_dns_query(domain)

            # Send the DNS query
            client_socket.sendto(dns_query, (HOST, PORT))
            print(f"Sent DNS query for domain: {domain}")
            
            # Receive and display the server's response
            response, server_address = client_socket.recvfrom(1024)  # Adjust buffer size as needed
            print(f"Server response: {response}")

            # Parse the DNS response
            answers = parse_dns_response(response)
            for answer in answers:
                print(f"Resolved IP Address: {answer.rdata}")
                
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
