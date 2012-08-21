# (c) Harri Rautila, 2011
#
# This file is part of pyFIX library. It is free software, distributed
# under the terms of the GNU Lesser General Public License Version 3,
# or any later version.
#
# See the COPYING file included in this archive

import logging as log

from context import *
from headerfields import FIX_HEADER_FIELD_IDS, FIX_TRAILER_FIELD_IDS

__all__ = ['FixObject', 'FixHeader', 'FixMessage', 'FixContext',
           'Heartbeat', 'Logon', 'Logout', 'Reject', 'ResendRequest',
           'SequenceReset', 'TestRequest',
           'set_default_context', 'get_default_context']

_SOH = chr(1)

_unknown_field_desc = FixFieldDescriptor('Unknown', 0, 'STRING', str)

class ParseError(Exception):
    pass

class FixMessage(list):
    """Raw representation of FIX message as list of tagged fields."""
    
    def to_raw(self):
        """Write message to wire-format."""

        # insert _SOH between fields and force to to non-unicode 
        s = _SOH.join(map(lambda x: str(x), self))
        chk = reduce(lambda x,y: x+ord(y), s, 0)
        chk += 1  # for missing SOH before checksum field
        return s + _SOH + "10=%03d" % (chk % 256)  + _SOH
        
    @classmethod
    def from_raw(cls, data):
        """Create message from wire-format data.

        Assumes ``data`` contains a complete wire format FIX message.
        """
        s = filter(None, data.split(_SOH))
        fixm = cls(s[:-1]) # do not include last checksum fied
        return fixm
        
    def validate(self):
        return all([self[0].startswith('8='),
                    self[1].startswith('9='),
                    self[2].startswith('35=')])
        
    def join(self, tail):
        """Append ``tail`` fields to self."""
        self.extend(tail)
        return self

    def add_prefix(self, msgname, context):
        """Add standard message prefix (version, msglen, type)."""
        self.set_prefix(context.version,
                        context.msgtype_for_name(msgname))
        return self
    
    def set_prefix(self, vers, msgcode=''):
        """Add standard message prefix (version, msglen, type).

        The message length is indicated in the BodyLength field and is 
        verified by counting the number of characters in the message following 
        the BodyLength field up to, and including, the delimiter
        immediately preceding the CheckSum tag (10=nnn).
        """
        if msgcode:
            self.insert(0, '35='+str(msgcode))

        # calculate length: +1 is for each <SOH>
        nbytes = reduce(lambda x, y: x+len(y)+1, self, 0) 
        self.insert(0, "9=%d" % nbytes)
        self.insert(0, '8=FIX.'+vers)
        return self

    def set_length(self):
        pos = n = 0
        if self[0].startswith('8=FIX'):
            pos = n = 1
        if self[n].startswith('9='):
            pos = 2
        # calculate length: +1 is for each <SOH>
        nbytes = reduce(lambda x, y: x+len(y)+1, self[pos:], 0)
        if pos != n:
            # length field was there already
            self[n] = '9=' + str(nbytes)
        else:
            # length is 2nd tagged field on message, so insert it @n
            self.insert(n, '9=' + str(nbytes))


    def split_message(self):
        """Split message to header and body."""
        hdr = FixMessage()
        body = FixMessage()
        for x in self:
            tagnum = int(x.split('=')[0])
            if  tagnum in FIX_HEADER_FIELD_IDS:
                hdr.append(x)
            elif tagnum not in FIX_TRAILER_FIELD_IDS:
                body.append(x)
        # endfor
        return hdr, body


    def get_field(self, name, context=None):
        """Get field value.

        Parameter ``name`` can be field name or tag number.
        """
        if context is not None:
            try:
                if not isinstance(name, int):
                    desc = context.desc_for_name(name)
                else:
                    desc = context.desc_for_id(name)
            except:
                return None
            tag = str(desc.number) + '='
            pytyp = desc.pytype
        else:
            tag = str(name) + '='
            pytyp = str

        n = self.find_tag(tag)
        if n == -1:
            return None
        return pytyp(self[n].split('=')[1])
    
    def set_field(self, name, value, context=None, append=True):
        """Set field value or if new tag add.

        Parameter ``name`` can be field name or tag number.
        """
        if context is not None:
            if not isinstance(name, int):
                desc = context.desc_for_name(name)
            else:
                desc = context.desc_for_id(name)
            tag = str(desc.number) + '='
        else:
            if not str(name).isdigit():
                raise ValueError("field name is not numeric.")
            tag = str(name) + '='

        n = self.find_tag(tag)
        if n == -1:
            if append:
                self.append(tag + str(value))
            else:
                self.insert(0, tag + str(value))
        else:
            # already exists, overwrite
            self[n] = tag + str(value)
        
    def find_tag(self, tag):
        n = 0
        for y in self:
            if y.startswith(tag):
                return n
            n += 1
        return -1

    def get(self, num, pytyp=str):
        tag = str(num) + '='
        n = self.find_tag(tag)
        if n == -1:
            return None
        return pytyp(self[n].split('=')[1])

    def set(self, num, val, append=True):
        tag = str(num) + '='
        n = self.find_tag(tag)
        if n == -1:
            if append:
                self.append(tag + str(val))
            else:
                self.insert(0, tag + str(val))
        else:
            # already exists, overwrite
            self[n] = tag + str(value)
        
    def add(self, num, val):
        tag = str(num) + '=' + str(val)
        self.append(tag)

    def ins(self, num, val, inx=0):
        tag = str(num) + '=' + str(val)
        self.insert(inx, tag)

    def delete(self, num):
        n = self.find_tag(str(num)+'=')
        if n != -1:
            del self[n]

