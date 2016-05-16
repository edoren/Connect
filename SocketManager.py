import socket
from threading import Lock

from .Message import Message
from .MessageSerializer import MessageSerializer, JsonSerializer

__all__ = ["SocketManager"]


class SocketManager:
    def __init__(self, arg=None, Serializer=JsonSerializer):
        self.socket = None
        self.address = None
        self.Serializer = Serializer
        self._send_lock = Lock()
        self._receive_lock = Lock()

        if isinstance(arg, tuple) and len(arg) == 2 and \
           isinstance(arg[0], str) and isinstance(arg[1], int):
            self.address = arg
            self.Connect(self.address)
        elif isinstance(arg, socket.socket):
            self.socket = arg
            self.address = self.socket.getsockname()
        else:
            raise TypeError("fist argument must be a tuple with (host, port) "
                            "or a socket")

        if not issubclass(self.Serializer, MessageSerializer):
            raise TypeError("second argument must be subclass of "
                            "MessageSerializer")

    def Connect(self, address):
        if self.socket is None:
            self.socket = socket.socket()
            self.socket.connect(address)

    def Receive(self, buffer_size=2048):
        with self._receive_lock:
            data = None
            try:
                data = self.socket.recv(buffer_size)
            except:
                raise
            finally:
                if not data:
                    raise socket.error("connection forcibly closed.")
            msg = Message.Decode(data, self.Serializer)
            return msg

    def Send(self, msg):
        with self._send_lock:
            if not isinstance(msg, Message):
                raise TypeError("{0} is not instance of {1}"
                                .format(msg.__class__, Message.__class__))
            serialized = Message.Encode(msg, self.Serializer)
            try:
                self.socket.send(serialized)
            except:
                raise socket.error("connection forcibly closed.")

    def Disconnect(self):
        if self.socket is not None:
            try:
                # Try to close the connection if not closed
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            finally:
                self.socket.close()

    def fileno(self):
        '''Return the attached socket file descriptor'''
        return self.socket.fileno()
