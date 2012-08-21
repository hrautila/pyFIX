#
# Copyright (c) Harri Rautila, 2012
#
# This file is part of pyFIX library. It is free software, distributed
# under the terms of the GNU Lesser General Public License Version 3,
# or any later version.
#
# See the COPYING file included in this archive


import logging
import json
import functools

from traceback import print_exc
from datetime import datetime
from time import time

import pyfix.exc as exc
from pyfix.interfaces import Protocol
from message import FixMessage
from headerfields import *

def utc_timestamp(milsecs=False):
    if milsecs:
        return datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
    return datetime.utcnow().strftime('%Y%m%d-%H:%M:%S')

def datetime_now():
    return datetime.now().strftime('%Y%m%d-%H:%M:%S')

def utc_today():
    return datetime.utcnow().strftime('%Y%m%d')

def utc_now():
    return datetime.utcnow().strftime('%H:%M:%S')


def fix_message_as_list(data):
    return filter(None, data.split(chr(1)))


class FixState(object):

    INIT = 0
    LOGIN_SENT = 1
    LOGIN_WAIT = 2
    IN_SESSION = 3

    NORMAL = 10
    RESEND_REQUESTED = 11
    RESEND_RECEIVED = 12
    GAPFILL = 13
    LOGOUT_SENT = 14

    def __init__(self, store_url=''):
        self.receive_seqno = 1
        self.send_seqno = 1
        self.logon_count = 0
        self.recv_state = FixState.INIT
        self.send_state = FixState.INIT
        self.status = FixState.INIT
        self.hb_count = 0
        self.resend_seqno = 0
        self.testrq_queue = []
        self.mstore = None
        if store_url:
            self.mstore = open_store(store_url)

    def __str__(self):
        return "status=%d [l=%d]: r=%d, s=%d" % \
            (self.status, self.logon_count, self.receive_seqno, self.send_seqno)

    def save(self, path):
        if not path:
            return

        state = {'receive_seqno': self.receive_seqno,
                 'send_seqno': self.send_seqno}
        try:
            with open(path, 'w+') as fp:
                fp.write(json.dumps(state))
                fp.flush()
        except Exception, e:
            logging.error("saving state failed: %s", str(e))
            
    def restore(self, path):
        if not path:
            return
        try:
            with open(path, 'r+') as fp:
                s = fp.read(10240)
                state = json.loads(s)
        except Exception, e:
            logging.error("restoring state failed: %s", str(e))
            return
        self.receive_seqno = state['receive_seqno']
        self.send_seqno = state['send_seqno']

    def store(self, num, msg):
        if self.mstore is not None:
            self.mstore.save(num, msg)
    
    def find(self, num):
        if self.mstore is not None:
            return self.mstore.find(num)
        return -1, None
        
    def find_next(self, num):
        if self.mstore is not None:
            return self.mstore.next(num)
        return -1, None

    def log(self, msg, outbound):
        pass


