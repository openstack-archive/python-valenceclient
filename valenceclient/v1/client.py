#   Copyright 2017 Intel, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from valenceclient.common import http


class Client(object):

    podmanagers = "/v1/pod_managers"
    podmanager_path = "/v1/pod_managers/%s"

    def __init__(self, **kwargs):
        self.http_client = http.HTTPClient(**kwargs)

    def list_podmanagers(self):
        resp, body = self.http_client.json_request('get', self.podmanagers)
        return body

    def create_podmanager(self, request):
        resp, body = self.http_client.json_request('post', self.podmanagers,
                                                   **request)
        return body

    def delete_podmanager(self, id):
        resp, body = self.http_client.json_request('delete',
                                                   self.podmanager_path % id)
        return body

    def show_podmanager(self, id):
        resp, body = self.http_client.json_request('get',
                                                   self.podmanager_path % id)
        return body
