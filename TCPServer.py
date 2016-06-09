import socket
import select
import threading

from .SafeContainers import SafeDict
from .MessageSerializer import JsonSerializer
from .SocketManager import SocketManager

__all__ = ["TCPServer", "ThreadingTCPServer", "BaseServerHandler"]


class TCPServer:
    """ Simple TCP server using select """

    address_family = socket.AF_INET

    socket_type = socket.SOCK_STREAM

    request_queue_size = 5

    allow_reuse_address = True

    def __init__(self, address, ServerHandler,
                 Serializer=JsonSerializer):
        self.address = address
        self.ServerHandler = ServerHandler(self)
        self.Serializer = Serializer

        self.running = False

        # Create the socket
        self.socket = socket.socket(self.address_family, self.socket_type)

        # Bind to the server address and activate the socket
        self.Bind()
        self.Activate()

        # Create the client list
        self.clients = []

    def Bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.address = self.socket.getsockname()

    def Activate(self):
        self.socket.listen(self.request_queue_size)

    def Start(self):
        self.running = True

        self.ServerHandler.HandleServerStart()

        try:
            self._ServerRun()
        except:
            raise
        finally:
            self.Close()

    def _ServerRun(self):
        while self.running:

            devices_waiting = [self.socket] + self.clients

            (ready_to_read,
             ready_to_write,
             with_error) = select.select(devices_waiting, [], [])

            for device_ready in ready_to_read:

                if device_ready == self.socket:
                    # Handle the server socket
                    (client_socket,
                     client_address) = self.socket.accept()

                    # Create the socket manager for the client
                    socket_manager = SocketManager(socket=client_socket,
                                                   address=client_address,
                                                   Serializer=self.Serializer)

                    # Add the client to the client list and waiting list
                    self.clients.append(socket_manager)

                    # Call the new request handler
                    self.ProcessNewConnection(socket_manager)
                else:
                    # Handle all other sockets
                    try:
                        self.ProcessRequest(device_ready)
                    except socket.error:
                        self.ProcessCloseConnection(device_ready)
                    except:
                        raise

    def ProcessNewConnection(self, socket_manager):
        self.ServerHandler.HandleNewConnection(socket_manager)

    def ProcessRequest(self, socket_manager):
        self.ServerHandler.HandleClientRequest(socket_manager)

    def ProcessCloseConnection(self, socket_manager):
        if socket_manager in self.clients:
            self.ServerHandler.HandleClientClose(socket_manager)
            self.clients.remove(socket_manager)
            socket_manager.Disconnect()

    def Close(self):
        self.running = False

        # Close existing client connections
        for socket_manager in self.clients.copy():
            self.ProcessCloseConnection(socket_manager)

        self.ServerHandler.HandleServerClose()

        # Close the server
        self.socket.close()


class ThreadingTCPServer(TCPServer):

    daemon_threads = False

    working_threads = SafeDict()

    def ProcessRequestThread(self, socket_manager):
        try:
            self.ServerHandler.HandleClientRequest(socket_manager)
            del self.working_threads[socket_manager]
        except:
            del self.working_threads[socket_manager]
            self.ProcessCloseConnection(socket_manager)

    def ProcessRequest(self, socket_manager):
        if socket_manager in self.working_threads.keys():
            return
        t = threading.Thread(target=self.ProcessRequestThread,
                             args=(socket_manager, ))
        self.working_threads[socket_manager] = t
        t.start()

    def Close(self):
        for thread in self.working_threads.values():
            thread.join()
        super(ThreadingTCPServer, self).ServerClose()


class BaseServerHandler:

    def __init__(self, server):
        self.server = server

    def HandleServerStart(self):
        pass

    def HandleNewConnection(self, socket_manager):
        pass

    def HandleClientRequest(self, socket_manager):
        pass

    def HandleClientClose(self, socket_manager):
        pass

    def HandleServerClose(self):
        pass
