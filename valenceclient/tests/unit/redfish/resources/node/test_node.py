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

import json

import mock
from sushy import exceptions
from sushy.resources.system import processor
import testtools

from valenceclient.redfish.resources.node import constants as node_cons
from valenceclient.redfish.resources.node import node


class NodeTestCase(testtools.TestCase):

    def setUp(self):
        super(NodeTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/node.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.node_inst = node.Node(
            self.conn, '/redfish/v1/Nodes/Node1',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.node_inst._parse_attributes()
        self.assertEqual('1.0.2', self.node_inst.redfish_version)
        self.assertEqual('Node #1', self.node_inst.description)
        self.assertEqual(node_cons.COMPOSED_NODE_STATE_ALLOCATED,
                         self.node_inst.composed_node_state)
        self.assertEqual('Node1', self.node_inst.identity)
        self.assertEqual('Composed Node', self.node_inst.name)
        self.assertEqual('fa39d108-7d70-400a-9db2-6940375c31c2',
                         self.node_inst.uuid)
        self.assertEqual(node_cons.NODE_POWER_STATE_ON,
                         self.node_inst.power_state)
        self.assertEqual(32, self.node_inst.memory_summary.size_gib)
        self.assertEqual("OK", self.node_inst.memory_summary.health)
        self.assertIsNone(self.node_inst._processors)

    def test__parse_attributes_missing_actions(self):
        self.node_inst.json.pop('Actions')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Actions',
            self.node_inst._parse_attributes)

    def test__parse_attributes_missing_boot(self):
        self.node_inst.json.pop('Boot')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Boot',
            self.node_inst._parse_attributes)

    def test__parse_attributes_missing_reset_target(self):
        self.node_inst.json['Actions']['#ComposedNode.Reset'].pop(
            'target')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError,
            'attribute Actions/#ComposedNode.Reset/target',
            self.node_inst._parse_attributes)

    def test_get__reset_action_element(self):
        value = self.node_inst._get_reset_action_element()
        self.assertEqual("/redfish/v1/Nodes/Node1/Actions/"
                         "ComposedNode.Reset",
                         value.target_uri)
        self.assertEqual(["On",
                          "ForceOff",
                          "GracefulRestart",
                          "ForceRestart",
                          "Nmi",
                          "ForceOn",
                          "PushPowerButton",
                          "GracefulShutdown"
                          ],
                         value.allowed_values)

    def test_get__reset_action_element_missing_reset_action(self):
        self.node_inst._actions.reset = None
        self.assertRaisesRegex(
            exceptions.MissingActionError, 'action #ComposedNode.Reset',
            self.node_inst._get_reset_action_element)

    def test_get_allowed_reset_node_values(self):
        values = self.node_inst.get_allowed_reset_node_values()
        expected = set([node_cons.RESET_GRACEFUL_SHUTDOWN,
                        node_cons.RESET_GRACEFUL_RESTART,
                        node_cons.RESET_FORCE_RESTART,
                        node_cons.RESET_FORCE_OFF,
                        node_cons.RESET_FORCE_ON,
                        node_cons.RESET_ON,
                        node_cons.RESET_NMI,
                        node_cons.RESET_PUSH_POWER_BUTTON])
        self.assertEqual(expected, values)
        self.assertIsInstance(values, set)

    @mock.patch.object(node.LOG, 'warning', autospec=True)
    def test_get_allowed_reset_system_values_no_values_specified(
            self, mock_log):
        self.node_inst._actions.reset.allowed_values = {}
        values = self.node_inst.get_allowed_reset_node_values()
        # Assert it returns all values if it can't get the specific ones
        expected = set([node_cons.RESET_GRACEFUL_SHUTDOWN,
                        node_cons.RESET_GRACEFUL_RESTART,
                        node_cons.RESET_FORCE_RESTART,
                        node_cons.RESET_FORCE_OFF,
                        node_cons.RESET_FORCE_ON,
                        node_cons.RESET_ON,
                        node_cons.RESET_NMI,
                        node_cons.RESET_PUSH_POWER_BUTTON])
        self.assertEqual(expected, values)
        self.assertIsInstance(values, set)
        self.assertEqual(1, mock_log.call_count)

    def test_reset_node(self):
        self.node_inst.reset_node(node_cons.RESET_FORCE_OFF)
        self.node_inst._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Node1/Actions/ComposedNode.Reset',
            data={'ResetType': 'ForceOff'})

    def test_reset_node_invalid_value(self):
        self.assertRaises(exceptions.InvalidParameterValueError,
                          self.node_inst.reset_node, 'invalid-value')

    def test_get_allowed_node_boot_source_values(self):
        values = self.node_inst.get_allowed_node_boot_source_values()
        expected = set([node_cons.BOOT_SOURCE_TARGET_NONE,
                        node_cons.BOOT_SOURCE_TARGET_PXE,
                        node_cons.BOOT_SOURCE_TARGET_HDD])
        self.assertEqual(expected, values)
        self.assertIsInstance(values, set)

    @mock.patch.object(node.LOG, 'warning', autospec=True)
    def test_get_allowed_node_boot_source_values_no_values_specified(
            self, mock_log):
        self.node_inst.boot.allowed_values = None
        values = self.node_inst.get_allowed_node_boot_source_values()
        # Assert it returns all values if it can't get the specific ones
        expected = set([node_cons.BOOT_SOURCE_TARGET_NONE,
                        node_cons.BOOT_SOURCE_TARGET_PXE,
                        node_cons.BOOT_SOURCE_TARGET_HDD])
        self.assertEqual(expected, values)
        self.assertIsInstance(values, set)
        self.assertEqual(1, mock_log.call_count)

    def test_set_node_boot_source(self):
        self.node_inst.set_node_boot_source(
            node_cons.BOOT_SOURCE_TARGET_PXE,
            enabled=node_cons.BOOT_SOURCE_ENABLED_CONTINUOUS,
            mode=node_cons.BOOT_SOURCE_MODE_UEFI)
        self.node_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Nodes/Node1',
            data={'Boot': {'BootSourceOverrideEnabled': 'Continuous',
                           'BootSourceOverrideTarget': 'Pxe',
                           'BootSourceOverrideMode': 'UEFI'}})

    def test_set_node_boot_source_no_mode_specified(self):
        self.node_inst.set_node_boot_source(
            node_cons.BOOT_SOURCE_TARGET_HDD,
            enabled=node_cons.BOOT_SOURCE_ENABLED_ONCE)
        self.node_inst._conn.patch.assert_called_once_with(
            '/redfish/v1/Nodes/Node1',
            data={'Boot': {'BootSourceOverrideEnabled': 'Once',
                           'BootSourceOverrideTarget': 'Hdd'}})

    def test_set_node_boot_source_invalid_target(self):
        self.assertRaises(exceptions.InvalidParameterValueError,
                          self.node_inst.set_node_boot_source,
                          'invalid-target')

    def test_set_node_boot_source_invalid_enabled(self):
        self.assertRaises(exceptions.InvalidParameterValueError,
                          self.node_inst.set_node_boot_source,
                          node_cons.BOOT_SOURCE_TARGET_HDD,
                          enabled='invalid-enabled')

    def test__get_processor_collection_path_missing_processors_attr(self):
        self.node_inst._json.pop('Processors')
        self.assertRaisesRegex(
            exceptions.MissingAttributeError, 'attribute Processors',
            self.node_inst._get_processor_collection_path)

    def test_memory_summary_missing_attr(self):
        # | GIVEN |
        self.node_inst._json['Memory']['Status'].pop('Health')
        # | WHEN |
        self.node_inst._parse_attributes()
        # | THEN |
        self.assertEqual(32, self.node_inst.memory_summary.size_gib)
        self.assertEqual(None, self.node_inst.memory_summary.health)

        # | GIVEN |
        self.node_inst._json['Memory'].pop('Status')
        # | WHEN |
        self.node_inst._parse_attributes()
        # | THEN |
        self.assertEqual(32, self.node_inst.memory_summary.size_gib)
        self.assertEqual(None, self.node_inst.memory_summary.health)

        # | GIVEN |
        self.node_inst._json['Memory'].pop('TotalSystemMemoryGiB')
        # | WHEN |
        self.node_inst._parse_attributes()
        # | THEN |
        self.assertEqual(None, self.node_inst.memory_summary.size_gib)
        self.assertEqual(None, self.node_inst.memory_summary.health)

        # | GIVEN |
        self.node_inst._json.pop('Memory')
        # | WHEN |
        self.node_inst._parse_attributes()
        # | THEN |
        self.assertEqual(None, self.node_inst.memory_summary)

    def test_processors(self):
        # check for the underneath variable value
        self.assertIsNone(self.node_inst._processors)
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/processor_collection.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_processors = self.node_inst.processors
        # | THEN |
        self.assertIsInstance(actual_processors,
                              processor.ProcessorCollection)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_processors,
                      self.node_inst.processors)
        self.conn.get.return_value.json.assert_not_called()

    def test_processors_on_refresh(self):
        # | GIVEN |
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/processor_collection.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.node_inst.processors,
                              processor.ProcessorCollection)

        # On refreshing the system instance...
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/node.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.node_inst.refresh()

        # | WHEN & THEN |
        self.assertIsNone(self.node_inst._processors)

        # | GIVEN |
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/processor_collection.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.node_inst.processors,
                              processor.ProcessorCollection)

    def _setUp_processor_summary(self):
        self.conn.get.return_value.json.reset_mock()
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/processor_collection.json',
                  'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        # fetch processors for the first time
        self.node_inst.processors

        successive_return_values = []
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/processor.json', 'r') as f:
            successive_return_values.append(json.loads(f.read()))
        with open('valenceclient/tests/unit/redfish/'
                  'json_samples/processor2.json', 'r') as f:
            successive_return_values.append(json.loads(f.read()))

        self.conn.get.return_value.json.side_effect = successive_return_values

    def test_processor_summary(self):
        # | GIVEN |
        self._setUp_processor_summary()
        # | WHEN |
        actual_processor_summary = self.node_inst.processors.summary
        # | THEN |
        self.assertEqual((16, node_cons.PROCESSOR_ARCH_x86),
                         actual_processor_summary)
        self.assertEqual(16, actual_processor_summary.count)
        self.assertEqual(node_cons.PROCESSOR_ARCH_x86,
                         actual_processor_summary.architecture)

        # reset mock
        self.conn.get.return_value.json.reset_mock()

        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_processor_summary,
                      self.node_inst.processors.summary)
        self.conn.get.return_value.json.assert_not_called()

    def test_delete_node(self):
        self.node_inst.delete_node()
        self.node_inst._conn.delete.assert_called_once()


