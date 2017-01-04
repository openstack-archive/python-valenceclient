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

from valenceclient.common.apiclient import exceptions
from valenceclient.common.apiclient.exceptions import  *

CommunicationError = ConnectionError
HTTPBadRequest = BadRequest
HTTPInternalServerError = InternalServerError


class InvalidAttribution(ClientException):
    pass

def from_response(response, message=None, traceback=None, method=None,
                  url=None):
    """Return an HttpError instance based on response from httplib/requests"""

    error_body = {}
    if message:
        error_body['message'] = message
    if traceback:
        error_body['traceback'] = traceback

    if hasattr(response, 'status') and not hasattr(response, 'status_code'):
        # NOTE(akurilin): These modifications around response object give
        # ability to get all necessary information in method `from_response`
        # from common code, which expecting response object from `requests`
        # library instead of object from `httplib/httplib2` library.
        response.status_code = response.status
        response.headers = {
            'Content-Type': response.getheader('content-type', '')}

    if hasattr(response, 'status_code'):
        # NOTE(jiangfei): These modifications allow SessionClient
        # to handle faultstring.
        response.json = lambda:{'error': error_body}

    return exceptions.from_response(response, method=method, url=url)