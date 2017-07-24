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

import logging

from sushy import exceptions
from sushy.resources import base
from sushy.resources.system import processor

from valenceclient.redfish.resources import common
from valenceclient.redfish.resources.node import constants as node_cons
from valenceclient.redfish.resources.node import mappings as node_maps


LOG = logging.getLogger(__name__)


class ActionsField(base.CompositeField):
    reset = common.ResetActionField('#ComposedNode.Reset')
    assemble = common.AssembleActionField('#ComposedNode.Assemble')
    attach_endpoint = common.AttachEndpointActionField(
        '#ComposedNode.AttachEndpoint')
    detach_endpoint = common.DetachEndpointActionField(
        '#ComposedNode.DetachEndpoint')


class BootField(base.CompositeField):
    allowed_values = base.Field(
        'BootSourceOverrideTarget@Redfish.AllowableValues',
        adapter=list)

    enabled = base.MappedField('BootSourceOverrideEnabled',
                               node_maps.BOOT_SOURCE_ENABLED_MAP)

    mode = base.MappedField('BootSourceOverrideMode',
                            node_maps.BOOT_SOURCE_MODE_MAP)

    target = base.MappedField('BootSourceOverrideTarget',
                              node_maps.BOOT_SOURCE_TARGET_MAP)


class MemorySummaryField(base.CompositeField):
    health = base.Field(['Status', 'Health'])
    """The overall health state of memory.

    This signifies health state of memory along with its dependent resources.
    """

    size_gib = base.Field('TotalSystemMemoryGiB', adapter=int)
    """The size of memory of the node in GiB.

    This signifies the total installed, operating system-accessible memory
    (RAM), measured in GiB.
    """


