#!/usr/bin/env python
#
# (c) Harri Rautila, 2012
#
# This file is part of pyFIX library. It is free software, distributed
# under the terms of the GNU Lesser General Public License Version 3,
# or any later version.
#
# See the COPYING file included in this archive


class SessionStream(object):

    IDLE = 0
    CONNECTING = 1
    LISTENING = 2
    CONNECTED = 3

    def __init__(self, proto):
        self.is_server = False
        self.state = None
        self.protocol = proto
        self.application = None
        self.status = SessionStream.IDLE
        self._config = {}

    def set_application(self, app):
        """Connect application."""
        self.application = app

    def clear_buffer(self):
        "Clear I/O buffer."""
        pass

    def get_conf(self, name, defval=None):
        """Get configuration parameter."""
        return self._config.get(name, defval)
    
    def set_conf(self, name, val):
        """Set configuration parameter."""
        self._config[name] = val

    def update_conf(self, dct):
        """Update configuration from dictionary."""
        for k, v in dct.items():
            self._config[k] = v

    def connect(self, address):
        """Connect to address."""
        pass

    def listen(self, address):
        """Listen on address."""
        pass

    def accept(self):
        """Accept client connection."""
        pass

    def bind(self, address):
        """Bind to network address."""
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def transmit(self, data):
        """Write protocol message to stream."""
        pass

    def received(self, message):
        """Forward application message from protocol level."""
        if self.application:
            return application.received(message)
        # could not forward message
        return False

    def send(self, message):
        """Forward application message to proto."""
        self.protocol.transmit(self, message)

    def close(self):
        self.status = SessionStream.IDLE
        
    def add_timer(self, callback,  secs, name):
        """Add named timer."""
        pass

    def remove_timer(self, name):
        """Remove named timer."""
        pass



class Protocol(object):
    """Protocol defines simple interface for session protocol.
    """
    def __str__(self):
        return self.__class__.__name__

    def connected(self, session):
        """Called when session is connected."""
        pass

    def disconnected(self, session):
        """Called when session is disconnected."""
        pass

    def received(self, session, data):
        """Receive protocol message and handle it.

        Called by session receiver to process messages.
        """
        session.received(data)

    def transmit(self, session, message):
        """Tranlate message to line format and forward to session."""
        session.transmit(message)

    def parser(self, data):
        """Parses data to message records.
        
        Returns list of messages and unused part of data
        """
        return [data], ''

class Application(object):
    def __init__(self):
        self.session = None

    def set_session(self, session):
        self.session = session

    def received(self, message):
        return False

    def send(self, message):
        self.session.send(message)

    def start(self, config):
        pass

    def stop(self):
        pass

class State(object):
    """Session state interface."""
    def save(self, path):
        pass

    def restore(self, path):
        pass


