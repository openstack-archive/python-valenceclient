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

    nodes = "/v1/nodes"
    node_path = "/v1/nodes/%s"
    node_manage_path = "/v1/nodes/manage"

    systems = "v1/systems"
    system_path = "v1/systems/%s"

    flavors = "v1/flavors"
    flavor_path = "v1/flavors/%s"

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

    def update_podmanager(self, id, request):
        resp, body = self.http_client.json_request('patch',
                                                   self.podmanager_path % id,
                                                   **request)
        return body

    def list_nodes(self):
        resp, body = self.http_client.json_request('get', self.nodes)
        return body

    def compose_node(self, request):
        resp, body = self.http_client.json_request('post', self.nodes,
                                                   **request)
        return body

    def list_node_by_id(self, id):
        resp, body = self.http_client.json_request('get',
                                                   self.node_path % id)
        return body

    def delete_node(self, id):
        resp, body = self.http_client.json_request('delete',
                                                   self.node_path % id)
        return body

    def manage_node(self, request):
        resp, body = self.http_client.json_request('post',
                                                   self.node_manage_path,
                                                   **request)
        return body

    def list_systems(self, request):
        resp, body = self.http_client.json_request('get', self.systems,
                                                   **request)
        return body

    def list_system_by_id(self, id, request):
        resp, body = self.http_client.json_request('get',
                                                   self.system_path % id,
                                                   **request)
        return body

    def list_flavors(self):
        resp, body = self.http_client.json_request('get', self.flavors)
        return body

    def create_flavor(self, request):
        resp, body = self.http_client.json_request('post', self.flavors,
                                                   **request)
        return body

    def list_flavor_by_id(self, id):
        resp, body = self.http_client.json_request('get',
                                                   self.flavor_path % id)
        return body

    def delete_flavor(self, id):
        resp, body = self.http_client.json_request('delete',
                                                   self.flavor_path % id)
        return body

    def update_flavor(self, id, request):
        resp, body = self.http_client.json_request('patch',
                                                   self.flavor_path % id,
                                                   **request)
        return body
