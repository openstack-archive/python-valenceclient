# Copyright 2017 Intel, Inc.
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

import sushy
from sushy.resources import base

from valenceclient.redfish.resources.node import node
from valenceclient.redfish.resources.storage import storage

class ValenceSushy(sushy.Sushy):

    _nodes_path = base.Field(['Nodes', '@odata.id'], required=True)
    """NodeCollection path"""

    _storage_path = base.Field(['Services', '@odata.id'], required=True)

    def get_node_collection(self):
        """Get the NodeCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a NodeCollection object
        """
        return node.NodeCollection(self._conn, self._nodes_path,
                                   redfish_version=self.redfish_version)

    def get_node(self, identity):
        """Given the identity return a Node object

        :param identity: The identity of the Node resource
        :returns: The Node object
        """
        return node.Node(self._conn, identity,
                         redfish_version=self.redfish_version)

    def get_storage_service_collection(self):
        return storage.StorageServiceCollection(self._conn, self._storage_path,
                                                redfish_version=self.redfish_version)

    def get_storage_service(self, identity):
        return storage.StorageService(self._conn, identify,
                                      redfish_version=self.redfish_version)
