# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 00:40:29 2023

@author: user
"""

import socket
import cv2
import numpy as np
import os
import sys
import tempfile
import time
import pickle

# Add YOLOv5 folder to the sys.path
yolov5_path = "C:/Users/AI/Aditya_project/yolov5_aditya"  
sys.path.append(yolov5_path)

# Import the run function
from detect import run
 # Provide the required arguments for the run function
weights = os.path.join(yolov5_path, 'yolov5x_bottle.pt')  # Replace with the path to your model weights
iou_thres = 0.55
augment = True

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = "localhost"
port = 1234
sock.bind((host, port))

# Listen for incoming connections
sock.listen(1)
print(f"Listening on {host}:{port}")

while True:
    # Wait for a connection
    conn, addr = sock.accept()
    print(f"Connection established from {addr}")

    try:
        while True:
            # Receive the image data
            image_data = b""
            while True:
                data = conn.recv(4096)
                if len(data) < 4096:
                    break
                image_data += data

            # If no more data is received, the connection is closed
            if not image_data:
                print("Connection closed by client.")
                break
            
            print ("Recieved data size: ", len(image_data))

            # Convert the image data to a NumPy array
            nparr = np.frombuffer(image_data, dtype=np.uint8)

            # Decode the NumPy array to an OpenCV image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Save the cv2 image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_img:
                temp_image_path = tmp_img.name
                cv2.imwrite(temp_image_path, img)
            
            print("Running detection..")
            # Call the run function
            output = run(weights=weights, source=temp_image_path, iou_thres=iou_thres,augment=augment)
            
            # Remove the temporary image file
            os.remove(temp_image_path)
            
            # Process the image data (e.g., save to a file, display, etc.)
            # Here, we simply show the image
            # cv2.imshow("Received Image", img)
                       
            print("Image opened in new window by name Recieved Image")
            
            response = pickle.dumps(output)
            
            #Test Start
            print('Sending Response')
            # response = 'Add Yolo Output Here'
            conn.send(response)
            print('sent response')
            #Test End
            
            # # Wait for a key press
            # key = cv2.waitKey(0)

            # # If the key is the escape key (ASCII value 27), close the window
            # if key == 27:
            #     cv2.destroyAllWindows()

    finally:
        # Close the connection
        conn.close()
