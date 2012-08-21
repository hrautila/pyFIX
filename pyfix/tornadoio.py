#!/usr/bin/env python
#
# (c) Harri Rautila, 2012
#
# This file is part of pyFIX library. It is free software, distributed
# under the terms of the GNU Lesser General Public License Version 3,
# or any later version.
#
# See the COPYING file included in this archive

import errno
import functools
import socket
import signal
import multiprocessing
import os
import time
import logging

from interfaces import SessionStream, Protocol, Application
import exc as exc

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.iostream import IOStream

    
class Session(SessionStream):

    def __init__(self, proto, io_loop=None):
        SessionStream.__init__(self, proto)
        self.io_loop  = io_loop
        if io_loop is None:
            self.io_loop = IOLoop.instance()
        self._iob = ''
        self.ios = None
        self._timers = {}

    def clear_buffer(self):
        self._iob = ''

    def close(self):
        self.ios.close()
        self.status = SessionStream.IDLE
        
    def transmit(self, data):
        #logging.debug("writing %d bytes to stream ...", len(data))
        try:
            self.ios.write(data)
        except Exception, e:
            logging.error("transmit error: %s", str(e))

    def add_timer(self, callback,  secs, name):
        if name not in self._timers:
            # create empty entry to timer table which will be updated
            # in self._setup_timer when actually setting the timer
            self._timers[name] = (False, None)
            self.io_loop.add_callback(functools.partial(self._setup_timer,
                                                        callback, secs, name))
        else:
            logging.warning("timer %s already exists!", name)

    def remove_timer(self, name):
        if name not in self._timers:
            logging.debug("removing non-existent timer  %s...  ", name)
            return

        is_set, timer = self._timers[name]
        if not is_set:
            del self._timers[name]
        elif not isinstance(timer, PeriodicCallback):
            self.io_loop.remove_timeout(timer)
            del self._timers[name]
        else:
            logging.error("use remove_periodic to delete periodic timer")

    def add_periodic(self, callback, secs, name):
        if name not in self._timers:
            pcb = PeriodicCallback(callback, 1000*secs, io_loop=self.io_loop)
            self._timers[name] = (True, pcb)
            pcb.start()
        else:
            logging.warning("periodic timer with name %s already exists!", name)

    def remove_periodic(self, name):
        if name in self._timers:
            is_set, timer = self._timers[name]
            if isinstance(timer, PeriodicCallback):
                timer.stop()
                del self._timers[name]
            else:
                logging.error("use remove_timer to delete normal timer")
        else:
            logging.debug("removing non-existent timer %s ...", name)

    def clear_timers(self):
        for name in self._timers.keys():
            is_set, timer = self._timers[name]
            if isinstance(timer, PeriodicCallback):
                timer.stop()
            else:
                self.io_loop.remove_timeout(timer)
            del self._timers[name]
                
    def _disconnected(self, data):
        logging.info("session disconnected")
        self.protocol.disconnected(self)
        self.close()

    def _receiver(self, data):
        """Stream reader for incoming data stream."""
        self._iob += data
        messages, self._iob = self.protocol.parser(self._iob)
        for m in messages:
            try:
                self.protocol.received(self, m)
            except exc.SessionError, se:
                logging.error("SessionError: %s", str(se))

    def _setup_timer(self, callback, secs, name):
        if name in self._timers:
            is_set, timer = self._timers[name]
            if timer is None:
                timer  = self.io_loop.add_timeout(time.time()+secs, callback)
                self._timers[name] = (True, timer)
            else:
                logging.debug("_setup_timer: non-zero timer %s [%s,%s]",
                              name, is_set, str(timer))
        else:
            logging.debug("_setup_timer: %s not in timer table", name)


class Client(Session):
    def __init__(self, protocol, io_loop=None):
        Session.__init__(self, protocol, io_loop)
        self.auto_reconnect = True
        self.reconnect_time = 5
        self.connect_time = 5

    def connect(self, address):
        self.status = SessionStream.CONNECTING
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.ios = IOStream(sock, self.io_loop)
        self.ios.set_close_callback(self._ios_closed)
        self.address = address
        self.clear_buffer()
        self.add_timer(self._connect_timeout, self.connect_time, "connect")
        self.ios.connect(address, self._connected)

    def _connected(self):
        self.status = SessionStream.CONNECTED
        self.protocol.connected(self)
        self.remove_timer("connect")
        self.ios.read_until_close(self._disconnected, self._receiver)

    def _connect_timeout(self):
        self.remove_timer("connect")
        self.status = SessionStream.IDLE
        self.ios.close()
        if self.auto_reconnect:
            self.add_timer(self._do_reconnect, self.reconnect_time, "reconnect")

    def _ios_closed(self):
        if self.status == SessionStream.CONNECTING:
            self.remove_timer("connect")
        if self.auto_reconnect:
            self.add_timer(self._do_reconnect, self.reconnect_time, "reconnect")

    def _do_reconnect(self):
        self.remove_timer("reconnect")
        self.connect(self.address)


