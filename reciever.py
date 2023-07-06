# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 21:14:51 2023

@author: user
"""

import pickle
import socket

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
receiver_address = ('localhost', 1234)
sock.bind(receiver_address)

# Listen for incoming connections
sock.listen(1)

# Accept a connection
connection, client_address = sock.accept()

# Receive the data
received_data = b""
while True:
    data = connection.recv(4096)
    if not data:
        break
    received_data += data

# Deserialize the data
deserialized_data = pickle.loads(received_data)

# Print the received list
print(deserialized_data, "\n")

# Close the connection and socket
connection.close()
sock.close()
