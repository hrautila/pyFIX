
import logging

from tornado.ioloop import IOLoop
from pyfix.fix import FixProtocol, FixState, FixMessage
from pyfix.tornadoio import Client, Server, SubProcessApplication

def main():
    import optparse
    from pyfix.util import read_config_section, parse_address

    parser = optparse.OptionParser(
        usage='%prog [OPTIONS] CONFIGFILE')

    parser.add_option('-F', '--fix-name', default='fixsession',
                      help='FIX config section name')
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

    app_config = read_config_section(config_path, options.app_name)
    if not app_config:
        logging.error("empty APPLICATION config section %s", options.app_name)
        sys.exit(2)

    appname = app_config.get('application_module', '')
    if not appname:
        logging.error("no application module defined!!")
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
    

    fixapp = SubProcessApplication(appname, io_loop=io_loop)
    fixapp.start(app_config)
    fixapp.set_session(session)
    session.set_application(fixapp)

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
