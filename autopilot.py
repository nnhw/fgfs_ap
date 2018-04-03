import socket
import time
import struct
import cmd
from threading import Thread
import queue

data_rcv = b''
data_send = b''


class pid:
    def __init__(self, l_type, l_p_coeff, l_i_coeff, l_d_coeff):
        self._type = l_type

        self._proportional_coefficient = l_p_coeff
        self._integral_coefficient = l_i_coeff
        self._differential_coefficient = l_d_coeff

        self._pitch_setpoint = 0
        self._roll_setpoint = 0
        self._yaw_setpoint = 0
        self._yaw_block = False
        self._I_prev = 0
        self._error_prev = 0
        self._pid_value = 0
        self._error = 0
        self._P = 0
        self._I = 0
        self._D = 0

    def calculate_pid(self, l_value, l_setpoint):
        t_error = l_setpoint - l_value
        self._P = self._proportional_coefficient * t_error
        self._I = self._I_prev + self._integral_coefficient * t_error
        # if I > 0.3:
        #     I = 0.3
        self._D = self._differential_coefficient * (t_error - self._error_prev)
        t_pid_value = self._P + self._I + self._D
        self._error_prev = t_error
        self._pid_prev = t_pid_value

        if self._type == "pitch":
            return -t_pid_value
        else:
            return t_pid_value


class autopilot:
    _pid_aileron = pid('aileron', 0.0055, 0.0001, 0.0001)
    _pid_elevator = pid('elevator', 0.0055, 0.0001, 0.0001)
    _pid_aileron = pid('aileron', 0.0055, 0.0001, 0.0001)
    _pid_aileron = pid('aileron', 0.0055, 0.0001, 0.0001)


def calculate_output(data):
    pitch, roll, yaw = parse_incoming(data)[0:3]
    elevator = calculate_pid(pitch, pitch_setpoint, "pitch")
    aileron = calculate_pid(roll, roll_setpoint, "roll")
    if yaw_block is True:
        rudder = 0
    elif yaw_block is False:
        rudder = calculate_pid(yaw, yaw_setpoint, "yaw")
        roll_setpoint = rudder * 10
    return pack_outgoing(elevator, aileron, rudder)


def data_calculation_handler():
    global data_rcv
    global data_send
    while True:
        time.sleep(0.1)
        data_send = calculate_output(data_rcv)


def start_data_calculation():
    data_calculation_thread = Thread(target=data_calculation_handler)
    data_calculation_thread.daemon = True
    data_calculation_thread.start()
