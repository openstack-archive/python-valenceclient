from valenceclient.common import  http
from valenceclient.common.i18n import _
from valenceclient import exc

from valenceclient.v1 import node
from valenceclient.v1 import system

class Client(object):

    def __init__(self, **kwargs):
        self.http_client = http.HTTPClient(**kwargs)
        self.node = node.NodeManager(self.http_client)