class FixProtocol(Protocol):
    """Simple Fix Protocol state machine.
    
    Session configuration  parameters:

    sender_comp_id
        Sender id as per FIX spec
    target_comp_id 
        Target id as per FIX spec
    heartbeat_interval
        Heartbeat message send interval in seconds. Value 0 indicates
        that messages are not sent at all.
    reset_seqno
        Reset sequence number on logon.
    reset_seqno_only_on_first
        Reset sequence number only on first login.
    forward_login
        Forward LOGIN message to application. Normally administrative
        messages (except REJECT) are not forwarded to application.
    resend_mode
        How to request resend, GAPFILL or not.
    session_save_interval
        Interval in seconds for saving session state. Value <0 disallows saving.
        Value 0 means save after each message.
    session_save_path
        Path to save sesssion state.
    """
    def __init__(self, version='4.4'):
        Protocol.__init__(self)
        self.version = version


    def parser(self, data):
        lines = []
        c_x = 0
        while True:
            # find start of header tag
            h_start = data.find('8=FIX', c_x)
            if h_start == -1:
                break

            # find start of checksum tag
            c_start = data.find('\x0110=', c_x)
            if c_start == -1:
                break

            # scan forward to next SOH
            try:
                c_end = c_start + 3
                while ord(data[c_end]) != 1:
                    c_end += 1
                lines.append(data[h_start:c_end+1])
                c_x = c_end + 1
            except IndexError, e:
                break

        # return full messages and rest of data
        return lines, data[c_x:]

    def transmit(self, session, data):
        """Split message to header and body. Rebuild header and send."""
        hdr, body = data.split_message()
        # remove prefix, length and type
        hdr.delete(8)
        hdr.delete(9)
        msgtype = hdr.get(35)
        hdr.delete(35)
        # delete TARGET_COMP_ID, SENDER_COMP_ID
        self._transmit(session, msgtype, body, options=hdr, admin=False)

    def validate(self, raw_data):
        """Convert from raw to internal FixMessage and validate it."""
        data = FixMessage.from_raw(raw_data)
        if not data.validate():
            logging.warning("disgarding message: %s", data)
            return None
        
        if data[0].find(self.version) == -1:
            # first contains wrong version number
            raise exc.SessionError, (exc.S_EVERSION)

        return data
        
    def connected(self, session):
        state = session.state
        if state.status != FixState.INIT:
            logging.warning("Connection created with status != INIT [%d]", state.status)
        state.status = FixState.LOGIN_WAIT
        if not session.is_server:
            self.send_login(session)
        callback = functools.partial(self._logon_timeout, session)
        session.add_timer(callback, 10, "logon")
        logging.debug("connected end state: %s", str(state))

    def disconnected(self, session):
        state = session.state
        state.status = FixState.INIT
        logging.debug("disconnected end state: %s", str(state))
        session.clear_timers()
        #session.close()

    def received(self, session, raw_data):
        """Handle received FIX message."""

        data = self.validate(raw_data)
        if data is None:
            return

        state = session.state
        if state.status == FixState.LOGIN_WAIT:
            return self.login_auth(session, data)

        msgtype = data.get(FLD_MSG_TYPE)
        seqno = data.get(FLD_MSG_SEQNUM, int)

        request_resend = False
        logging.debug("next expected seqno: %d, msg seqno: %d, state: %d",
                       state.receive_seqno, seqno, state.status)
        
        logging.debug(" IN: %s", str(data))
        posdup_flag = data.get(FLD_POSS_DUPFLAG)

        # at this point receive_seqno should be equal
        if seqno < state.receive_seqno:
            logging.error('excepted [%d] >  [%d] message: poss_dup=%s',
                           state.receive_seqno, seqno, posdup_flag)

            # if not 'possibly duplicate' then fail the session
            if posdup_flag != 'Y':
                raise exc.SessionError, (exc.S_ESEQNO,
                                   "Expected seqno %d higher that received seqno %d" %
                                   (state.receive_seqno, seqno))

        elif seqno > state.receive_seqno:
            logging.error('excepted [%d] <  [%d] message: missing messages',
                           state.receive_seqno, seqno)
            request_resend = True
            
        if msgtype not in ADMIN_MSGTYPES:
            session.received(data)
            if posdup_flag != 'Y':
                state.receive_seqno += 1
        else:
            self.handle_admin(session, msgtype, seqno, data)

        if request_resend:
            self.request_resend(session, state.receive_seqno+1, seqno)

        savesecs = int(session.get_conf('session_save_interval', -1))
        if savesecs == 0:
            session.state.save(session.get_conf('session_save_path'))

    def login_auth(self, session, data):
        """Verify login."""

        session.remove_timer("logon")
        state = session.state
        msgtype = data.get(FLD_MSG_TYPE, str)
        seqno = data.get(FLD_MSG_SEQNUM, int)

        # waiting for Logon response message
        if msgtype == MSG_LOGOUT:
            msg = data.get(58)
            logging.error("received LOGOUT: %s", msg)
            raise exc.SessionError, (exc.S_EINMESSAGE, msg)
 
        elif msgtype != MSG_LOGON:
            logging.error("received %s message in LOGIN state", msgtype)
            raise exc.SessionError, (exc.S_EINMESSAGE)

        if seqno != state.receive_seqno:
            if seqno > state.receive_seqno:
                logging.warning('LOGON: excepted [%d] <  [%d] message: missing seqnos',
                                state.receive_seqno, seqno)
                state.recv_state = FixState.RESEND_REQUESTED
                state.send_state = FixState.NORMAL
                state.resend_seqno = seqno
                #self.request_resend(state.receive_seqno+1, 0)
            else:
                # unexpected seqno for login (message seqno < receive_seqno)
                logging.error('LOGON: excepted [%d] >  [%d] message: failing ...',
                              state.receive_seqno, seqno)
                raise exc.SessionError, (exc.S_ESEQNO)

        if not session.is_server:
            # client part when all OK
            #state.receive_seqno = seqno
            #logging.debug("set last received seqno to %d", state.receive_seqno)
            state.status = FixState.IN_SESSION
            # per FIX protocol send TestRequest after successfull Logon
            if state.recv_state != FixState.RESEND_REQUESTED:
                self.send_testrequest(session)

        elif session.is_server:
            # server part when all OK
            logging.debug("Creating LOGON reply ...")
            # reply
            clnt_hb = data.get(FLD_HEARTBEAT_INT, int)
            session.set_conf('heartbeat_interval', clnt_hb)

            lg = FixMessage()
            lg.set(FLD_HEARTBEAT_INT, clnt_hb)
            reset_flag = data.get(FLD_RESET_SEQNUM_FLAG)
            if reset_flag == 'Y':
                loggging.warning("Reseting sequence numbers at logon (r=%d, s=%d)",
                                 state.receive_seqno, state.send_seqno)
                lg.set(FLD_RESET_SEQNUM_FLAG, 'Y')
                state.send_seqno = 1
                state.receive_seqno = 1
            lg.set(FLD_ENCRYPT_METHOD, 0)
            state.status = FixState.IN_SESSION
            self._transmit(session, MSG_LOGON, lg, admin=True)

        # test if resend request need to be sent 
        if state.recv_state == FixState.RESEND_REQUESTED:
            self.request_resend(session, state.receive_seqno, 0)
        else:
            state.receive_seqno += 1

        state.logon_count += 1
        state.hb_count = 0

        # check if login messages forwarded...
        if session.get_conf("forward_logon", True):
            session.received(data)
            
        save_secs = int(session.get_conf('session_save_interval', -1))
        if save_secs > 0:
            callback = functools.partial(state.save,
                                         session.get_conf('session_save_path', ''))
            session.add_periodic(callback, save_secs, "session_saver")
        elif save_secs == 0:
            session.state.save(session.get_conf('session_save_path'))

        logging.debug("end of LOGIN sequence: %s", str(state))
        return True

    def send_login(self, session):
        """Send client login data to transport."""
        state = session.state
        hb_secs = int(session.get_conf('heartbeat_interval', 30))
        reset = session.get_conf('reset_seqno', False)
        reset_only_on_first = session.get_conf('reset_seqno_only_on_first', True)
        if reset:
            reset_seqno = (state.logon_count == 0 and reset_only_on_first) or \
                (not reset_only_on_first)
        else:
            reset_seqno = False

        lg = FixMessage()
        lg.set(FLD_HEARTBEAT_INT, hb_secs)
        lg.set(FLD_ENCRYPT_METHOD, 0)
        if reset_seqno:
            lg.set(FLD_RESET_SEQNUM_FLAG, 'Y')
            logging.warning("Reseting sequence numbers at logon (r=%d, s=%d)",
                             state.receive_seqno, state.send_seqno)
            if state.send_seqno > 1:
                state.send_seqno = 1
            if state.receive_seqno > 1:
                state.receive_seqno = 1
        self._transmit(session, MSG_LOGON, lg, admin=True)

    def handle_admin(self, session, msgtype, seqno, data):
        """Handle FIX administrative messages."""
        
        logging.debug("Administrative message %s [%d] received", msgtype, seqno)

        state = session.state
        if msgtype == MSG_REJECT:
            session.received(data)
            state.receive_seqno += 1

        elif msgtype == MSG_TEST_REQUEST:
            test_id = data.get(FLD_TESTREQ_ID)
            logging.info("TestRequest received: %s", test_id)
            hb = FixMessage()
            hb.set(FLD_TESTREQ_ID, test_id)
            self._transmit(session, MSG_HEARTBEAT, hb, admin=True)
            state.receive_seqno += 1

        elif msgtype == MSG_HEARTBEAT:
            logging.info("Heartbeat received [%d]", seqno)
            state.receive_seqno += 1
            state.hb_count = 0
            try:
                reqid = data.get(FLD_TESTREQ_ID)
                logging.debug("Response test request: %s [ql=%d]",
                              reqid, len(state.testrq_queue))
                if reqid == state.testrq_queue[0]:
                    state.testrq_queue.pop(0)
            except:
                pass

        elif msgtype == MSG_RESEND_REQUEST:
            begin_seqno = data.get(FLD_BEGIN_SEQNO, int)
            end_seqno = data.get(FLD_END_SEQNO, int)
            logging.info("ResendRequest received [%d, %d]", begin_seqno, end_seqno)
            self.resend(session, begin_seqno, end_seqno)
            state.receive_seqno += 1

        elif msgtype == MSG_SEQUENCE_RESET:
            logging.debug("received SequenceReset: %s", str(data))
            state.receive_seqno += 1
            gap_fill = data.get(FLD_GAPFILL_FLAG)
            new_seqno = data.get(FLD_NEW_SEQNO, int)
            logging.info("SequenceReset, gap_fill=%s, msg_seqno=%d, new_seqno=%d",
                             gap_fill, seqno, new_seqno)
            if gap_fill == 'Y':
                logging.warning("GapFill: reset last received seqno to %d", new_seqno)
                state.receive_seqno = new_seqno 
            else:
                logging.warning("Reset: reset last receive seqno to %d", new_seqno)
                state.receive_seqno = new_seqno 
                
        elif msgtype == MSG_LOGOUT:
            # this propably happens mostly on server side
            logging.info("Logout received")
            session.received(data)
            state.receive_seqno += 1
            session.close()

        else:
            logging.warning("Unknown admin message type: %s", msgtype)

                
    def resend(self, session, start, end):
        """Resend message as for ResendRequest"""
        state = session.state
        logging.info("handling resend from %d to %d", start, end)
        state.send_state = FixState.RESEND_RECEIVED
        resend_mode = session.get_conf('resend_mode', 'GAPFILL')
        opts = FixMessage()
        if resend_mode == 'GAPFILL' or resend_mode == 'BUYSIDE':
            logging.info("sending SequeceReset-GapFill: next seqno = %d", state.send_seqno+1)
            opts.set(FLD_POSS_DUPFLAG, 'Y')
            opts.set(FLD_ORIG_SENDING_TIME, utc_timestamp())
            opts.set(FLD_MSG_SEQNUM, start)
            mg = FixMessage()
            mg.set(FLD_GAPFILL_FLAG, 'Y')
            mg.set(FLD_NEW_SEQNO, state.send_seqno+1)
            self._transmit(session, MSG_SEQUENCE_RESET, mg, options=opts, admin=True)
        elif resend_mode == 'RESET':
            logging.info("sending SequeceReset-Reset")
            mg = FixMessage()
            # initialize to seqno after this message (seqno is last sent seqno)
            mg.set(FLD_NEW_SEQNO, state.send_seqno+1)
            self._transmit(session, MSG_SEQUENCE_RESET, mg, options=opts, admin=True)
        elif resend_mode:
            logging.warning("unknown resend_mode: %s", resend_mode)

    def request_resend(self, session, start, end):
        """Send  ResendRequest message"""
        state = session.state
        logging.info("request resend from %d to %d", start, end)
        mg = FixMessage()
        mg.set(FLD_BEGIN_SEQNO, start)
        mg.set(FLD_END_SEQNO, end)
        state.recv_state = FixState.RESEND_REQUESTED
        self._transmit(session, MSG_RESEND_REQUEST, mg, admin=True)
            
    def send_hb(self, session):
        """Send heartbeat to transport."""
        hb = FixMessage()
        self._transmit(session, MSG_HEARTBEAT, hb, admin=True)

    def send_testrequest(self, session):
        """Send FIX TestRequest message"""

        state = session.state
        if state.testrq_queue:
            # Do not send if pending test requests
            return
        rqid = datetime_now()
        rq = FixMessage()
        rq.set(FLD_TESTREQ_ID, rqid)
        state.testrq_queue.append(rqid)
        logging.debug("Sending test request: %s", rqid)
        self._transmit(session, MSG_TEST_REQUEST, rq)

    def send_heartbeat(self, session):
        """Send FIX Heatbeat message."""
        logging.debug("Sending heartbeat")
        self._transmit(session, MSG_HEARTBEAT, FixMessage(), admin=True)

    def timeout(self, session):
        logging.debug("heartbeat timeout")
        # count heartbeats
        session.state.hb_count += 1
        self.send_heartbeat(session)

    def _logon_timeout(self, session):
        logging.debug("session logon timeout.")
        session.remove_timer("logon")
        session.close()

    def _next_header(self, session, options=None):
        """Provide next FIX message header."""

        state = session.state
        header = FixMessage()

        header.set(FLD_SENDER_COMP_ID, session.get_conf('sender_comp_id'))
        header.set(FLD_TARGET_COMP_ID, session.get_conf('target_comp_id'))
        if options is None:
            header.set(FLD_MSG_SEQNUM, state.send_seqno)
        else:
            if options.get(FLD_MSG_SEQNUM, int) is None:
                header.set(FLD_MSG_SEQNUM, state.send_seqno)
            # merge options
            header.join(options)

        header.set(FLD_SENDING_TIME, utc_timestamp())
        return header

    def _transmit(self, session, msgname, msg, options=None, admin=False):
        """Transmit data. Add headers and log message."""

        session.remove_timer("heartbeat")
        state = session.state
        data = self._next_header(session, options)
            
        data.extend(msg)
        data.set_prefix(self.version, msgname)
        
        if not admin:
            state.store(state.send_seqno, data)
        logging.debug("OUT: %s", str(data))
        # translate to wire format and push out to session
        state.send_seqno += 1
        self._transmit_internal(session, data)
        
    def _transmit_internal(self, session, data):
        """Handle data going to transport."""
        raw_data = data.to_raw()
        hbsec = int(session.get_conf('heartbeat_interval', 30))
        if session.state.status == FixState.IN_SESSION and hbsec > 0:
            logging.debug("Add heartbeat timer %d sec", hbsec)
            callback = functools.partial(self.timeout, session)
            session.add_timer(callback, hbsec, "heartbeat")
        session.transmit(raw_data)
        savesecs = int(session.get_conf('session_save_interval', -1))
        logging.debug("saving state data ... %s", str(savesecs==0))
        if savesecs == 0:
            session.state.save(session.get_conf('session_save_path'))



