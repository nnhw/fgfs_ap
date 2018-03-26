import socket
import struct
import time

sock = socket.socket()
sock.connect(('localhost', 9090))

sock_inter = socket.socket()
sock_inter.connect(('localhost', 9093))

#data_send = struct.pack('!iiii',0,0,0,305419896)

while True:
    time.sleep(1)
    data_recv = sock_inter.recv(24)
    udata = struct.unpack('!iiiiii',data_recv) #TODO:Порядок байт наоборот!
    print(udata)
    data_send = struct.pack('!iiii',udata[0]+1,udata[1]+1,udata[2]+1,305419896)
    print(data_send)
    sock.send(data_send)




