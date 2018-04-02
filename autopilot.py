import socket
import time
import struct
import cmd
from threading import Thread
import queue

error_prev = 0
I_prev_p = 0
I_prev_r = 0
I_prev_y = 0
pid_prev = 0

pitch_setpoint = 0
roll_setpoint = 0
yaw_setpoint = 0

yaw_block = 0

data_rcv = b''
data_send = b''


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

    if _mode == "pitch":
        return -pid_value
    else:
        return pid_value



def calculate_output(data):
    global pitch_setpoint
    global roll_setpoint
    global yaw_setpoint
    global yaw_block
    pitch, roll, yaw = parse_incoming(data)[0:3]
    elevator = calculate_pid(pitch,pitch_setpoint,"pitch") 
    aileron = calculate_pid(roll,roll_setpoint,"roll")
    if yaw_block == True:
        rudder = 0
    elif yaw_block == False:
        rudder = calculate_pid(yaw, yaw_setpoint,"yaw")
        roll_setpoint = rudder * 10
    return pack_outgoing(elevator, aileron, rudder)



def data_calculation_handler():
    global data_rcv
    global data_send
    while True:
        time.sleep(0.1)
        data_send = calculate_output(data_rcv)

def data_logging_handler(_file):
    while(True):
        global data_rcv
        pitch,roll,yaw,elevator,aileron,rudder,speed,altitude = parse_incoming(data_rcv)
        _file.write('{}\n Pitch = {}, Roll = {},Yaw = {}\n Elevator = {}, Aileron = {}, Rudder = {}\n Speed = {}, Altitude =  {}\n\n'.format
                    (time.ctime(),pitch,roll,yaw,elevator,aileron,rudder,speed,altitude))
        _file.flush
        time.sleep(1)



def start_data_calculation():
    data_calculation_thread = Thread(target = data_calculation_handler)
    data_calculation_thread.daemon = True
    data_calculation_thread.start()

def start_data_logging():
    f = open('output.log', 'a')
    data_logging_thread = Thread(target = data_logging_handler,args = (f,))
    data_logging_thread.daemon = True
    data_logging_thread.start()







