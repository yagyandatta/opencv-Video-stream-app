import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = input("Please enter IP address of server") 
port = int(input("Please enter Port number of server"))

client_socket.connect((host_ip,port)) 
data = b""

# calcsize calculate data size which is not even packed
payload_size = struct.calcsize("Q")  

#print(payload_size) gives output  ==> 8

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    
    packed_msg_size = data[:payload_size]     # retrieving the message part from packed data
    # print(packed_msg_size)   gives output like==> b'\xa4\x84\x03\x00\x00\x00\x00\x00'
    
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]   #unpacking the size of data in bytes
    #print(msg_size)   gives output like==> 230564


    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)        #converting in binary
    cv2.imshow("RECEIVING VIDEO",frame)     #opening a window and displaying client video
    key = cv2.waitKey(1) & 0xFF
    
    #Doing AND on pressed key + 0xFF (binary 11111111)
    #if key bytes == q bytes then close
    if key  == ord('q'):
        break
client_socket.close()
