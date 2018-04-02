import cmd
from connection import connection

connection_fgfs = connection()

class ConvertShell(cmd.Cmd):
    intro = 'Welcome to the Converter shell.   Type help or ? to list commands.\n'
    prompt = '(command) '

    def do_set_pitch(self, arg):
        'Set pitch'
        global pitch_setpoint
        global I_prev_p
        I_prev_p = 0
        pitch_setpoint = parse(arg)

    def do_set_roll(self, arg):
        'Set roll'
        global roll_setpoint
        global I_prev_r
        I_prev_r = 0
        roll_setpoint = parse(arg)

    def do_set_yaw(self, arg):
        'Set yaw'
        global yaw_setpoint
        global I_prev_y
        global yaw_block
        yaw_block = False
        I_prev_y = 0
        yaw_setpoint = parse(arg)        

    def do_stop_yaw_stab(self, arg):
        'Stop yaw calc'
        global yaw_block
        yaw_block = True

    def do_takeoff(self, arg):
        'take-off'

    def do_start_flow(self, arg):
        'Start data flow'
        connection_fgfs.start_data_flow()

    def do_start_calc(self, arg):
        'Start data calculation'
        start_data_calculation()
 
    def do_start_log(self, arg):
        'Start data logging'
        start_data_logging()

    def do_bye(self,arg):
        'Exit'
        print('Good Bye')
        return True

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    # return tuple(map(int, arg.split()))
    return int(arg)


if __name__ == "__main__":
    ConvertShell().cmdloop()