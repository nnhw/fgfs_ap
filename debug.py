from connection import connection_debug
from blessings import Terminal
import time

connection_interface = connection_debug(l_type="in", l_port_in=9002)

t = Terminal()

pitch = 0
roll = 0
yaw = 0

while True:
    time.sleep(0.1)
    print(t.clear())
    with t.location(int(t.width/2), 0):
        print('Debugger')
    with t.location(0, t.height-2):
        print(time.ctime())
    pitch, roll, yaw = connection_interface.receive_data()
    print(t.bold("Elevator = ") + '{0: .5f}'.format(pitch))
    print(t.bold("Aileron = ") + '{0: .5f}'.format(roll))
    print(t.bold("Rudder = ") + '{0: .5f}'.format(yaw))
