# Copyright (c) Harri Rautila, 2011

# This file is part of sxsuite library. It is free software, distributed
# under the terms of the GNU Lesser General Public License Version 3,
# or any later version.
# See the COPYING file included in this archive

import logging
import json

from traceback import print_exc
from datetime import datetime
from time import time

import sxsuite.exc as exc
from sxsuite.exc import SessionError, TransportError
from sxsuite.session import TCPSession
from sxsuite.protocol import SessionProtocol
from sxsuite.store import open_store
from sxsuite.fix.message import *

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
    NORMAL = 1
    LOGIN_SENT = 1
    LOGIN_WAIT = 2
    RESEND_REQUESTED = 3
    RESEND_RECEIVED = 4
    GAPFILL = 5
    LOGOUT_SENT = 6

    def __init__(self, store_url):
        self.receive_seqno = 0
        self.send_seqno = 0
        self.recv_state = FixState.INIT
        self.send_state = FixState.INIT
        self.resend_seqno = 0
        self.testrq_queue = []
        self.mstore = None
        if store_url:
            self.mstore = open_store(store_url)

    def save(self, path):
        state = {'receive_seqno': self.receive_seqno,
                 'send_seqno': self.send_seqno}
        try:
            with open(path, 'w+') as fp:
                fp.write(json.dumps(state))
                fp.flush()
        except Exception, e:
            logging.error("saving state failed: %s", str(e))
            
    def restore(self, path):
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

class FixSession(TCPSession):
    def __init__(self, reaktor, protocol, name='', server=False, 
                 transport=None, state_path='', store_url=''):
        TCPSession.__init__(self, reaktor, protocol, name=name,
                            transport=transport, server=server)
        self.store_url = store_url
        self.state_path = state_path
        self.state = FixState(self.store_url)

    def login_hook(self, data):
        if not self.server:
            return True

        sender_id = self.get_conf('sender_comp_id')
        target_id = self.get_conf('target_comp_id')
        m_sender = data.get_field(49)
        m_target = data.get_field(56)
        self.log.debug("msg: s=%s, t=%s, ses: s=%s, t=%s",
                       m_sender, m_target, sender_id, target_id)
        if m_target == sender_id and m_sender == target_id:
            return True
        return False

    def send(self, data):
        """Send message."""
        self.protocol.rebuild_and_transmit(data)

    def save(self, path):
        self.state.save(path)

    def restore(self, path):
        self.state.restore(path)


class FixClient(FixSession):
    def __init__(self, reaktor, protocol, name='', state_path='', store_url=''):
        FixSession.__init__(self, reaktor, protocol,
                            name=name, state_path=state_path, store_url=store_url)

class FixServer(FixSession):
    def __init__(self, reaktor, protocol, transport=None, name='', state_path='', store_url=''):
        FixSession.__init__(self, reaktor, protocol, server=True,
                            name=name, state_path=state_path, store_url=store_url)