class FixObject(object):
    """Base type for FIX message objects.

    Represents message as object and fields as normal object attributes.
    """
    def __init__(self, context, values={}):

        # called as ({...})
        if isinstance(context, dict):
            values = context
            context = _default_context
            
        self.__dict__["_context"]  = context
        if values:
            for k, v in values.items():
                setattr(self, k, v)
        
    def __setattr__(self, attr, value):
        try:
            desc = self._check_attribute(attr)
            if desc.fixtype == 'NUMINGROUP':
                if not isinstance(value, list):
                    raise TypeError('%s: invalid value type for field group' % attr)
                vl = []
                for val in value:
                    if isinstance(val, FixObject):
                        vl.append(val)
                    elif isinstance(val, dict):
                        vl.append(FixObject(self._context, val))
                    else:
                        raise TypeError('%s: invalid value type for field group' % attr)
                self.__dict__[attr] = vl
            else:
                self.__dict__[attr] = value
        except KeyError, e:
            raise AttributeError("%s does not exist." % attr)

    def __str__(self):
        return "%s" % self.__dict__
    
    def _check_attribute(self, attr):
        if attr.startswith('_'):
            try:
                num = int(attr[1:])
                return self._context.desc_for_id(num)
            except ValueError:
                return _unknown_field_desc
        return self._context.desc_for_name(attr)
        
    def attributes(self):
        """Return list of defined valid fields."""
        return filter(lambda x: x != '_context', self.__dict__.keys())
    
    def get(self, key, defval):
        return getattr(self, key, defval)

    def to_message(self, header=None, full=False):
        """Translate ``FixObject`` to a ``FixMessage``."""
        msg_m = _make_mbody(self, self._context)
        if header is None:
            header = FixHeader(self._context)
        hdr_m = _make_mheader(self, header, self._context)
        hdr_m.join(msg_m)
        if full:
            # add length and version
            hdr_m.set_prefix(self._context.version)
        return hdr_m
        
    @classmethod
    def from_message(cls, fixm, context):
        """Split message to request and header objects."""

        # Message fields is 'tag=STRING'. String may contain equal '=' signs and therefore
        # lambda functions second part joins together parts possibly splited apart by the
        # split function
        vfields = map(lambda x: (int(x[0]), '='.join(x[1:])),
                      [y.split('=') for y in fixm])

        hdr, msgname, index = _extract_header(vfields, 0, context)
        cls = context.class_for_msgname(msgname)
        body = cls(context)
        body, count = _extract_body(vfields[index:], 0, context, body)

        index += count
        return body, hdr

    def mheader(self, header, context):
        return _make_mheader(self, header, context)

    def mbody(self, context):
        return _make_mbody(self, context)

    def is_admin(self):
        return False

class FixHeader(FixObject):
    """Header part of FIX message."""
    
    def _check_attribute(self, attr):
        desc = FixObject._check_attribute(self, attr)
        if desc.number not in self._context.header_ids:
            if desc.number > 0:
                raise AttributeError("%s: not a header field" % desc.name)
        return desc


    

class Heartbeat(FixObject):
    """FIX Heartbeat message."""
    def is_admin(self):
        return True

class Logon(FixObject):
    """FIX Logon message."""
    def is_admin(self):
        return True

class Logout(FixObject):
    """FIX Logout message."""
    def is_admin(self):
        return True

class Reject(FixObject):
    """FIX Reject message."""
    def is_admin(self):
        return True

class ResendRequest(FixObject):
    """FIX ResendRequest message."""
    def is_admin(self):
        return True

class SequenceReset(FixObject):
    """FIX SequenceReset message."""
    def is_admin(self):
        return True

