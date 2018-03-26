import socket
import time

sock_fgfs = socket.socket()
sock_fgfs.connect(('localhost', 9090))

sock_ap = socket.socket()
sock_ap.connect(('localhost', 9093))

while True:
    time.sleep(1)
    data_recv = sock_ap.recv(16)
    sock_fgfs.send(data_recv)




