import socket
from struct import pack, unpack
from threading import Lock

from .Message import Message
from .MessageSerializer import MessageSerializer, JsonSerializer

__all__ = ["SocketManager"]


class SocketManager:
    def __init__(self, **kwargs):
        self.socket = kwargs.get("socket", None)
        self.address = kwargs.get("address", None)
        self.Serializer = kwargs.get("Serializer", JsonSerializer)
        self._send_lock = Lock()
        self._receive_lock = Lock()

        if self.address is not None:
            if self.socket is None:
                self.socket = socket.socket()
                self.socket.connect(self.address)
        else:
            raise TypeError("SocketManager constructor should provide an "
                            "'address' key with (host, port) tuple.")

        try:
            isserializer = issubclass(self.Serializer, MessageSerializer)
        except:
            isserializer = False

        if not isserializer:
            raise TypeError("'Serializer' key should contain a subclass of {}."
                            .format(MessageSerializer.__name__))

    def Receive(self):
        with self._receive_lock:
            data = None
            try:
                data = self.socket.recv(4)
                if len(data) != 4:
                    return None
                msg_size = unpack("<I", data)[0]
                data = self.socket.recv(msg_size)
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
                data = pack("<I", len(serialized))
                data += serialized
                self.socket.send(data)
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
