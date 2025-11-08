#!/usr/bin/env python3
# import socket

# from Server.clientHandler import ClientHandler

# # Global variables
# IP = "127.0.0.1"
# PORT = 53


# def main():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((IP, PORT))
#     print("DNS Listening on {0}:{1} ...".format(IP, PORT))
#     while True:
#         data, address = sock.recvfrom(650)
#         client = ClientHandler(address, data, sock)
#         client.run()


# if __name_ == "__main__":
#     main()

import socket
import logging
import sys
from Server.clientHandler import ClientHandler  # Ensure this import matches your project structure

# Global variables
IP = "127.0.0.1"
PORT = 8053  # Changed to a non-privileged port for local testing

# Setting up logging
logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Bind to IP and port
        sock.bind((IP, PORT))
        logging.info(f"DNS Listening on {IP}:{PORT} ...")

        while True:
            # Receive data from client
            data, address = sock.recvfrom(650)
            logging.info(f"Received data from {address}")

            # Create a new ClientHandler thread for each request
            client = ClientHandler(address, data, sock)
            client.run()

    except PermissionError:
        logging.error(f"Permission denied: You do not have permission to bind to port {PORT}. Try using a port > 1024 or run as admin/root.")
        sys.exit(1)
    except socket.error as e:
        logging.error(f"Socket error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
