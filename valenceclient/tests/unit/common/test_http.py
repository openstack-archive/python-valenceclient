import time
import mock
from oslo_serialization import jsonutils
import requests
import six
from six.moves import http_client

from valenceclient.common import http
from valenceclient import exc
from valenceclient.tests.unit import utils

DEFAULT_TIMEOUT = 600
DEFAULT_HOST = 'localhost'
DEFAULT_POST = '1234'


def _get_error_body(faultstring=None, debuginfo=None, description=None):
    if description:
        error_body = {'description': description}
    else:
        error_body = {
            'faultstring': faultstring,
            'debuginfo': debuginfo
            }
    raw_error_body = jsonutils.dump_as_bytes(error_body)
    body = {'error_message': raw_error_body}
    return jsonutils.dumps(body)


class HttpClientTest(utils.BaseTestCase):

    def test_url_generation_trailing_slash_in_base(self):
        kwargs = {"valence_url": "http://localhost/"}
        client = http.HTTPClient(**kwargs)
        url = client._make_connection_url('/redfish/v1')
        self.assertEqual('http://localhost/redfish/v1', url)

    def test_url_generation_without_trailing_slash_in_base(self):
        kwargs = {"valence_url": "http://localhost"}
        client = http.HTTPClient(**kwargs)
        url = client._make_connection_url('/redfish/v1')
        self.assertEqual('http://localhost/redfish/v1', url)

    def test_url_generation_without_prefix_slash_in_path(self):
        kwargs = {"valence_url": "http://localhost"}
        client = http.HTTPClient(**kwargs)
        url = client._make_connection_url('redfish/v1')
        self.assertEqual('http://localhost/redfish/v1', url)

    def test_server_exception_empty_body(self):
        pass

    def test_server_https_empty_body(self):
        pass

    def test_server_execption_msg_only(self):
        pass

    def test_server_exception_description_only(self):
        pass

    def test_server_http_request_ok(self):
        pass

    def test_server_https_request_ok(self):
        pass

    def test_server_http_not_valide_request(self):
        pass

    def test_server_https_bad_request(self):
        pass
