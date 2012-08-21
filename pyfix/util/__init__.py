#

def read_config_section(path, section):
    """Read named ``section`` from configuration file ``path``.

    Returns section items as dictionary.
    """
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read(path)
    if config.has_section(section):
        return dict(config.items(section))
    return {}


def parse_address(url):
    """Parse network addres in form scheme://host:port.

    Return triple (host, port, scheme).
    """
    from urlparse import urlparse
    r = urlparse(url)
    if ':' in r.netloc:
        h, p = r.netloc.split(':')
    else:
        h = r.netloc
        p = 0
    return (h, int(p), r.scheme)