class TestRequest(FixObject):
    """FIX TestRequest message."""
    def is_admin(self):
        return True

def _make_mheader(obj, header, context):
    """Create ``FixMessage`` header for this ``FixObject`` including
    attributes from ``header``.

    """
    msgtype = context.msgtype_for_name(obj.__class__.__name__)
    fixm = FixMessage()
    hdr_fields = []
    for name in header.attributes():
        desc = context.desc_for_name(name)
        # append all but these 3 that are inserted in the end
        if desc.number not in [8, 9, 35]:
            hdr_fields.append((desc.number, str(getattr(header, name))))

    # sorting to ascending order is not really needed ??
    hdr_fields.sort(lambda x, y: cmp(x[0], y[0]))
    for num, val in hdr_fields:
        fixm.add(num, val)
    # insert message type infront
    fixm.ins(35, msgtype)
    return fixm


def _make_mbody(obj, context):
    """Create message body for this ``FixObject``."""

    fixm = FixMessage()
    for name in obj.attributes():
        desc = context.desc_for_name(name)
        #print "desc %s is: %s" % (desc.name, desc.__class__.__name__)
        if not isinstance(desc, FixGroupDescriptor):
            fixm.add(desc.number, str(getattr(obj, name)))
        else:
            grp = getattr(obj, name)
            fixm.add(desc.number, len(grp))
            gspec = context.group_for_name(name)

            _build_group(grp, gspec, fixm, context)
    # endfor
    return fixm

def _build_group(group, gspec, fixm, context):
    """Build ``group`` spesified by ``gspec`` into FixMessage ``fixm``."""

    for ge in group:
        for tagnum, tagname in gspec:
            if tagname not in ge.attributes():
                continue

            desc = context.desc_for_name(tagname)
            if not isinstance(desc, FixGroupDescriptor):
                fixm.add(desc.number, str(getattr(ge, tagname)))
            else:
                subgrp = getattr(ge, tagname)
                fixm.add(desc.number, len(subgrp))
                subspec = context.group_for_name(tagname)
                _build_group(subgrp, subspec, fixm, context)
        # endfor
    # endfor 


def _extract_header(fields, index, context):
    """Extract header part starting at index from message fields."""

    hdr = FixHeader(context)
    msgname = 'FixObject'
    for num, val in fields:
        if num not in context.header_ids:
            break
        if num in context.trailer_ids:
            break
        try:
            desc = context.desc_for_id(num)
        except KeyError, e:
            desc = FixFieldDescriptor('_%d' % num, num, 'STRING', str)
        try:
            setattr(hdr, desc.name, desc.pytype(val))
        except ValueError, e:
            # log.debug("%s [tag=%d, name=%s, val=%s]", str(e), num, desc.name, val)
            if desc.pytype == int:
                setattr(target, desc.name, float(val))
            else:
                setattr(target, desc.name, str(val))
        if num == 35:
            msgname = context.name_for_msgtype(val)
        index += 1
    # end of loop
    return hdr, msgname, index

def _extract_body(fields, index, context, body, group_ids=[]):
    """Extract message body part starting at index from fields."""

    if isinstance(body, list):
        # recursively called with list object as body (in group)
        target = FixObject(context)
    else:
        target = body

    fields_seen = []
    max_index = len(fields)

    while index < max_index:
        num, val = fields[index]
        if group_ids and num not in group_ids:
            # end of a group here
            body.append(target)
            return body, index

        if num in END_FIELDS:
            return body, index
        try:
            desc = context.desc_for_id(num)
        except KeyError, e:
            desc = FixFieldDescriptor('_%d' % num, num, 'STRING', str)

        if isinstance(desc, FixGroupDescriptor):
            grp_fields = map(lambda x: x[0], context.group_for_id(num))
            # print "extract group %s: %s" % (desc.name, grp_fields)
            val, count = _extract_body(fields[index+1:], 0, context, [], grp_fields)
            index += count
        elif group_ids:
            # inside group
            if num not in fields_seen:
                fields_seen.append(num)
            else:
                # repeating group
                body.append(target)
                target = FixObject(context)
                fields_seen = [num]
        try:
            # set the value and convert to python type
            if isinstance(val, list):
                setattr(target, desc.name, val)
            else:
                setattr(target, desc.name, desc.pytype(val))
        except ValueError, e:
            # log.debug("%s [tag=%d, name=%s, val=%s]", str(e), num, desc.name, val)
            # if int field makes an error, try float (may thow
            if desc.pytype == int:
                setattr(target, desc.name, float(val))
            else:
                setattr(target, desc.name, str(val))
        index += 1
    # end of loop
    if group_ids:
        # don't forget the last target of a group
        body.append(target)
    return body, index




