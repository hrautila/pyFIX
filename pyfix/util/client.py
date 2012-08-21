
import json
import httplib

class FixHTTPClient(object):
    def __init__(self, address):
        self.address = address

    def send(self, message, url=''):
        url = url or "/session"
        body = json.dumps(message)
        conn = httplib.HTTPConnection(self.address[0], self.address[1], timeout=10)
        conn.request("POST", url, body)
        r1 = conn.getresponse()
        print r1.status, r1.reason

    def recv(self, url=''):
        url = url or "/session"
        conn = httplib.HTTPConnection(self.address[0], self.address[1], timeout=10)
        conn.request("GET", url)
        r1 = conn.getresponse()
        if r1.status == 200:
            data = r1.read()
            return json.loads(data)
        print r1.status, r1.reason
        return None


        
