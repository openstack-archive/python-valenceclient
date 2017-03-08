# Copyright 2017 99cloud, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import mock
from oslo_serialization import jsonutils

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
        error_body = _get_error_body()
        kwargs = {"valence_url": "http://localhost"}
        client = http.HTTPClient(**kwargs)
        client.session = utils.mockSession(
            {'Content-Type': 'application/json'},
            error_body,
            version=1,
            status_code=http_client.INTERNAL_SERVER_ERROR)

        self.assertRaises(exc.InternalServerError,
                          client.json_request,
                          'GET', 'redfish/v1')

    def test_server_exception_msg_only(self):
        error_body = "test error msg"
        kwargs = {"valence_url": "http://localhost"}
        client = http.HTTPClient(**kwargs)
        client.session = utils.mockSession(
            {'Content-Type': 'application/json'},
            error_body,
            version=1,
            status_code=http_client.INTERNAL_SERVER_ERROR)

        self.assertRaises(exc.InternalServerError,
                          client.json_request,
                          'GET', 'redfish/v1')

    def test_server_exception_description_only(self):
        error_msg = "test error msg"
        error_body = _get_error_body(description=error_msg)
        kwargs = {"valence_url": "http://localhost/"}
        client = http.HTTPClient(**kwargs)
        client.session = utils.mockSession(
            {'Content-Type': 'application/json'},
            error_body,
            version=1,
            status_code=http_client.BAD_REQUEST)

        self.assertRaises(exc.BadRequest,
                          client.json_request,
                          'GET', 'redfish/v1')

    def test_server_https_request_ok(self):
        kwargs = {"valence_url": "http://localhost/"}
        client = http.HTTPClient(**kwargs)
        client.session = utils.mockSession(
            {'Content-Type': 'application/json'},
            'Body',
            version=1,
            status_code=http_client.OK)

        client.json_request('GET', 'redfish/v1')

    def test_server_http_not_valide_request(self):
        kwargs = {"valence_url": "http://localhost/"}
        client = http.HTTPClient(**kwargs)
        client.session.request = mock.Mock(
            side_effect=http.requests.exceptions.InvalidSchema)
        self.assertRaises(exc.ValidationError, client._http_request, 'GET',
                          'http://localhost/')

    @mock.patch.object(http.LOG, 'debug', autospec=True)
    def test_log_curl_request(self, mock_log):
        # kwargs = {"valence_url": "http://localhost/"}
        # client = http.HTTPClient(**kwargs)
        pass
