import socket
import struct

sock = socket.socket()
sock.bind(('', 9091))
sock.listen(1)
conn, addr = sock.accept()

print('fgfs connected:', addr)

sock_inter = socket.socket()
sock_inter.bind(('', 9092))
sock_inter.listen(1)
conn_inter, addr_inter = sock_inter.accept()

print('inter connected:', addr_inter)

while True:
    data = conn.recv(24)
    #udata = data.struct.unpack();
    
 #   print(data)
 #   print(udata)
    conn_inter.send(data)
conn.close()