class FixProtocol(SessionProtocol):
    def __init__(self, version='4.4', context=None):
        SessionProtocol.__init__(self)
        self.version = version
        if context:
            self.context = context
        else:
            self.context = FixContext(version=version)

    log = logging

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

    def transmit(self, data):
        """Handle data going to transport."""
        raw_data = data.to_raw()
        self.session.transmit(raw_data)

    def rebuild_and_transmit(self, data):
        """Split message to header and body. Rebuild header and send."""
        hdr, body = data.split_message(self.context)
        # remove prefix, length and type
        hdr.delete(8)
        hdr.delete(9)
        msgtype = hdr.get(35)
        hdr.delete(35)
        self._transmit(msgtype, body, options=hdr, admin=False)

    def validate(self, raw_data):
        """Convert from raw to internal FixMessage and validate it."""
        data = FixMessage.from_raw(raw_data)
        if not data.validate():
            self.log.warning("disgarding message: %s", data)
            return None
        
        if data[0].find(self.context.version) == -1:
            # first contains wrong version number
            raise SessionError, (self.session, exc.S_EVERSION)

        return data
        
    def client_auth(self, seqno, data):

        try:
            login_ok = self.session.login_hook(data)
        except Exception, e:
            print_exc()
            raise e

        if not login_ok:
            raise SessionError, (self.session, exc.S_ELOGINFAILED)

        state = self.session.state
        if seqno - state.receive_seqno != 1:
            if seqno - state.receive_seqno > 1:
                self.log.warning('LOGON: excepted [%d] <  [%d] message: missing seqnos',
                                 state.receive_seqno+1, seqno)
                state.recv_state = FixState.RESEND_REQUESTED
                state.send_state = FixState.NORMAL
                state.resend_seqno = seqno
                self.request_resend(state.receive_seqno+1, 0)
            else:
                # unexpected seqno for login (message seqno < receive_seqno)
                self.log.error('LOGON: excepted [%d] >  [%d] message: failing ...',
                               state.receive_seqno+1, seqno)
                raise SessionError, (self.session, exc.S_ESEQNO)

        else:
            state.receive_seqno = seqno
            self.log.debug("set last received seqno to %d", state.receive_seqno)
            state.send_state = FixState.NORMAL
            state.recv_state = FixState.NORMAL
            # per FIX protocol send TestRequest after successfull Logon
            self.send_testrequest()
        
        return True

    def server_auth(self, seqno, data):

        try:
            login_ok = self.session.login_hook(data)
        except Exception, e:
            print_exc()
            raise e

        if not login_ok:
            raise SessionError, (self.session, exc.S_ELOGINFAILED)
        
        state = self.session.state
        if seqno - state.receive_seqno != 1:
            if seqno - state.receive_seqno > 1:
                self.log.warning('LOGON: excepted [%d] <  [%d] message: missing seqnos',
                                 state.receive_seqno+1, seqno)
                state.recv_state = FixState.RESEND_REQUESTED
                state.send_state = FixState.NORMAL
                state.resend_seqno = seqno
            else:
                # unexpected seqno for login (message seqno < receive_seqno)
                self.log.error('LOGON: excepted [%d] >  [%d] message: failing ...',
                               state.receive_seqno+1, seqno)
                raise SessionError, (self.session, exc.S_ESEQNO)

        self.log.debug("Creating LOGON reply ...")
        # reply
        clnt_hb = data.get_field('HeartBtInt', self.context)
        self.session.set_conf('heartbeat_interval', clnt_hb)

        lg = FixMessage()
        lg.set_field('HeartBtInt', clnt_hb, self.context)
        reset_flag = data.get_field('ResetSeqNumFlag', self.context)
        if reset_flag == 'Y':
            self.log.warning("Reseting sequence numbers at logon (r=%d, s=%d)",
                             state.receive_seqno, state.send_seqno)
            lg.set_field('ResetSeqNumFlag', 'Y', self.context)
            state.send_seqno = 0
            state.receive_seqno = 0
        lg.set_field('EncryptMethod', 0, self.context)
        self._transmit('Logon', lg, admin=True)

        if state.recv_state == FixState.RESEND_REQUESTED:
            self.request_resend(state.receive_seqno+1, 0)
        else:
            state.receive_seqno += 1

        return True

    def login_auth(self, data, server=False):
        """Verify login."""

        msgtype = data.get_field('MsgType', self.context)
        seqno = data.get_field('MsgSeqNum', self.context)

        direct = self.session._direct
        if not direct:
            self.session._direct = True

        # waiting for Logon response message
        if self.context.isinstance(msgtype, Logout):
            msg = data.get(58)
            self.log.error("received LOGOUT: %s", msg)
            raise SessionError, (self.session, exc.S_EINMESSAGE, msg)

        elif not self.context.isinstance(msgtype, Logon):
            self.log.error("received %s message in LOGIN state",
                           self.context.name_for_msgtype(msgtype))
            self.session._direct = direct
            raise SessionError, (self.session, exc.S_EINMESSAGE)

        if not server:
            self.client_auth(seqno, data)
        else:
            self.server_auth(seqno, data)

        self.session._direct = direct
        self.log.debug("end of LOGIN sequence: %s", str(self))
        return True

    def send_login(self):
        """Send login data to transport."""
        hb_secs = self.session.get_conf('heartbeat_interval', 10)
        reset_seqno = self.session.get_conf('reset_seqno', False)
        lg = FixMessage()
        lg.set_field('HeartBtInt', hb_secs, self.context)
        lg.set_field('EncryptMethod', 0, self.context)
        if reset_seqno:
            lg.set_field('ResetSeqNumFlag', 'Y', self.context)
            state = self.session.state
            self.log.warning("Reseting sequence numbers at logon (r=%d, s=%d)",
                             state.receive_seqno, state.send_seqno)
            if state.send_seqno > 0:
                state.send_seqno = 0
            if state.receive_seqno > 0:
                state.receive_seqno = 0
        self._transmit('Logon', lg, admin=True)

    def send_hb(self):
        """Send heartbeat to transport."""
        hb = FixMessage()
        self._transmit('Heartbeat', hb, admin=True)

    def received(self, data, server=False):
        """Handle received FIX message."""

        msgtype = data.get_field('MsgType', self.context)
        seqno = data.get_field('MsgSeqNum', self.context)

        state = self.session.state
        request_resend = False
        self.log.debug("last received seqno: %d, msg seqno: %d, state: %d",
                       state.receive_seqno, seqno, self.session._state)
        
        self.log.debug(" IN: %s", str(data))
        posdup_flag = data.get_field('PossDupFlag', self.context)

        # at this point receive_seqno should be smaller by one
        if seqno - state.receive_seqno < 1:
            self.log.error('excepted [%d] >  [%d] message: poss_dup=%s',
                           state.receive_seqno+1, seqno, posdup_flag)

            # if not 'possibly duplicate' then fail the session
            if posdup_flag != 'Y':
                raise SessionError, (self.session, exc.S_ESEQNO,
                                   "Expected seqno %d higher that received seqno %d" %
                                   (state.receive_seqno+1, seqno))

        elif seqno - state.receive_seqno > 1:
            self.log.error('excepted [%d] <  [%d] message: missing messages',
                           state.receive_seqno+1, seqno)
            request_resend = True
            
        if self.context.msgtype_is_application(msgtype):
            self.session.received(data)
        else:
            self.handle_admin(msgtype, seqno, data, server)

        if request_resend:
            self.request_resend(state.receive_seqno+1, seqno)
        else:
            state.receive_seqno += 1


            
    def handle_admin(self, msgtype, seqno, data, server):
        """Handle FIX administrative messages."""

        state = self.session.state
        if self.context.isinstance(msgtype, Reject):
            self.session.received(data)

        elif self.context.isinstance(msgtype, TestRequest):
            test_id = data.get_field('TestReqID', self.context)
            self.log.info("TestRequest received: %s", test_id)
            hb = FixMessage()
            hb.set_field('TestReqID',test_id, self.context)
            self._transmit('Heartbeat', hb, admin=True)

        elif self.context.isinstance(msgtype, Heartbeat):
            self.log.info("Heartbeat received")
            try:
                reqid = data.get_field('TestReqID', self.context)
                if reqid == self._testrq_queue[0]:
                    self.log.debug("Response test request: %s", reqid)
                    state.testrq_queue.pop(0)
            except:
                pass
            # ??
            #self.timeout()

        elif self.context.isinstance(msgtype, ResendRequest):
            begin_seqno = data.get_field('BeginSeqNo', self.context)
            end_seqno = data.get_field('EndSeqNo', self.context)
            self.log.info("ResendRequest received [%d, %d]", begin_seqno, end_seqno)
            self.resend(begin_seqno, end_seqno)

        elif self.context.isinstance(msgtype, SequenceReset):
            self.log.debug("received SequenceReset: %s", str(data))
            gap_fill = data.get_field('GapFillFlag', self.context)
            new_seqno = data.get_field('NewSeqNo', self.context)
            self.log.info("SequenceReset, gap_fill=%s, msg_seqno=%d, new_seqno=%d",
                             gap_fill, seqno, new_seqno)
            if gap_fill == 'Y':
                self.log.warning("GapFill: reset last received seqno to %d",
                                 new_seqno)
                state.receive_seqno = new_seqno - 1
            else:
                self.log.warning("Reset: reset next send seqno to %d", new_seqno)
                state.send_seqno = new_seqno - 1
                
        elif self.context.isinstance(msgtype, Logout):
            # this propably happens mostly on acceptor side
            self.log.info("Logout received")
            if self.session.logout_hook:
                self.session.logout_hook(self, message, header)
            # send logout message
                
    def resend(self, start, end):
        """Resend message as for ResendRequest"""
        state = self.session.state
        self.log.info("handling resend from %d to %d", start, end)
        state.send_state = FixState.RESEND_RECEIVED
        resend_mode = self.session.get_conf('resend_mode', '')
        if resend_mode == 'GAPFILL' or resend_mode == 'BUYSIDE':
            self.log.info("sending SequeceReset-GapFill")
            opts = FixMessage()
            opts.set_field('PossDupFlag', 'Y', self.context)
            opts.set_field('OrigSendingTime', utc_timestamp(), self.context)
            opts.set_field('MsgSeqNum', start, self.context)
            mg = FixMessage()
            mg.set_field('GapFillFlag', 'Y', self.context)
            mg.set_field('NewSeqNo', state.send_seqno, self.context)
            self._transmit('SequenceReset', mg, options=opts, admin=True)
        elif resend_mode == 'RESET':
            self.log.info("sending SequeceReset-Reset")
            mg = FixMessage()
            # initialize to seqno after this message (seqno is last sent seqno)
            mg.set_field('NewSeqNo', state.send_seqno+2, self.context)
            self._transmit('SequenceReset', mg, options=opts, admin=True)
        elif resend_mode:
            self.log.warning("unknown resend_mode: %s", resend_mode)

    def request_resend(self, start, end):
        """Send  ResendRequest message"""
        state = self.session.state
        self.log.info("request resend from %d to %d", start, end)
        mg = FixMessage()
        mg.set_field('BeginSeqNo', start, self.context)
        mg.set_field('EndSeqNo', end, self.context)
        state.recv_state = FixState.RESEND_REQUESTED
        self._transmit('ResendRequest', mg, admin=True)
            
    def send_testrequest(self):
        """Send FIX TestRequest message"""

        state = self.session.state
        if state.testrq_queue:
            # Do not send if pending test requests
            return
        rqid = datetime_now()
        rq = FixMessage()
        rq.set_field('TestReqID', rqid, self.context)
        state.testrq_queue.append(rqid)
        self.log.debug("Sending test request: %s", rqid)
        self._transmit('TestRequest', rq)

    def send_heartbeat(self):
        """Send FIX Heatbeat message."""
        self.log.debug("Sending heartbeat")
        self._transmit('Heartbeat', FixMessage(), admin=True)

    def _next_header(self, options=None):
        """Provide next FIX message header."""

        state = self.session.state
        header = FixMessage()

        header.set_field('SenderCompID',
                         self.session.get_conf('sender_comp_id'), self.context)
        header.set_field('TargetCompID',
                         self.session.get_conf('target_comp_id'), self.context)
        if options is None:
            state.send_seqno += 1
            header.set_field('MsgSeqNum', state.send_seqno, self.context)
        else:
            if options.get_field('MsgSeqNum', self.context) is None:
                state.send_seqno += 1
                header.set_field('MsgSeqNum', state.send_seqno, self.context)
            # merge options
            header.join(options)

        header.set_field('SendingTime', utc_timestamp(), self.context)
        return header

    def _transmit(self, msgname, msg, options=None, admin=False):
        """Transmit data. Add headers and log message."""

        state = self.session.state
        data = self._next_header(options)
            
        data.extend(msg)
        if len(msgname) <= 2:
            data.set_prefix(self.context.version, msgname)
        else:
            data.add_prefix(msgname, self.context)
        
        if not admin:
            state.store(state.send_seqno, data)
        self.log.debug("OUT: %s", str(data))
        self.transmit(data)
        

