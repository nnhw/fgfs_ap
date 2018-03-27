import socket
import time
import struct

def parse(data):
    udata = struct.unpack('!iiifffiii',data)
    _pitch = udata[0]
    _roll = udata[1]
    _yaw = udata[2]
    _elevator = udata[3]
    _aileron = udata[4]
    _rudder = udata[5]
    _speed = udata[6]
    _altitude = udata[7]
    print('aileron=', _aileron)    
    return _pitch,_roll,_yaw

def calculate_output(data):
    pitch, roll, yaw = parse(data)

    print('pitch=',pitch)
    print('roll=',roll)
    print('yaw=',yaw)

    
    elevator = 0
    aileron = -0.01*roll
    rudder = 0

    data_send = struct.pack('!fffi',elevator,aileron,rudder,305419896)
    return data_send


sock_client = socket.socket()
sock_client.bind(('', 9093))
sock_client.listen(1)
conn_client, addr_client = sock_client.accept()

sock_server = socket.socket()
sock_server.connect(('localhost', 9092))

while True:
    time.sleep(1)
    data_rcv = sock_server.recv(36)

    data_send = calculate_output(data_rcv)

    conn_client.send(data_send)
