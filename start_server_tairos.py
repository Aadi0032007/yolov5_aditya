# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 00:40:29 2023

@author: aadi
"""

import socket
import cv2
import numpy as np
import os
import sys
import tempfile
import time
from datetime import datetime

# Add YOLOv5 folder to the sys.path
# yolov5_path = "C:/Users/AI/Aditya_project/yolov5_aditya"
yolov5_path = "C:/Users/user/Spyder Project/YOLOv5/yolov5_aditya"   # change back
sys.path.append(yolov5_path) 

# Import the run function
from detect import run,load_model
 # Provide the required arguments for the run function
weights = os.path.join(yolov5_path, 'yolov5x_bottle.pt')  # Replace with the path to your model weights
iou_thres = 0.55
augment = True

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = "localhost"
port = 8008
sock.bind((host, port))

count = 0
total_time = 0

# Listen for incoming connections
sock.listen(1)
print(f"Listening on {host}:{port}")
model,stride,names,pt = load_model(weights=weights)

while True:
    # Wait for a connection
    conn, addr = sock.accept()
    print(f"Connection established from {addr}")

    try:
        while True:
            # Receive the image length
            img_len_bytes = conn.recv(8)
            if not img_len_bytes:
                print("Didn't recieve image length.")
                break
            
            # Convert the image length bytes to an integer
            img_len = int.from_bytes(img_len_bytes, 'big')
            print("Image data length : ",img_len)            
            
            # Receive the image data
            image_data = b""
            while True:
                count+=1
                data = conn.recv(4096)
                # print(len(data),count)
                if len(data) < 4096:
                    break
                image_data += data
                

            # If no more data is received, the connection is closed
            if not image_data:
                print("Connection closed by client.")
                break
            
            # print ("Recieved data size: ", len(image_data))
            # print("Converting Buffer to Arary.")

            # Convert the image data to a NumPy array
            nparr = np.frombuffer(image_data, dtype=np.uint8)

            # print("Converting Array to Image.")
            # Decode the NumPy array to an OpenCV image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # print("Temp file created.")
            # Save the cv2 image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_img:
                temp_image_path = tmp_img.name
                cv2.imwrite(temp_image_path, img)
            
            # print("Running detection..")
            # Call the run function
            before = datetime.now()
            output = run(weights=weights, source=temp_image_path, iou_thres=iou_thres,augment=augment,
                         model=model,stride=stride,names=names,pt=pt)
            after = datetime.now()
            duration = after - before
            total_time+=int( duration.microseconds // 1000)
            print("inference time : ",int( duration.microseconds // 1000),"ms")

            # Remove the temporary image file
            os.remove(temp_image_path)
            
                        
            # encoding response
            response = output.encode()
           
            # encoding rsponse lenghth 
            response_len = len(response).to_bytes(8, 'big')
            # print('Sending Response Length')
            conn.send(response_len)
            
            # # Wait for a short delay (optional)
            # time.sleep(1)
            
            # print('Sending Response')
            # response = 'Add Yolo Output Here'
            conn.send(response)
            print('sent response')
            

    finally:
        # Close the connection
        conn.close()
        print("avg inference time :",total_time//25)
        sys.exit()