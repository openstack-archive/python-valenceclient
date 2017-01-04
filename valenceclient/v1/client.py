from valenceclient.common import  http
from valenceclient.common.i18n import _
from valenceclient import exc

from valenceclient.v1 import chassis

class Client(object):

    def __init__(self, **kwargs):
        if kwargs.get('os_username') or kwargs.get('os_password'):
            raise exc.Unauthorized(_("None username or password"))

        self.http_client = http.