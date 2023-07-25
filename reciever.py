# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 21:14:51 2023

@author: user
"""

import socket
import pickle

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set a timeout for the socket
sock.settimeout(30)  # Set the timeout value in seconds

# Bind the socket to a specific address and port
server_address = ('localhost', 1234)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print('Server is listening on', server_address)

def flatten_list(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(str(item))
    return flattened

try:
    # Accept a connection
    connection = None
    client_address = None
    try:
        connection, client_address = sock.accept()
        print('Connected by', client_address)
    except socket.timeout:
        print('Timeout: No connection received.')

    if connection is not None:
        # Receive the data from the client
        received_data = b""
        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    print('Connection closed by the client.')
                    break
                received_data += data
                # Deserialize the received data
                received_list = pickle.loads(received_data)
                # Flatten the list and remove brackets
                response_msg = ', '.join(flatten_list(received_list))
                print('Received list:', response_msg)
            except socket.timeout:
                print('Timeout: No data received.')
                break

        

finally:
    if connection is not None:
        # Close the connection
        connection.close()
    # Close the socket
    sock.close()
