import socket
import time

sock_fgfs = socket.socket()
sock_fgfs.bind(('', 9091))
sock_fgfs.listen(1)
conn_fgfs, addr_fgfs = sock_fgfs.accept()

print('fgfs connected:', addr_fgfs)

sock_ap = socket.socket()
sock_ap.bind(('', 9092))
sock_ap.listen(1)
conn_ap, addr_ap = sock_ap.accept()

print('ap connected:', addr_ap)

while True:
    time.sleep(1)
    data = conn_fgfs.recv(24)
    conn_ap.send(data)
