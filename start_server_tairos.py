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
yolov5_path = "C:/Users/AI/Aditya_project/yolov5_aditya"
# yolov5_path = "C:/Users/user/Spyder Project/YOLOv5/yolov5_aditya"   # change back
sys.path.append(yolov5_path)

# Import the run function
from detect import run, load_model

### YOLO model
# weights = os.path.join(yolov5_path, 'yolov5x_bottle.pt')  # Replace with the path to your model weights

### YOLO - OpenVINO optmized model
weights = os.path.join(yolov5_path, "yolov5x_bottle_back_openvino_model")

iou_thres = 0.55
conf_thres = 0.15
augment = True
debug_save = False  # change to True if want to save image for debugging
device = "CPU"

# Load the model
model, stride, names, pt = load_model(weights=weights, device=device)

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


while True:
    # Wait for a connection
    conn, addr = sock.accept()
    print(f"Connection established from {addr}")

    try:
        while True:
            # Receive the image length
            print("Waiting for image length")
            img_len_bytes = conn.recv(4)
            if not img_len_bytes:
                # print("Didn't recieve image length.")
                break

            # Convert the image length bytes to an integer
            img_len = int.from_bytes(img_len_bytes, "little", signed=False)
            # print("  Image data length : ",img_len)

            before = time.time()
            # Receive the image data
            image_data = b""

            # image_data = conn.recv(img_len)
            to_read_len = img_len
            data_len = 0
            while True:
                count += 1
                data = conn.recv(to_read_len)
                # print(len(data)," ", end="")
                data_len = len(data)

                image_data += data
                to_read_len -= data_len
                if to_read_len == 0:
                    break

            # print("  recieved image data",len(image_data))
            img_len = len(image_data)

            after = time.time()
            duration = after - before
            # print("  transmission time : ",duration * 1000,"ms")

            # If no more data is received, the connection is closed
            if not image_data:
                print("Connection closed by client.")
                break

            # Convert the image data to a NumPy array
            nparr = np.frombuffer(image_data, dtype=np.uint8)

            # Decode the NumPy array to an OpenCV image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # print("  Image size: ", img.shape)

            # Save the cv2 image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_img:
                temp_image_path = tmp_img.name
                cv2.imwrite(temp_image_path, img)

            # Call the run function
            before = time.time()
            output = run(
                weights=weights,
                source=temp_image_path,
                iou_thres=iou_thres,
                conf_thres=conf_thres,
                augment=augment,
                model=model,
                stride=stride,
                names=names,
                pt=pt,
                debug_save=debug_save
            )
            after = time.time()
            duration = after - before
            print("  inference time: ", duration * 1000, " ms")

            # Remove the temporary image file
            os.remove(temp_image_path)

            # encoding response
            response = output.encode()
            print ("*** Detected : ", output[0], " bottles")
            print(response)

            # encoding rsponse lenghth
            response_len = len(response).to_bytes(8, "little", signed=False)

            # print('  Sending Response Length')
            conn.send(response_len)

            # print('Sending Response')
            conn.send(response)
            print ("==================================")

    except Exception as e:
        print ("Exception: ", e.str())
        pass

    conn.close()
