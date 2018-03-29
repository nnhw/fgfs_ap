import socket
import time
import struct

# error_prev = 0
# I_prev = 0
# pid_prev = 0

def calculate_pid(_value,_setpoint):
    proportional_coefficient = 0.01
    integral_coefficient = 0
    differential_coefficient = 0
 
    pid_value = 0 
    error = 0
    P = 0
    I = 0
    D = 0

    error = _setpoint - _value

    P = proportional_coefficient * error
    # I = I_prev + integral_coefficient * error
    # if I>500:
    #     I = 500
    # D = differential_coefficient * (error - pid_prev)

    pid_value = P+I+D
    error_prev = error
    I_prev = I
    # pid_value += 1500

    # if(angle_value>2000) angle_value = 2000;
    # if(angle_value<1000) angle_value = 1000;

    pid_prev = pid_value

    return pid_value

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
    print('elevator=', _elevator)    
    print('aileron=', _aileron)    
    print('rudder=', _rudder)    
    return _pitch,_roll,_yaw

def calculate_output(data):
    pitch, roll, yaw = parse(data)

    print('pitch=',pitch)
    print('roll=',roll)
    print('yaw=',yaw)
    
    elevator = -calculate_pid(pitch,0) 
    aileron = calculate_pid(roll,0)
    rudder = 0 #-0.01*roll

    data_send = struct.pack('!fffi',elevator,aileron,rudder,305419896)
    return data_send

def reconnect_to_fgfs(_socket):
    print('reconnecting...')
    try:
        _socket.connect(('localhost', 9090))
    except Exception:
        time.sleep(1);
        reconnect_to_fgfs(_socket);

def connect_to_fgfs():
    print('connecting...')
    _sock_out = socket.socket()
    try:
        sock_out.connect(('localhost', 9090))
    except Exception:
        time.sleep(1);
        reconnect_to_fgfs(_sock_out);
    print('outgoing connection established')
    return _sock_out
        
def wait_for_incoming_connection_from_fgfs():
    print('waiting for connecting...')
    _sock_in = socket.socket()
    _sock_in.bind(('', 9091))
    _sock_in.listen(1)
    _conn_in, _addr_in = _sock_in.accept()
    print('incoming connection established:', _addr_in)
    return _conn_in, _addr_in

conn_in, addr_in = wait_for_incoming_connection_from_fgfs()
sock_out = connect_to_fgfs()

while True:
    time.sleep(1)
    data_rcv = conn_in.recv(36)

    data_send = calculate_output(data_rcv)

    sock_out.send(data_send)
