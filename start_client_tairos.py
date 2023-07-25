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

def send_image(image_path):
    
    global sock
    # Load the image
    img = cv2.imread(image_path)
    

    # Encode the image as JPEG before sending
    _, img_encoded = cv2.imencode(".jpg", img)

    # Convert the encoded image to bytes
    img_bytes = img_encoded.tobytes()

    # Send the image data over the socket to the server
    sock.sendall(img_bytes)
    print("Image sent to the server")

    #Test Start
    #time.sleep(20)
    response = sock.recv(4096)
    response_msg = pickle.loads(response)
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
