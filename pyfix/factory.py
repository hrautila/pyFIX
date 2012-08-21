

class ServerFactory(object):
    def __init__(self, protocol, callback, config={}, io_loop=None):
        self.protocol = protocol
        self.callback = callback
        if io_loop == None:
            self.io_loop = IOLoop.instance()
        else:
            self.io_loop = io_loop
        
    def bind(self, address):
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0)
        self.sock.bind(address)
        
    def start(self):
        self.sock.listen(2)
        self.io_loop.add_handler(self.sock.fileno(), self._accept, self.io_loop.READ)
        self.status = SessionStream.LISTENING
        
    def listen(self, address):
        self.bind(address)
        self.start()

    def _accept(self, fd, event):
        conn, address = self.sock.accept()
        server = Server(self.protocol(), self.io_loop, conn)

