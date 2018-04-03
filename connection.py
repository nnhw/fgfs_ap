import socket
import struct
import time
from threading import Thread


class connection:
    _data_send = 0
    _data_rcv = 0

    def start_data_flow(self):
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_in.bind(('', 9091))

        data_flow_thread = Thread(
            target=self._data_flow_handler, args=(sock_in, sock_out))
        data_flow_thread.daemon = True
        data_flow_thread.start()

    def start_data_logging(self):
        f = open('output.log', 'a')
        data_logging_thread = Thread(target=data_logging_handler, args=(f,))
        data_logging_thread.daemon = True
        data_logging_thread.start()

    def _data_flow_handler(self, _sock_in, _sock_out):
        while True:
            time.sleep(0.1)
            self._data_rcv = _sock_in.recvfrom(36)[0]
            _sock_out.sendto(self._data_send, ("", 9090))

    def parse_incoming(self, data):
        udata = struct.unpack('!iiifffiii', data)
        _pitch = udata[0]
        _roll = udata[1]
        _yaw = udata[2]
        _elevator = udata[3]
        _aileron = udata[4]
        _rudder = udata[5]
        _speed = udata[6]
        _altitude = udata[7]
        return _pitch, _roll, _yaw, _elevator, _aileron, _rudder, _speed, _altitude

    def pack_outgoing(self, _elevator, _aileron, _rudder):
        return struct.pack('!fffi', _elevator, _aileron, _rudder, 305419896)

    def data_logging_handler(self,_file):
        while(True):
            global data_rcv
            pitch, roll, yaw, elevator, aileron, rudder, speed, altitude = parse_incoming(
                data_rcv)
            _file.write('{}\n Pitch = {}, Roll = {},Yaw = {}\n Elevator = {}, Aileron = {}, Rudder = {}\n Speed = {}, Altitude =  {}\n\n'.format
                        (time.ctime(), pitch, roll, yaw, elevator, aileron, rudder, speed, altitude))
            _file.flush
            time.sleep(1)