class NodeCollectionTestCase(testtools.TestCase):

    def setUp(self):
        super(NodeCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('valenceclient/tests/unit/redfish/json_samples/'
                  'node_collection.json', 'r') as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        self.node_col = node.NodeCollection(
            self.conn, '/redfish/v1/Nodes', redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.node_col._parse_attributes()
        self.assertEqual('1.0.2', self.node_col.redfish_version)
        self.assertEqual('Composed Nodes Collection', self.node_col.name)
        self.assertEqual(('/redfish/v1/Nodes/Node1',),
                         self.node_col.members_identities)

    @mock.patch.object(node, 'Node', autospec=True)
    def test_get_member(self, mock_node):
        self.node_col.get_member('/redfish/v1/Nodes/Node1')
        mock_node.assert_called_once_with(
            self.node_col._conn, '/redfish/v1/Nodes/Node1',
            redfish_version=self.node_col.redfish_version)

    @mock.patch.object(node, 'Node', autospec=True)
    def test_get_members(self, mock_node):
        members = self.node_col.get_members()
        mock_node.assert_called_once_with(
            self.node_col._conn, '/redfish/v1/Nodes/Node1',
            redfish_version=self.node_col.redfish_version)
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))

    def test__get_compose_action_element(self):
        value = self.node_col._get_compose_action_element()
        self.assertEqual("/redfish/v1/Nodes/Actions/Allocate",
                         value.target_uri)

    def test_compose_node_no_properties(self):
        self.node_col.compose_node()
        self.node_col._conn.post.assert_called_once_with(
            '/redfish/v1/Nodes/Actions/Allocate', data={})
