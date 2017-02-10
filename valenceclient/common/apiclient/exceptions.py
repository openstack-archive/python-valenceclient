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

"""
Exception definitions
"""

import inspect
import sys

import six
from six.moves import http_client

from valenceclient.common.i18n import _


class ClientException(Exception):
    """The base exception class for all exceptions this library raises"""

    message = _("ClientException")


class HttpError(ClientException):
    """The base exception class of all HTTP exceptions"""

    http_status = 0
    message = _("HTTP Error")

    def __init__(self, message=None, details=None, response=None,
                 request_id=None, url=None, method=None,
                 http_status=None):
        self.message = message or self.message
        self.details = details
        self.response = response
        self.request_id = request_id
        self.url = url
        self.method = method
        self.http_status = http_status

        formatted_string = "%s (HTTP %s)" % (self.message, self.http_status)
        if request_id:
            formatted_string += " (Request-ID: %s)" % (self.request_id)

        super(HttpError, self).__init__(formatted_string)


class HTTPClientError(HttpError):
    """Client-side HTTP error.
    Exception for cases in which the client seems to have erred.
    """

    message = _("HTTP Client Error")


class HttpServerError(HttpError):
    """Server-side HTTP error.
    Exception for cases in which the server is aware that it has
    erred or is incapable of performing the request.
    """

    message = _("HTTP Server Error")


# _code_map cotains all the classes that have http_status attribute
_code_map = dict((getattr(obj, 'http_status', None), obj)
                 for name, obj in vars(sys.modules[__name__]).items()
                 if inspect.isclass(obj) and
                 getattr(obj, 'http_status', False))


def from_response(response, method, url):
    """
    Returns an instance of :class:`HttpError` or subclass based on response.

    :param response: instance of `requests.Response` class
    :param method: HTTP method used for request
    :param url: URL used for request
    """

    req_id = response.headers.get('X-openstack-request-id')
    # NOTE(hdd) true for older versions of nova and cinder
    if not req_id:
        req_id = response.headers.get('X-compute-request-id')

    kwages = {
        'http_status': response.status_code,
        'response': response,
        'method': method,
        'url': url,
        'request_id': req_id
    }

    if 'retry_after' in response.headers:
        kwages['retry_after'] = response.headers['retry_after']

    content_type = response.headers.get('Content-Type', "")
    if content_type.startswith('application/json'):
        try:
            body = response.json()
        except ValueError:
            pass
        else:
            if isinstance(body, dict):
                error = body.get(list(body)[0])
                if isinstance(error, dict):
                    kwages['message'] = (error.get('message') or
                                         error.get('faultstring'))
                    kwages['details'] = (error.get('details') or
                                         six.text_type(body))
    elif content_type.startswith("text/"):
        kwages['details'] = getattr(response, 'text', '')

    try:
        cls = _code_map[response.status_code]
    except KeyError:
        # 5XX status codes are server errors
        if response.status_code >= http_client.INTERNAL_SERVER_ERROR:
            cls = HttpServerError
        # 4XX status codes are client request errors
        elif (http_client.BAD_REQUEST <= response.status_code <
              http_client.INTERNAL_SERVER_ERROR):
            cls = HTTPClientError
        else:
            cls = HttpError

    return cls