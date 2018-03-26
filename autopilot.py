import socket
import time
import struct

def parse(data):
    udata = struct.unpack('!iiiiii',data)
    _pitch = udata[0]
    _roll = udata[1]
    _yaw = udata[2]
    _speed = udata[3]
    _altitude = udata[4]    
    return _pitch,_roll,_yaw

def calculate_output(data):
    pitch, roll, yaw = parse(data)

    print('pitch=',pitch)
    print('roll=',roll)
    print('yaw=',yaw)

    elevator = 0
    aileron = 0
    rudder = 0

    data_send = struct.pack('!iiii',elevator,aileron,rudder,305419896)
    return data_send


sock_client = socket.socket()
sock_client.bind(('', 9093))
sock_client.listen(1)
conn_client, addr_client = sock_client.accept()

sock_server = socket.socket()
sock_server.connect(('localhost', 9092))

while True:
    time.sleep(1)
    data_rcv = sock_server.recv(24)

    data_send = calculate_output(data_rcv)

    conn_client.send(data_send)
