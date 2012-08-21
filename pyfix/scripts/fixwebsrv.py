
import sys
import json
import logging

import tornado.web
from tornado.ioloop import IOLoop

import pyfix
from pyfix.fix import FixProtocol, FixState, FixMessage
from pyfix.tornadoio import Client

class SessionManageRequestHandler(tornado.web.RequestHandler):
    def initialize(self, session, config):
        self.session = session
        self.config = config


class FixRequestHandler(tornado.web.RequestHandler):
    def initialize(self, fixapp, config):
        self.fixapp = fixapp
        self.config = config
        
    def get(self, *args, **kwargs):
        logging.debug("GET Request: %s", str(self.request))
        m = self.fixapp.dequeue()
        if m:
            self.set_status(200)
            data = json.dumps(m)
            self.write(data)
        else:
            self.set_status(401)
            

    def post(self, *args, **kwargs):
        logging.debug("POST Request: %s", str(self.request))
        data = self.request.body
        try:
            logging.debug("convert data: %s %s", type(data), str(data))
            m = json.loads(data)
            # encode elements to str and create FixMessage
            fixm = FixMessage(map(lambda x: str(x), m))
            self.fixapp.send(fixm)
            self.set_status(200)
        except Exception, e:
            logging.error("post: %s", str(e))
            self.set_status(501)


class HTTPtoFIXApplication(pyfix.Application):
    def start(self, config):
        self.config = config
        self.mqueue = []

    def received(self, message):
        self.mqueue.append(message)
        return True
    
    def send(self, message):
        self.session.send(message)

    def dequeue(self):
        if self.mqueue:
            return self.mqueue.pop(0)


def main():

    import optparse
    from pyfix.util import read_config_section, parse_address

    parser = optparse.OptionParser(
        usage='%prog [OPTIONS] CONFIGFILE')

    parser.add_option('-F', '--fix-name', default='fixsession',
                      help='FIX config section name')
    parser.add_option('-H', '--http-name', default='http',
                      help='HTTP config section name')
    parser.add_option('-A', '--app-name', default='application',
                      help='APPLICATION config section name')
    parser.add_option('-L', '--log-level', default='INFO',
                      help='Logging level name DEBUG|INFO|WARN|ERROR')

    options, args = parser.parse_args()
    if not args or len(args) > 1:
        parser.print_help()
        sys.exit(2)

    config_path = args[0]

    loglevel = getattr(logging, options.log_level.upper(), None)
    if loglevel is None:
        loglevel = logging.INFO

    logging.basicConfig(level=loglevel)
    address = ('localhost', 4321)

    session_config = read_config_section(config_path, options.fix_name)
    if not session_config:
        logging.error("empty FIX config section %s", options.fix_name)
        sys.exit(2)

    http_config = read_config_section(config_path, options.http_name)
    if not http_config:
        logging.error("empty HTTP config section %s", options.http_name)
        sys.exit(2)

    app_config = read_config_section(config_path, options.app_name)
    if not app_config:
        logging.error("empty APPLICATION config section %s", options.app_name)
        sys.exit(2)

    address_url = session_config.get('address', '')
    session_type = session_config.get('session_type', 'client').lower()
    if not address_url:
        logging.error("no address defined in FIX config section.")
        sys.exit(2)

    host, port, scheme = parse_address(address_url)
        
    io_loop = IOLoop.instance()
    if session_type == 'client':
        session = Client(FixProtocol(), io_loop=io_loop)
    else:
        session = Server(FixProtocol(), io_loop=io_loop)

    session.update_conf(session_config)
    session.state = FixState()
    if session.get_conf('session_save_path'):
        session.state.restore(session.get_conf('session_save_path'))
    

    fixapp = HTTPtoFIXApplication()
    fixapp.start(app_config)
    fixapp.set_session(session)
    session.set_application(fixapp)

    # create HTTP interfaces
    http_port = int(http_config.get('port', 7030))
    handler_path = http_config.get('handler_path', '/session')
    applist = []
    applist.append(
        (handler_path, FixRequestHandler, dict(fixapp=fixapp, config=http_config))
        )
    mgmt_path = http_config.get('session_manage_path', '')
    if mgmt_path:
        applist.append(
            (mgmt_path, ManageHandler, dict(session=session, config=http_config))
            )
    tornado_app = tornado.web.Application(applist)

    tornado_app.listen(http_port)
    if session_type == 'client':
        session.connect((host, port))
    else:
        session.listen((host, port))

    try:
        io_loop.start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

