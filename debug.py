from connection import connection_debug
import time

connection_interface = connection_debug(l_type="in", l_port_in=9002)

while True:
    time.sleep(0.1)
    print(connection_interface.receive_data())
