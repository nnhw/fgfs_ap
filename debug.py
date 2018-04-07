from connection import connection
import time

connection_interface = connection(l_type_c="in", l_port_in_c=9002)

while True:
    time.sleep(1)
    print(connection_interface.receive_data())