class Server(Session):
    def __init__(self, protocol, io_loop=None, sock=None):
        Session.__init__(self, protocol, io_loop)
        self.is_server = True
        if sock is not None:
            self._setup(sock)

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
        if fd != self.sock.fileno():
            print "panic: fd != sock.fileno() ...."
            return
        conn, address = self.sock.accept()
        if self.status == SessionStream.LISTENING:
            self._setup(conn)
        elif self.status == SessionStream.CONNECTED:
            logging.warning( "already connected ...")
            conn.close()

    def _setup(self, conn):
        self.ios = IOStream(conn, self.io_loop)
        self.status = SessionStream.CONNECTED
        self.protocol.connected(self)
        self.ios.set_close_callback(self._ios_closed)
        self.ios.read_until_close(self._disconnected, self._receiver)
        
    def close(self):
        logging.debug("Server.close() called...")
        if self.ios is not None:
            self.ios.close()
        self.io_loop.remove_handler(self.sock.fileno())
        if self.sock is not None:
            self.sock.close()
        self.status = SessionStream.IDLE

    def _disconnected(self, data):
        logging.info("client disconnected ... ")
        self.protocol.disconnected(self)
        self.clear_buffer()
        self.clear_timers()
        self.ios.close()
        self.status = SessionStream.LISTENING
        logging.debug("end of client disconnect ...")

    def _ios_closed(self):
        self.status = SessionStream.LISTENING





class _Subprocess(object):
    
    def __init__(self, target, socket, config):
        self.target = target
        self.socket = socket
        self.running = False
        self.config = config
        self.init = getattr(self.target, 'setup', None)
        self.finish = getattr(self.target, 'finish', None)
        if hasattr(self.target, 'handle'):
            self.handler = getattr(self.target, 'handle')
        else:
            self.handler = target
        if not callable(self.handler):
            raise NotImplementedError('handle')
        self.io_loop = None

    def run(self):
        """Run the application data receiving loop.

        This is executed in the subprocess context.
        """
        signal.signal(signal.SIGTERM, self.sigterm)
        logging.debug("starting subprocess in pid: %d [fd %d]",
                      os.getpid(), self.socket.fileno())

        # close extra files descriptor from master, [3 -> fileno(self.socket)-1]
        os.closerange(3, self.socket.fileno())

        self.io_loop = IOLoop()
        self.ios = IOStream(self.socket, self.io_loop)
        if callable(self.init):
            self.init(self._writer, self.config)
        self.running = True
        self.ios.read_until('\r\n', self._receiver)
        try:
            self.io_loop.start()
        except (IOError, KeyboardInterrupt), ex:
            pass
        except Exception, e:
            logging.error("Subprocess recv failed: %s", str(e))

        if callable(self.finish):
            self.finish(self._writer)
        self.io_loop.close(all_fds=True)

    def _writer(self, data):
        self.ios.write(binascii.b2a_base64(json.dumps(data))+'\r\n')

    def _receiver(self, data):
        """Received data from session.(master process)"""
        msg = json.loads(binascii.a2b_base64(data))
        self.handler(msg, self._writer)

    def sigterm(self, signum, frame):
        logging.info("SIGTERM caught; terminating ...")
        self.running = False
        self.io_loop.stop()


class SubProcessApplication(Application):
    """Run application class in subprocess."""

    def __init__(self, target, io_loop=None):
        Application.__init__(self)
        if isinstance(target, str):
            self.target = self._load_module(target)
        else:
            self.target = target
        if io_loop is None:
            self.io_loop = IOLoop().instance()
        else:
            self.io_loop = io_loop
        self._process = None
        self.socket = None
        self.runner = None

    def start(self, config):
        signal.signal(signal.SIGCHLD, self._sigchld)
        self.socket, child = socket.socketpair()
        self.runner = _Subprocess(self.target, child, config)
        self._process = multiprocessing.Process(target=self.runner.run)
        self._process.start()
        child.close()
        self.ios = IOStream(self.socket, self.io_loop)
        self.ios.read_until('\r\n', self._receiver)

    def _close(self, timeout):
        self._process.join(timeout)

    def _sigchld(self, signum, frame):
        self._close(0.5)

    def _receiver(self, data):
        """Receive data from subprocess. Forward to session."""
        msg = json.loads(binascii.a2b_base64(data))
        if self.session:
            self.session.send(msg)
        else:
            logging.error("from app: %s", str(msg))

    def stop(self):
        self._process.terminate()
        self._close(2.0)

    def send(self, data):
        """Send data to application."""
        self.ios.write(data + '\r\n')

    def received(self, data):
        """Handle data from session. Forward to subprocess for handling."""
        self.send(binascii.b2a_base64(json.dumps(data)))
        return True

    def _load_module(self, modulename):
        import importlib
        return importlib.import_module(modulename)



if __name__ == "__main__":
    import sys
    from testing import LineProtocol

    class Echo(Application):
        def received(self, message):
            if self.session:
                session.send(message)

    if len(sys.argv) > 1:
        is_server = sys.argv[1] == 'server'
    else:
        is_server = False

    io_loop = IOLoop.instance()
    if is_server:
        print "starting server ..."
        session = Server(LineProtocol(), io_loop)
    else:
        print "starting client ..."
        session = Client(LineProtocol(), io_loop)
    app = Echo()
    app.set_session(session)
    session.set_application(app)
    if is_server:
        session.listen(("", 8810))
    else:
        session.connect(("localhost", 8810))
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
    except Exception, e:
        print str(e)

