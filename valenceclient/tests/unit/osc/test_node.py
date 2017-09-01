#   Copyright 2017 NEC, Corp.
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

import mock

from valenceclient.osc.v1 import nodes
from valenceclient.tests.unit.osc import test_base


class TestComposeNode(test_base.TestValenceClient):
    def test_compose_node(self):
        response = {"index": "xxxxxx",
                    "links": [
                        {
                            "url": "http://localhost"
                        }
                    ],
                    "name": "test_node",
                    "uuid": "test_id"
                    }

        arglist = ['test_node',
                   '--flavor_id', "test_fav_id",
                   '--podm_id', "test_podm_id"]
        verifylist = [
            ('name', 'test_node'),
            ('flavor_id', 'test_fav_id'),
            ('podm_id', 'test_podm_id')
        ]

        mocker = mock.Mock(return_value=response)
        self.valenceclient.compose_node = mocker
        cmd = nodes.ComposeNode(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('uuid', 'name', 'links', 'index'),
                    ('test_id', 'test_node', [{'url': 'http://localhost'}],
                     'xxxxxx')]
        self.assertEqual(filtered, result)


class TestShowNode(test_base.TestValenceClient):
    @staticmethod
    def _get_mocked_response():
        return {"boot_source": "hdd",
                "created_at": "2017-08-31 10:56:13 UTC",
                "health_status": "ok",
                "description": "testDesc",
                "index": "000000",
                "links": [
                    {
                        "url": "http://localhost"
                    }
                ],
                "name": "node1",
                "node_power_state": "on",
                "node_state": "Allocated",
                "podm_id": "podm_uuid",
                "target_boot_source": "pxe",
                "updated_at": "2017-08-31 10:56:13 UTC",
                "uuid": "node_uuid",
                "pooled_group_id": "xxxxxx"
                }

    def test_show_node(self):
        arglist = ['node_uuid']
        verifylist = [
            ('id', 'node_uuid'),
        ]
        response = self._get_mocked_response()
        mocker = mock.Mock(return_value=response)
        self.valenceclient.list_node_by_id = mocker
        cmd = nodes.ShowNode(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        filtered = self._get_mocked_response()
        # NOTE(Akhil): Due to ordering issue, can not be compared directly
        for key, value in zip(result[0], result[1]):
            self.assertEqual(value, filtered[key])


class TestDeleteNode(test_base.TestValenceClient):
    def test_delete_node(self):
        arglist = ['test-id']
        verifylist = [('id', ['test-id']), ]
        mocker = mock.Mock(return_value=None)
        self.valenceclient.delete_node = mocker
        cmd = nodes.DeleteNodes(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        mocker.assert_called_with('test-id')
        self.assertIsNone(result)
