import cmd
from connection import connection
from autopilot import autopilot

connection_fgfs = connection(9091, 9090)
autopilot_fgfs = autopilot()


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
        connection_fgfs.start_data_flow()

    def do_start_calc(self, arg):
        'Start data calculation'
        autopilot_fgfs.start_periodic_update()

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
