from valenceclient.common import http
from valenceclient.v1 import node

class Client(object):

    def __init__(self, **kwargs):
        self.http_client = http.HTTPClient(**kwargs)
        self.node = node.NodeManager(self.http_client)
