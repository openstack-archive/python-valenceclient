#   Copyright 2017 NEC, Corp.
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

from valenceclient.common import base


class Node(base.Resource):
    def __repr__(self):
        return "<Node %s>" % self._info


class NodeClient(base.CreateManager):
    resource_class = Node
    _creation_attributes = ['name', 'podm_id', 'flavor_id', 'properties']
    _resource_name = 'nodes'

    def list_nodes(self):
        return self._list(self._path())

    def compose_node(self, request):
        return self.create(**request)

    def delete_node(self, node_id):
        self._delete(resource_id=node_id)

    def show_node(self, node_id):
        return self._get(resource_id=node_id)

    def manage_node(self, request):
        return self._manage(path='/manage', **request)
