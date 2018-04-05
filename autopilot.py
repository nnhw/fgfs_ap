import socket
import time
import struct
import cmd
from threading import Thread
import queue
from enum import Enum


class state(Enum):
    initialization = 0
    updating = 1
    ready = 2


class type(Enum):
    pitch = 0
    roll = 1
    yaw = 2


class pid:
    def __init__(self, l_type, l_p_coeff, l_i_coeff, l_d_coeff):
        self._type = l_type

        self._proportional_coefficient = l_p_coeff
        self._integral_coefficient = l_i_coeff
        self._differential_coefficient = l_d_coeff

        self._I_prev = 0
        self._error_prev = 0
        self._pid_value = 0
        self._P = 0
        self._I = 0
        self._D = 0

    def calculate(self, l_value, l_setpoint):
        t_error = l_setpoint - l_value
        self._P = self._proportional_coefficient * t_error
        self._I = self._I_prev + self._integral_coefficient * t_error
        # if I > 0.3:
        #     I = 0.3
        self._D = self._differential_coefficient * (t_error - self._error_prev)
        t_pid_value = self._P + self._I + self._D
        self._error_prev = t_error
        self._pid_prev = t_pid_value

        if self._type == type.pitch:
            return -t_pid_value
        else:
            return t_pid_value


class autopilot:
    def __init__(self):
        self._state = state.initialization
        self._update_rate_hz = 10

        self._pitch_setpoint = 0
        self._roll_setpoint = 0
        self._yaw_setpoint = 0
        
        self._pitch_value = 0
        self._roll_value = 0
        self._yaw_value = 0
        
        self._yaw_block = False
        
        self._elevator = 0
        self._aileron = 0
        self._rudder = 0
        
        self._pid_aileron = pid(type.roll, 0.0055, 0.0001, 0.0001)
        self._pid_elevator = pid(type.pitch, 0.0055, 0.0001, 0.0001)
        self._pid_rudder = pid(type.yaw, 0.0055, 0.0001, 0.0001)

    def _update_state(self):
        self._state = state.updating
        self._elevator = self._pid_elevator.calculate(self._pitch_value, self._pitch_setpoint)
        self._aileron = self._pid_aileron.calculate(self._roll_value, self._roll_setpoint)
        if self._yaw_block is True:
            self._rudder = 0
        elif self._yaw_block is False:
            self._rudder = self._pid_rudder.calculate(self._yaw_value, self._yaw_setpoint)
        self._state = state.ready
    
    def get_result(self):
        return self._elevator, self._aileron, self._rudder

    def set_setpoint(self, l_type, l_value):
        if l_type == type.pitch:
            self._pitch_setpoint = l_value
        elif l_type == type.roll:
            self._roll_setpoint = l_value
        elif l_type == type.yaw:
            self._yaw_setpoint = l_value

    def set_value(self, l_type, l_value):
        if l_type == type.pitch:
            self._pitch_value = l_value
        elif l_type == type.roll:
            self._roll_value = l_value
        elif l_type == type.yaw:
            self._yaw_value = l_value

    def isReady(self):
        if self._state == state.ready:
            return True
        else:
            return False

    def _periodic_update_handler(self):
        while True:  # TODO: Переделать на срабатыванию новых данных
            time.sleep(1/self._update_rate_hz)
            self._update_state()

    def start_periodic_update(self):
        data_calculation_thread = Thread(target=self._periodic_update_handler)
        data_calculation_thread.daemon = True
        data_calculation_thread.start()
