# Copyright 2016 99cloud
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


import copy
import functools
import logging
import requests
import time

import six
from six.moves import http_client
import six.moves.urllib.parse as urlparse


from oslo_serialization import jsonutils
from oslo_utils import strutils

from valenceclient.common.i18n import _
from valenceclient.common.i18n import _LE
from valenceclient import exc

LOG = logging.getLogger(__name__)
USER_AGENT = 'python-valenceclient'

API_VERSION = '/v1'
DEFAULT_VERSION = 1

DEFAULT_MAX_RETRIES = 5
DEFAULT_RETRY_INTERVAL = 2


def _trim_endpoint_api_version(url):
    """Trim API version and trailing slash from endpoint."""

    return url.rstrip('/').rstip(API_VERSION)


def _extract_error_json(body):
    error_json = {}
    try:
        body_json = jsonutils.loads(body)
        if 'error_message' in body_json:
            raw_msg = body_json['error_message']
            error_json = jsonutils.loads(raw_msg)
    except ValueError:
        pass

    return error_json


def with_retries(func):
    """Wrapper for _http_request adding support for retries."""

    @functools.wraps(func)
    def wrapper(self, url, method, **kwargs):
        if self.conflict_max_retries is None:
            self.conflict_max_retries = DEFAULT_MAX_RETRIES
        if self.conflict_retry_interval is None:
            self.conflict_retry_interval = DEFAULT_RETRY_INTERVAL

        num_attempts = self.conflict_max_retries + 1
        for attempt in range(1, num_attempts + 1):
            try:
                return func(url, method, **kwargs)
            except Exception as error:
                msg = (_LE("Error contacting Valence server: %(error)s."
                           "Attempt %(attempt)d of %(total)d") %
                       {'attempt': attempt,
                        'total': num_attempts,
                        'error': error})
                if attempt == num_attempts:
                    LOG.error(msg)
                else:
                    LOG.debug(msg)
                    time.sleep(self.conflict_retry_interval)
        return wrapper


class HTTPClient(object):

    def __init__(self, **kwargs):
        self.valence_api_version = kwargs.get('valence_api_version',
                                              DEFAULT_VERSION)
        self.valence_url = kwargs.get('valence_url')
        self.session = requests.Session()

    def log_curl_request(self, method, url, kwargs):
        curl = ['curl -i -X %s' % method]

        for (key, value) in kwargs['headers'].items():
            header = "-H '%s: %s'" % (key, value)
            curl.append(header)

        if 'body' in kwargs:
            body = strutils.mask_password(kwargs['body'])
            curl.append("-d '%s'" % body)

        curl.append(urlparse.urljoin('v1', self.valence_url))
        LOG.debug(" ".join(curl))

    @staticmethod
    def log_http_response(resp, body=None):
        status = (resp.raw.version / 10.0, resp.status_code, resp.reason)
        dump = ['\nHTTP/%.1f %s %s' % status]
        dump.extend(['%s: %s' % (k, v) for k, v in resp.headers.items()])
        dump.append('')
        if body:
            body = strutils.mask_password(body)
            dump.extend([body, ''])
        LOG.debug('\n'.join(dump))

    def _make_connection_url(self, url):
        return urlparse.urljoin(self.valence_url, url)

    def _http_request(self, url, method, **kwargs):
        """Send an http request with the specified characteristics

        Wrapper around request.Session.request to handle tasks such as
        setting headers and error handling.
        """

        kwargs['headers'] = copy.deepcopy(kwargs.get('headers', {}))
        kwargs['headers'].setdefault('User-agent', USER_AGENT)

        self.log_curl_request(method, url, kwargs)
        body = kwargs.pop('body', None)
        if body:
            kwargs['data'] = body
        conn_url = self._make_connection_url(url)
        try:
            resp = self.session.request(method, conn_url, **kwargs)
        except requests.exceptions.RequestException as e:
            msg = (_("Error has occured while handling request for "
                     "%(url)s: %(e)s") % dict(url=conn_url, e=e))
            if isinstance(e, ValueError):
                raise exc.ValidationError(msg)
            raise exc.ConnectionRefuse(msg)

        self.log_http_response(resp, resp.text)
        body_iter = six.StringIO(resp.text)

        if resp.status_code >= http_client.BAD_REQUEST:
            error_json = _extract_error_json(resp.text)
            raise exc.from_response(resp, error_json.get('faultstring'),
                                    error_json.get('debugfino'), method, url)
        elif resp.status_code in (http_client.FOUND,
                                  http_client.USE_PROXY):
            return self._http_request(resp['location'], method, **kwargs)

        return resp, body_iter

    def json_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('Accept', 'application/json')
        if 'body' in kwargs:
            kwargs['body'] = jsonutils.dump_as_bytes(kwargs['body'])

        resp, body_iter = self._http_request(url, method, **kwargs)
        content_type = resp.headers.get('Content-Type')
        if(resp.status_code in (http_client.NO_CONTENT,
                                http_client.RESET_CONTENT)
            or content_type is None):
            return resp, list()

        if 'application/json' in content_type:
            body = ''.join([chunk for chunk in body_iter])
            try:
                body = jsonutils.loads(body)
            except ValueError:
                LOG.error(_LE('Could not decode response body as JSON'))
        else:
            body = None

        return resp, body