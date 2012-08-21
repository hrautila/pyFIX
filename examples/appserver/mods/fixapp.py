
import logging

import pyfix.fix.fix42 as fix
from pyfix.fix import FixMessage, FixContext

appconf = None
fixctx = None

def setup(writer, config):
    appconf = config
    fixctx = FixContext(version='4.2')
    logging.info("app setup executed ...")

def handle(data, writer):
    logging.info("app received: %s", str(data))
    msg, hdr = FixObject.from_message(data, fixctx)
    if isinstance(msg, fix.Logon):
        print "Logon received ..."
                 

def finish(writer):
    logging.info("app finish executed ...")
