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


from valenceclient.common import base


class Node(base.Resource):
    def __repr__(self):
        return "<Node %s" % self._info


class NodeManager(base.CreateManager):
    resource_class = Node
    _resource_name = 'nodes'
    _creation_attributes = ['Processors', 'RemoteDrives', 'Memory']

    def list(self, resource_class=None):
        nodes = self._list(self._path(),
                           resource_class \
                           if resource_class else self.resource_class)
        return nodes

    def get(self, node_id):
        return self._get(node_id)

    def delete(self, node_id):
        return self._delete(node_id)

    def update(self, node_id, patch, http_method='PATCH'):
        return self._update(resource_id=node_id, patch=patch,
                            method=http_method)

    def compose(self, **kwargs):
        return self.create(**kwargs)
