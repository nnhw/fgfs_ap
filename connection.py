import socket
import struct
import time


class connection:
    def __init__(self, l_type_c="both", l_port_in_c=0, l_port_out_c=0):
        self._type = l_type_c
        if self._type == "in" or self._type == "both":
            self._data_rcv = b''
            self._port_in = l_port_in_c
            self._sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock_in.bind(('', self._port_in))

        if self._type == "out" or self._type == "both":
            self._data_send = b''
            self._port_out = l_port_out_c
            self._sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, l_data):
        if self._type == "out" or self._type == "both":
            self._data_send = l_data
            self._sock_out.sendto(self._data_send, ("", self._port_out))

    def receive_data(self, l_size):
        if self._type == "in" or self._type == "both":
            self._data_rcv = self._sock_in.recvfrom(l_size)[0]
            return self._data_rcv
        else:
            return 0


class connection_debug(connection):
    def __init__(self, l_type="both", l_port_in=0, l_port_out=0):
        connection.__init__(self, l_type_c=l_type,
                            l_port_in_c=l_port_in, l_port_out_c=l_port_out)

    def _parse_incoming(self, l_data_rcv):
        return struct.unpack('!ffffffffffff', l_data_rcv)

    def _pack_outgoing(self, l_data):
        return struct.pack('!ffffffffffff', l_data[0], l_data[1], l_data[2],
                           l_data[3], l_data[4], l_data[5],
                           l_data[6], l_data[7], l_data[8],
                           l_data[9], l_data[10], l_data[11])

    def send_data(self, l_data):
        connection.send_data(self, self._pack_outgoing(l_data))

    def receive_data(self):
        return self._parse_incoming(connection.receive_data(self, 48))


class connection_autopilot(connection):
    def __init__(self, l_port_in, l_port_out):
        connection.__init__(self, l_type_c="both",
                            l_port_in_c=l_port_in, l_port_out_c=l_port_out)

        self._pitch = 0
        self._roll = 0
        self._yaw = 0
        self._elevator_in = 0
        self._aileron_in = 0
        self._rudder_in = 0
        self._speed = 0
        self._altitude = 0

        self._elevator_out = 0
        self._aileron_out = 0
        self._rudder_out = 0

    def _parse_incoming(self, l_data_rcv):
        udata = struct.unpack('!fffffffff', l_data_rcv)
        self._pitch = udata[0]
        self._roll = udata[1]
        self._yaw = udata[2]
        self._elevator_in = udata[3]
        self._aileron_in = udata[4]
        self._rudder_in = udata[5]
        self._speed = udata[6]
        self._altitude = udata[7]

    def _pack_outgoing(self):
        return struct.pack('!fffi', self._elevator_out, self._aileron_out, self._rudder_out, 305419896)

    def send_data(self, l_elevator, l_aileron, l_rudder):
        self._elevator_out = l_elevator
        self._aileron_out = l_aileron
        self._rudder_out = l_rudder
        self._data_send = self._pack_outgoing()
        connection.send_data(self, self._data_send)

    def receive_data(self):
        self._data_rcv = connection.receive_data(self, 36)
        self._parse_incoming(self._data_rcv)
        return self._pitch, self._roll, self._yaw, self._speed, self._altitude

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
