# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 00:42:06 2023

@author: aadi
"""

import socket
import time
import cv2
from datetime import datetime

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = "localhost"
port = 8008
sock.connect((host, port))
print(f"Connected to {host}:{port}")

def send_image(image_path):
    
    global sock
    # Load the image
    img = cv2.imread(image_path)
    

    # Encode the image as JPEG before sending
    _, img_encoded = cv2.imencode(".bmp", img)

    # Convert the encoded image to bytes
    img_bytes = img_encoded.tobytes()
    
    
    # Get the length of the image data
    img_len = len(img_bytes)

    # Convert the image length to bytes
    img_len_bytes = img_len.to_bytes(8, 'little',signed=False)
    
    count = 0
    while True:
        before = datetime.now()
        # Send the image length over the socket to the server
        sock.sendall(img_len_bytes)
        # print("Image length sent to the server")
        
        # # Wait for a short delay (optional)
        # time.sleep(1)
    
        # Send the image data over the socket to the server
        sock.sendall(img_bytes)
        # print("Image sent to the server")
    
        
        #time.sleep(20)
        # recive response length
        response_len_bytes = sock.recv(8)
        response_len = int.from_bytes(response_len_bytes, 'little')
        
        # recive response
        response = sock.recv(response_len)
        response_msg = response.decode()
        
        print("Recieved response length: ", response_len)
        print("Recieved response: ", response_msg)
        after = datetime.now()
        
        duration = after - before
        print(int(duration.microseconds // 1000),"ms")
        count+=1
        print("count :",count)
        
        if (count==1):
            break
    
       
    
# Replace 'image_path' with the path to your image
image_path = 'C:/Users/AI/Aditya_project/test_images/Test2.jpg'
# image_path = "C:/Users/user/Downloads/test_image_3.jpg" # change back
send_image(image_path)


# Close the socket
sock.close()
