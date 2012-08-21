if __name__ == "__main__":
    import sys
    import logging
    from tornado.ioloop import IOLoop
    from pyfix.tornadoio import Client, Server
    from pyfix.fix import FixProtocol, FixState

    class Sink(object):
        def set_session(self, ses):
            pass

        def received(self, message):
            print str(message)

    if len(sys.argv) > 1:
        is_server = sys.argv[1] == 'server'
    else:
        is_server = False


    logging.basicConfig(level=logging.DEBUG)
    io_loop = IOLoop.instance()
    if is_server:
        print "starting server ..."
        fix_config = {'sender_comp_id': 'BSIDE',
                      'target_comp_id': 'ASIDE',
                      'heartbeat_interval': 30,
                      }
        session = Server(FixProtocol(), io_loop)
    else:
        print "starting client ..."
        fix_config = {'sender_comp_id': 'ASIDE',
                      'target_comp_id': 'BSIDE',
                      'heartbeat_interval': 30,
                      }
        session = Client(FixProtocol(), io_loop)

    session.update_conf(fix_config)
    session.state = FixState()
    app = Sink()
    app.set_session(session)
    session.set_application(app)
    if is_server:
        session.listen(("", 8810))
    else:
        session.connect(("localhost", 4321))
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
    except Exception, e:
        print str(e)
