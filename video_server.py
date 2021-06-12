import socket
#import sys
import cv2
import pickle
#import numpy as np
import struct
import imutils

HOST = socket.gethostbyname(socket.gethostname())
PORT = int(input("Please enter the port no of server: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(10)

print(f'[+] SERVER listening on {HOST}:{PORT}')
print("[+] Press Q to quit")


while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        
        while(vid.isOpened()):
            ret, frame = vid.read()
            
            frame = imutils.resize(frame, width=320)
            
            a = pickle.dumps(frame)  # serializing data

            # packing the data with size used in server
            message = struct.pack("Q",len(a))+a
            
            client_socket.sendall(message)
            
            cv2.imshow('LIVE!',frame)  #opening the window 
			
            # waiting for key input and doing AND operation on pressed key and 0xFF binary(11111111)
            key = cv2.waitKey(1) & 0xFF
			
            # if binary of key == binary of 'q' then close socket
            if key ==ord('q'):
                 client_socket.close()
