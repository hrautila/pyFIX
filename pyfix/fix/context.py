# (c) Harri Rautila, 2011

# This file is part of sxsuite library. It is free software, distributed
# under the terms of the GNU Lesser General Public License Version 3,
# or any later version.
# See the COPYING file included in this archive

_default_context = None 

_fix_modules = {}

def get_default_context():
    return _default_context

def set_default_context(context=None):
    if context is not None:
        _default_context = context
    else:
        _default_context = FixContext()

def do_import(name):
    from sys import modules
    m = __import__(name)
    return modules[name]


def fix_pytype(fixtype):
    """Convert FIX message type to Python basic type."""
    if fixtype in ['INT', 'NUMINGROUP', 'SEQNUM', 'DAYOFMONTH', 'TAGNUM']:
        return int
    elif fixtype in ['PRICE', 'QTY', 'PRICEOFFSET', 'AMT', 'PERCENTAGE', 'FLOAT']:
        return float
    elif fixtype in ['BOOLEAN']:
        return bool
    return str


class FixFieldDescriptor(object):
    """FIX message field descriptor.

    ``name``            message field name
    ``fixnumber``       FIX message tag number
    ``fixtype``         FIX type name
    ``pytype``          Corresponding Python type
    """

    def __init__(self, name, fixnumber, fixtype, pytype):
        self.name = name
        self.number = fixnumber
        self.fixtype = fixtype
        self.pytype = pytype

    def __str__(self):
        return "%s [tag=%d, %s, %s]" % (self.name, self.number, self.fixtype, self.pytype)
    
class FixGroupDescriptor(FixFieldDescriptor):
    """FIX message field group descriptor."""
    
    def __init__(self, name, fixnumber):
        FixFieldDescriptor.__init__(self, name, fixnumber, 'NUMINGROUP', int)
        self.fields = []
        
    
class FixContext(object):
    """FIX messaging context for FIX protocol version.

    """
    
    def __init__(self, name='', version='4.4', module_name=None):
        if not module_name:
            module_name = 'pyfix.fix.fix%s' % version.replace('.', '')
        module = do_import(module_name)
        global _fix_modules
        _fix_modules[version] = module
        #self._fixmod = do_import(module_name) # this makes context unpickable
        self._field_types = {}
        self._field_numbers = {}
        self._group_types = {}
        self._group_numbers = {}
        self.version = version
        if name:
            self.name = name
        else:
            self.name = 'FIX.' + self.version
        self.header_ids = getattr(module, 'FIX_HEADER_FIELD_IDS')
        self.trailer_ids = getattr(module, 'FIX_TRAILER_FIELD_IDS')

    def add_field(self, name, num, fixtype):
        """Add new field to context.

        """
        desc = FixFieldDescriptor(name, num, fixtype, fix_pytype(fixtype))
        self._field_types[name] = desc
        self._field_numbers[num] = desc
        

    def add_group(self, name, num, groupfields):
        """Add new field group to context.

        """
        groupdesc = FixGroupDescriptor(name, num)
        self._field_types[name] = groupdesc
        self._field_numbers[num] = groupdesc

        gspec = []
        for field in groupfields:
            if isinstance(field, int):
                desc = self.desc_for_id(field)
                gspec.append((desc.number, desc.name))
            elif isinstance(field, str):
                desc = self.desc_for_name(field)
                gspec.append((desc.number, desc.name))
            elif isinstance(field, tuple):
                gspec.append(field)
            else:
                # throw exception, maybe??
                pass

        self._group_types[name] = gspec
        self._group_numbers[num] = self._group_types[name]

    def desc_for_name(self, name):
        """Get field descriptor for ``name``"""
        if name[0] == '_':
            num = int(name[1:])
            return self.desc_for_id(num)

        if name in self._field_types:
            return self._field_types[name]
        return fix_desc_for_name(self.version, name)

    def desc_for_id(self, num):
        """Get field descriptor for message field numbered ``num``."""
        if num in self._field_numbers:
            return self._field_numbers[num]
        return fix_desc_for_id(self.version, num)
    
    def group_for_name(self, name):
        """Get group descriptor for group ``name``."""
        if name in self._group_types:
            return self._group_types[name]
        return fix_group_for_name(self.version, name)

    def group_for_id(self, num):
        """Get group descriptor for group numbered ``num``."""
        if num in self._group_numbers:
            return self._group_numbers[num]
        return fix_group_for_id(self.version, num)

    def msgtype_for_name(self, name):
        """Get FIX message type code for message ``name``."""
        return fix_msgtype_for_name(self.version, name)

    def name_for_msgtype(self, mtyp):
        """Get FIX message name for message of type code ``mtyp``."""
        return fix_name_for_msgtype(self.version, mtyp)

    def msgname_is_application(self, msgname):
        """Test if FIX message is application message."""
        return fix_message_is_application(self.version, msgname, True)

    def msgtype_is_application(self, msgtyp):
        """Test if message type corresponds application message."""
        return fix_message_is_application(self.version, msgtyp, False)

    def class_for_msgname(self, name):
        """Return Python class for message."""
        return fix_class_for_msgname(self.version, name)
    
    def create_message(self, name):
        """Return Python object for message type ``name``."""
        cls = self.class_for_msgname(name)
        return cls(self)

    def isinstance(self, num, cls):
        """Test if message is of type ``cls``."""
        mcls = self.class_for_msgname(self.name_for_msgtype(num))
        return cls == mcls

def fix_desc_for_name(version, name):
    fixmod = _fix_modules[version]
    return getattr(fixmod, '_fix_field_types')[name]


def fix_desc_for_id(version, num):
    fixmod = _fix_modules[version]
    return getattr(fixmod, '_fix_field_numbers')[num]


def fix_group_for_name(version, name):
    fixmod = _fix_modules[version]
    return getattr(fixmod, '_fix_group_types')[name]


def fix_group_for_id(version, num):
    fixmod = _fix_modules[version]
    return getattr(fixmod, '_fix_group_numbers')[num]

def fix_msgtype_for_name(version, name):
    fixmod = _fix_modules[version]
    return getattr(fixmod, '_fix_message_types')[name][0]


def fix_message_is_application(version, key, key_is_name):
    fixmod = _fix_modules[version]
    if key_is_name:
        return getattr(fixmod, '_fix_message_types')[key][1]
    return fix_message_is_application(fixmod,
                                      fix_name_for_msgtype(fixmod, key), True)
    

def fix_name_for_msgtype(version, mtyp):
    fixmod = _fix_modules[version]
    return getattr(fixmod, '_fix_msgtype_table')[mtyp]

def fix_class_for_msgname(version, name):
    fixmod = _fix_modules[version]
    return getattr(fixmod, name)


    
