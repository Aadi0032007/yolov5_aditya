# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 00:42:06 2023

@author: aadi
"""

import socket
import time
import cv2
import pickle
from datetime import datetime

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = "localhost"
port = 1234
sock.connect((host, port))
print(f"Connected to {host}:{port}")

def flatten_list(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(str(item))
    return flattened

def send_image(image_path):
    
    global sock
    # Load the image
    img = cv2.imread(image_path)
    

    # Encode the image as JPEG before sending
    _, img_encoded = cv2.imencode(".jpg", img)

    # Convert the encoded image to bytes
    img_bytes = img_encoded.tobytes()
    
    
    # Get the length of the image data
    img_len = len(img_bytes)

    # Convert the image length to bytes
    img_len_bytes = img_len.to_bytes(4, 'big')

    # Send the image length over the socket to the server
    sock.sendall(img_len_bytes)
    print("Image length sent to the server")
    
    # Wait for a short delay (optional)
    time.sleep(1)

    # Send the image data over the socket to the server
    sock.sendall(img_bytes)
    print("Image sent to the server")

    #Test Start
    #time.sleep(20)
    response = sock.recv(4096)
    response_lst = pickle.loads(response)
    # Flatten the list and remove brackets
    response_msg = ', '.join(flatten_list(response_lst))
    
    print("Recieved response: ", response_msg)
    #Test Ends
       
    
# Replace 'image_path' with the path to your image
image_path = 'C:/Users/AI/Aditya_project/test_images/Test.jpg'
before = datetime.now()
send_image(image_path)
after = datetime.now()
duration = after - before
print(int(duration.microseconds // 1000),"ms")

# Close the socket
sock.close()
