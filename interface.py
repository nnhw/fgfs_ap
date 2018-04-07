import cmd
from connection import connection_autopilot, connection
from autopilot import autopilot, state, type
from threading import Thread
import time


def start_data_flow():
    data_flow_thread = Thread(target=data_flow_handler)
    data_flow_thread.daemon = True
    data_flow_thread.start()


def data_flow_handler():
    global update_rate_hz
    while True:
        time.sleep(1/update_rate_hz)
        t_pitch, t_roll, t_yaw, t_speed, t_altitude = connection_fgfs.receive_data()

        # print(t_pitch, t_roll, t_yaw)

        autopilot_fgfs.set_value(type.pitch, t_pitch)
        autopilot_fgfs.set_value(type.roll, t_roll)
        autopilot_fgfs.set_value(type.yaw, t_yaw)

        autopilot_fgfs.update_state()

        while autopilot_fgfs.isReady() is not True:
            pass

        t_elevator, t_aileron, t_rudder = autopilot_fgfs.get_result()

        connection_debug.send_data(bytes(t_elevator, t_aileron, t_rudder))
        connection_fgfs.send_data(t_elevator, t_aileron, t_rudder)


def start_periodic_update(self):
    data_calculation_thread = Thread(target=self._periodic_update_handler)
    data_calculation_thread.daemon = True
    data_calculation_thread.start()


class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell. Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_set_pitch(self, arg):
        'Set pitch'
        pitch_setpoint = parse(arg)
        autopilot_fgfs.set_setpoint(type.pitch, pitch_setpoint)

    def do_set_roll(self, arg):
        'Set roll'
        I_prev_r = 0
        roll_setpoint = parse(arg)
        autopilot_fgfs.set_setpoint(type.roll, roll_setpoint)

    def do_set_yaw(self, arg):
        'Set yaw'
        yaw_setpoint = parse(arg)
        autopilot_fgfs.set_setpoint(type.yaw, yaw_setpoint)

    def do_stop_yaw_stab(self, arg):
        'Stop yaw calc'
        autopilot_fgfs.set_block(type.yaw)

    def do_takeoff(self, arg):
        'take-off'

    def do_start_flow(self, arg):
        'Start data flow'
        start_data_flow()

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
    connection_fgfs = connection_autopilot(9091, 9090)
    connection_debug = connection(l_type_c="out", l_port_out_c=9002)
    autopilot_fgfs = autopilot()
    update_rate_hz = 10
    ConvertShell().cmdloop()
