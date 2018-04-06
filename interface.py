import cmd
from connection import connection
from autopilot import autopilot, state, type
from threading import Thread
import time

connection_fgfs = connection(9091, 9090)
autopilot_fgfs = autopilot()

update_rate_hz = 10


def start_data_flow():
    data_flow_thread = Thread(target=data_flow_handler)
    data_flow_thread.daemon = True
    data_flow_thread.start()


def data_flow_handler():
    global update_rate_hz
    while True:
        time.sleep(1/update_rate_hz)
        t_pitch, t_roll, t_yaw, t_speed, t_altitude = connection_fgfs.receive_data()

        autopilot_fgfs.set_value(type.pitch, t_pitch)
        autopilot_fgfs.set_value(type.roll, t_roll)
        autopilot_fgfs.set_value(type.yaw, t_yaw)
        autopilot_fgfs.set_setpoint(type.pitch, 0)
        autopilot_fgfs.set_setpoint(type.roll, 0)
        autopilot_fgfs.set_setpoint(type.yaw, 0)

        while autopilot_fgfs.isReady() is not True:
            pass

        t_elevator, t_aileron, t_rudder = autopilot_fgfs.get_result()

        connection_fgfs.send_data(t_elevator, t_aileron, t_rudder)


# def _periodic_update_handler(self):
#     while True:  # TODO: Переделать на срабатыванию новых данных
#         time.sleep(1/self._update_rate_hz)
#         self._update_state()


def start_periodic_update(self):
    data_calculation_thread = Thread(target=self._periodic_update_handler)
    data_calculation_thread.daemon = True
    data_calculation_thread.start()


class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell. Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_set_pitch(self, arg):
        'Set pitch'
        I_prev_p = 0
        pitch_setpoint = parse(arg)

    def do_set_roll(self, arg):
        'Set roll'
        I_prev_r = 0
        roll_setpoint = parse(arg)

    def do_set_yaw(self, arg):
        'Set yaw'
        yaw_block = False
        I_prev_y = 0
        yaw_setpoint = parse(arg)

    def do_stop_yaw_stab(self, arg):
        'Stop yaw calc'

    def do_takeoff(self, arg):
        'take-off'

    def do_start_flow(self, arg):
        'Start data flow'
        start_data_flow()

    # def do_start_calc(self, arg):
    #     'Start data calculation'
    #     autopilot_fgfs.start_periodic_update()

    # def do_start_log(self, arg):
    #     'Start data logging'
    #     start_data_logging()

    def do_bye(self, arg):
        'Exit'
        print('Good Bye')
        return True


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    # return tuple(map(int, arg.split()))
    return int(arg)


if __name__ == "__main__":
    ConvertShell().cmdloop()
