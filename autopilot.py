import socket
import time
import datetime
import struct
import cmd
from threading import Thread

error_prev = 0
I_prev_p = 0
I_prev_r = 0
I_prev_y = 0
pid_prev = 0

pitch_setpoint = 0
roll_setpoint = 0
yaw_setpoint = 0

data_rcv = b''
data_send = b''

    #Класс-оболочка для командного интерфейса
class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell.   Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_set_pitch(self, arg):
        'Set pitch'
        global pitch_setpoint
        global I_prev_p
        I_prev_p = 0
        pitch_setpoint = parse(arg)
        # print('hi!')

    def do_set_roll(self, arg):
        'Set roll'
        global roll_setpoint
        global I_prev_r
        I_prev_r = 0
        roll_setpoint = parse(arg)
        # print('hi!')

    def do_set_yaw(self, arg):
        'Set yaw'
        global yaw_setpoint
        global I_prev_y
        I_prev_y = 0
        yaw_setpoint = parse(arg)        
        # print('hi!')

    def do_start(self, arg):
        'Start!'
        start_data_flow()

    def do_start_data(self, arg):
        'Start data flow'
        start_data_flow()

    def do_start_calculation(self, arg):
        'Start data calculation'
        start_data_calculation()


    def do_bye(self,arg):
        'Exit'
        print('Good Bye')
        return True

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    # return tuple(map(int, arg.split()))
    return int(arg)

def calculate_pid(_value,_setpoint,_mode):
    global error_prev
    global pid_prev
    global I_prev_p
    global I_prev_r
    global I_prev_y

    if _mode == "pitch":
        I_prev = I_prev_p
    elif _mode == "roll":
        I_prev = I_prev_r
    elif _mode == "yaw":
        I_prev = I_prev_y


    proportional_coefficient = 0.0055 
    integral_coefficient = 0.0001
    differential_coefficient = 0.001
 
    pid_value = 0 
    error = 0
    P = 0
    I = 0
    D = 0

    error = _setpoint - _value

    P = proportional_coefficient * error
    I = I_prev + integral_coefficient * error
    if I > 0.3:
        I = 0.3
    D = differential_coefficient * (error - error_prev)

    pid_value = P+I+D
    error_prev = error

    if _mode == "pitch":
        I_prev_p = I
    elif _mode == "roll":
        I_prev_r = I
    elif _mode == "yaw":
        I_prev_y = I

    pid_prev = pid_value

    return pid_value

def parse_incoming(data):
    udata = struct.unpack('!iiifffiii',data)
    _pitch = udata[0]
    _roll = udata[1]
    _yaw = udata[2]
    _elevator = udata[3]
    _aileron = udata[4]
    _rudder = udata[5]
    _speed = udata[6]
    _altitude = udata[7]
    # print('pitch=',_pitch)
    # print('roll=',_roll)
    # print('yaw=',_yaw)
    # print('elevator=', _elevator)    
    # print('aileron=', _aileron)    
    # print('rudder=', _rudder)    
    return _pitch,_roll,_yaw

def pack_outgoing(_elevator,_aileron,_rudder):
    return struct.pack('!fffi',_elevator,_aileron,_rudder,305419896)

def calculate_output(data):
    global pitch_setpoint
    global roll_setpoint
    pitch, roll, yaw = parse_incoming(data)
    elevator = -calculate_pid(pitch,pitch_setpoint,"pitch") 
    aileron = calculate_pid(roll,roll_setpoint,"roll")
    rudder = calculate_pid(yaw, yaw_setpoint,"yaw")
    return pack_outgoing(elevator, aileron, rudder)

def data_flow_handler(_sock_in,_sock_out):
    global data_rcv
    global data_send
    while True:
        time.sleep(0.1)
        data_rcv, address = _sock_in.recvfrom(36)
        _sock_out.sendto(data_send,("", 9090))

def data_calculation_handler():
    global data_rcv
    global data_send
    while True:
        time.sleep(0.1)
        data_send = calculate_output(data_rcv)

def start_data_flow():
    # conn_in = wait_for_incoming_connection_from_fgfs()
    # sock_out = connect_to_fgfs()
    sock_in = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock_out = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock_in.bind(('', 9091))

    data_flow_thread = Thread(target = data_flow_handler,args = (sock_in,sock_out))
    data_flow_thread.daemon = True
    data_flow_thread.start()

def start_data_calculation():
    data_calculation_thread = Thread(target = data_calculation_handler)
    data_calculation_thread.daemon = True
    data_calculation_thread.start()

if __name__ == "__main__":
    ConvertShell().cmdloop()






