
from interfaces import Protocol

class LineProtocol(Protocol):
    """Simple line protocol with message terminated with new-lines."""

    IDLE = 1
    LOGIN_WAIT = 2
    IN_SESSION = 3

    def __init__(self, no_login=False):
        Protocol.__init__(self)
        self.state = LineProtocol.IDLE
        self.no_login = no_login

    def connected(self, session):
        if no_login:
            self.state = LineProtocol.IN_SESSION
        else:
            self.state = LineProtocol.LOGIN_WAIT
            if not session.is_server:
                self._send_login(session)
            session.add_timer(functools.partial(self.timeout, session), 5, "login")

    def disconnected(self, session):
        if self.state == LineProtocol.LOGIN_WAIT:
            session.remove_timer("login")
        self.state = LineProtocol.IDLE

    def received(self, session, data):
        """Handle data coming from transport."""
        if self.state == LineProtocol.IN_SESSION:
            session.received(data)
        elif self.state == LineProtocol.LOGIN_WAIT:
            session.remove_timer("login")
            if not self._login_auth(session, data):
                print "login failed! state=%d, data='%s'" % (session.is_server, data)
                session.close()
                self.state = LineProtocol.IDLE
            else:
                self.state = LineProtocol.IN_SESSION
        else:
            print "message received in unexpected state"

    def transmit(self, session, message):
        """Add newlien to ``message`` and forward to ``session``."""
        session.transmit(message + '\n')

    def timeout(self, session):
        if self.state == LineProtocol.LOGIN_WAIT:
            session.remove_timer("login")
        session.close()
        self.state = LineProtocol.IDLE

    def parser(self, data):
        """Split incoming data to complete messages."""
        lines = data.replace('\r', '').split('\n')
        rem = lines.pop(-1)
        return lines, rem
    
    def validate(self, data):
        if len(data) > 0 and data[0].isupper():
            return data
        return None

    def _login_auth(self, session, data):
        """Verify login."""
        if not session.is_server:
            if data == 'OK':
                return True
        if session.is_server:
            if data == 'LOGIN':
                self.transmit('OK')
                return True
        return False

    def _send_login(self, session):
        """Send login data to transport."""
        self.transmit(session, "LOGIN")

