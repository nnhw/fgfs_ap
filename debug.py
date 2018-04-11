from connection import connection_debug
from blessings import Terminal
import time

connection_interface = connection_debug(l_type="in", l_port_in=9002)

t = Terminal()

t_elevator = 0
t_aileron = 0
t_rudder = 0

while True:
    time.sleep(0.1)
    print(t.clear())
    with t.location(int(t.width/2), 0):
        print('Debugger')
    with t.location(0, t.height-2):
        print(time.ctime())
    t_data_rcv = connection_interface.receive_data()

    t_elevator = t_data_rcv[0]
    t_aileron = t_data_rcv[1]
    t_rudder = t_data_rcv[2]
    t_P_elevator = t_data_rcv[3]
    t_I_elevator = t_data_rcv[4]
    t_D_elevator = t_data_rcv[5]
    t_P_aileron = t_data_rcv[6]
    t_I_aileron = t_data_rcv[7]
    t_D_aileron = t_data_rcv[8]
    t_P_rudder = t_data_rcv[9]
    t_I_rudder = t_data_rcv[10]
    t_D_rudder = t_data_rcv[11]

    print(t.bold("Elevator = ") + '{0: .5f}'.format(t_elevator))
    print(t.bold("Elevator P = ") + '{0: .5f}'.format(t_P_elevator))
    print(t.bold("Elevator I = ") + '{0: .5f}'.format(t_I_elevator))
    print(t.bold("Elevator D = ") + '{0: .5f}'.format(t_D_elevator))
    print("----------------------------------------------------\n")
    print(t.bold("Aileron = ") + '{0: .5f}'.format(t_aileron))
    print(t.bold("Aileron P = ") + '{0: .5f}'.format(t_P_aileron))
    print(t.bold("Aileron I = ") + '{0: .5f}'.format(t_I_aileron))
    print(t.bold("Aileron D = ") + '{0: .5f}'.format(t_D_aileron))
    print("----------------------------------------------------\n")
    print(t.bold("Rudder = ") + '{0: .5f}'.format(t_rudder))
    print(t.bold("Rudder P = ") + '{0: .5f}'.format(t_P_rudder))
    print(t.bold("Rudder I = ") + '{0: .5f}'.format(t_I_rudder))
    print(t.bold("Rudder D = ") + '{0: .5f}'.format(t_D_rudder))
    print("----------------------------------------------------\n")