class Node(base.ResourceBase):

    boot = BootField('Boot', required=True)
    """A dictionary containg the current boot device, frequency and mode"""

    composed_node_state = base.MappedField('ComposedNodeState',
                                           node_maps.COMPOSED_NODE_STATE_MAP)
    """Current state of assembly process for this node"""

    description = base.Field('Description')
    """The node description"""

    identity = base.Field('Id', required=True)
    """The node identity string"""

    name = base.Field('Name')
    """The node name"""

    power_state = base.MappedField('PowerState',
                                   node_maps.NODE_POWER_STATE_MAP)
    """The node power state"""

    uuid = base.Field('UUID')
    """The node UUID"""

    memory_summary = MemorySummaryField('Memory')
    """The summary info of memory of the node in general detail"""

    _processors = None  # ref to ProcessorCollection instance

    _actions = ActionsField('Actions', required=True)

    def __init__(self, connector, identity, redfish_version=None):
        """A class representing a ComposedNode

        :param connector: A Connector instance
        :param identity: The identity of the Node resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(Node, self).__init__(connector, identity, redfish_version)

    def _get_reset_action_element(self):
        reset_action = self._actions.reset
        if not reset_action:
            raise exceptions.MissingActionError(action='#ComposedNode.Reset',
                                                resource=self._path)
        return reset_action

    def _get_assemble_action_element(self):
        assemble_action = self._actions.assemble
        if not assemble_action:
            raise exceptions.MissingActionError(action='#ComposedNode.Assemble',
                                                resource=self._path)
        return assemble_action

    def get_allowed_reset_node_values(self):
        """Get the allowed values for resetting the node.

        :returns: A set with the allowed values.
        """
        reset_action = self._get_reset_action_element()

        if not reset_action.allowed_values:
            LOG.warning('Could not figure out the allowed values for the '
                        'reset node action for Node %s', self.identity)
            return set(node_maps.RESET_NODE_VALUE_MAP_REV)

        return set([node_maps.RESET_NODE_VALUE_MAP[v] for v in
                    set(node_maps.RESET_NODE_VALUE_MAP).
                    intersection(reset_action.allowed_values)])

    def reset_node(self, value):
        """Reset the node.

        :param value: The target value.
        :raises: InvalidParameterValueError, if the target value is not
            allowed.
        """
        valid_resets = self.get_allowed_reset_node_values()
        if value not in valid_resets:
            raise exceptions.InvalidParameterValueError(
                parameter='value', value=value, valid_values=valid_resets)

        value = node_maps.RESET_NODE_VALUE_MAP_REV[value]
        target_uri = self._get_reset_action_element().target_uri

        self._conn.post(target_uri, data={'ResetType': value})

    def assemble_node(self):
        """Assemble the composed node."""
        target_uri = self._get_assemble_action_element().target_uri

        self._conn.post(target_uri)

    def get_allowed_node_boot_source_values(self):
        """Get the allowed values for changing the boot source.

        :returns: A set with the allowed values.
        """
        if not self.boot.allowed_values:
            LOG.warning('Could not figure out the allowed values for '
                        'configuring the boot source for Node %s',
                        self.identity)
            return set(node_maps.BOOT_SOURCE_TARGET_MAP_REV)

        return set([node_maps.BOOT_SOURCE_TARGET_MAP[v] for v in
                    set(node_maps.BOOT_SOURCE_TARGET_MAP).
                    intersection(self.boot.allowed_values)])

    def set_node_boot_source(self, target,
                             enabled=node_cons.BOOT_SOURCE_ENABLED_ONCE,
                             mode=None):
        """Set the boot source.

        Set the boot source to use on next reboot of the Node.

        :param target: The target boot source.
        :param enabled: The frequency, whether to set it for the next
            reboot only (BOOT_SOURCE_ENABLED_ONCE) or persistent to all
            future reboots (BOOT_SOURCE_ENABLED_CONTINUOUS) or disabled
            (BOOT_SOURCE_ENABLED_DISABLED).
        :param mode: The boot mode, UEFI (BOOT_SOURCE_MODE_UEFI) or
            Legacy (BOOT_SOURCE_MODE_LEGACY).
        :raises: InvalidParameterValueError, if any information passed is
            invalid.
        """
        valid_targets = self.get_allowed_node_boot_source_values()
        if target not in valid_targets:
            raise exceptions.InvalidParameterValueError(
                parameter='target', value=target, valid_values=valid_targets)

        if enabled not in node_maps.BOOT_SOURCE_ENABLED_MAP_REV:
            raise exceptions.InvalidParameterValueError(
                parameter='enabled', value=enabled,
                valid_values=list(node_maps.BOOT_SOURCE_TARGET_MAP_REV))

        data = {
            'Boot': {
                'BootSourceOverrideTarget':
                    node_maps.BOOT_SOURCE_TARGET_MAP_REV[target],
                'BootSourceOverrideEnabled':
                    node_maps.BOOT_SOURCE_ENABLED_MAP_REV[enabled]
            }
        }

        if mode is not None:
            if mode not in node_maps.BOOT_SOURCE_MODE_MAP_REV:
                raise exceptions.InvalidParameterValueError(
                    parameter='mode', value=mode,
                    valid_values=list(node_maps.BOOT_SOURCE_MODE_MAP_REV))

            data['Boot']['BootSourceOverrideMode'] = (
                node_maps.BOOT_SOURCE_MODE_MAP_REV[mode])

        self._conn.patch(self.path, data=data)

    def _get_processor_collection_path(self):
        """Helper function to find the ProcessorCollection path"""
        processor_col = self.json.get('Processors')
        if not processor_col:
            raise exceptions.MissingAttributeError(attribute='Processors',
                                                   resource=self._path)
        return processor_col.get('@odata.id')

    @property
    def processors(self):
        """Property to provide reference to `ProcessorCollection` instance

        It is calculated once when the first time it is queried. On refresh,
        this property gets reset.
        """
        if self._processors is None:
            self._processors = processor.ProcessorCollection(
                self._conn, self._get_processor_collection_path(),
                redfish_version=self.redfish_version)

        return self._processors

    def refresh(self):
        super(Node, self).refresh()
        self._processors = None


class NodeCollection(base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Node

    def __init__(self, connector, path, redfish_version=None):
        """A class representing a ComposedNodeCollection

        :param connector: A Connector instance
        :param path: The canonical path to the Node collection resource
        :param redfish_version: The version of RedFish. Used to construct
            the object according to schema of the given version.
        """
        super(NodeCollection, self).__init__(connector, path,
                                             redfish_version)
