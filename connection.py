import socket
import struct
import time


class connection:
    def __init__(self, l_port_in, l_port_out):
        self._data_send = b''
        self._data_rcv = b''
        self._port_in = l_port_in
        self._port_out = l_port_out

        self._pitch = 0 
        self._roll = 0
        self._yaw = 0
        self._elevator = 0
        self._aileron = 0
        self._rudder = 0
        self._speed = 0
        self._altitude = 0

        self.sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_in.bind(('', self._port_in))

    def _parse_incoming(self):
        udata = struct.unpack('!iiifffiii', self._data_rcv)
        self._pitch = udata[0]
        self._roll = udata[1]
        self._yaw = udata[2]
        self._elevator = udata[3]
        self._aileron = udata[4]
        self._rudder = udata[5]
        self._speed = udata[6]
        self._altitude = udata[7]

    def _pack_outgoing(self, _elevator, _aileron, _rudder):
        return struct.pack('!fffi', _elevator, _aileron, _rudder, 305419896)

    def send_data(self, l_data):
        self._data_send = self._pack_outgoing(l_data)
        _sock_out.sendto(self._data_send, ("", self._port_out))

    def receive_data(self):
        self._data_rcv = _sock_in.recvfrom(36)[0]
        self._parse_incoming
        return self._data_rcv

    # def start_data_logging(self):
    #     f = open('output.log', 'a')
    #     data_logging_thread = Thread(target=self.data_logging_handler, args=(f,))
    #     data_logging_thread.daemon = True
    #     data_logging_thread.start()

    # def data_logging_handler(self, _file):
    #     while(True):
    #         pitch, roll, yaw, elevator, aileron, rudder, speed, altitude = self.parse_incoming(
    #             self._data_rcv)
    #         _file.write('{}\n Pitch = {}, Roll = {},Yaw = {}\n Elevator = {}, Aileron = {}, Rudder = {}\n Speed = {}, Altitude =  {}\n\n'.format
    #                     (time.ctime(), pitch, roll, yaw, elevator, aileron, rudder, speed, altitude))
    #         _file.flush
    #         time.sleep(1)
