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

import copy
import mock

from valenceclient.osc.v1 import systems
from valenceclient.tests.unit.osc import test_base
from valenceclient.v1 import system_client


def _get_mocked_response():
    return {"uuid": "system_uuid",
            "name": "system_1",
            "power_state": "off",
            "links": [
                {
                    "url": "http://localhost"
                }
            ],
            "description": "description",
            "health": "down",
            "chassis_id": "sled2",
            "assettag": "ComputeSystem",
            "url_id": "systems",
            "created_at": "2017-08-31 10:56:13 UTC",
            "updated_at": "2017-08-31 10:56:13 UTC"
            }


class TestShowSystem(test_base.TestValenceClient):
    def test_show_system(self):
        response = system_client.System(self, _get_mocked_response())
        arglist = ['system_uuid', 'podmanager_uuid']
        verifylist = [
            ('id', 'system_uuid'),
            ('podm_id', 'podmanager_uuid'),
        ]

        mocker = mock.Mock(return_value=response)
        self.valenceclient.systems.show_system = mocker
        cmd = systems.ShowSystem(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        # NOTE(Akhil): Due to ordering issue, can not be compared directly
        filtered = _get_mocked_response()
        for key, value in zip(result[0], result[1]):
            self.assertEqual(value, filtered[key])


class TestListSystem(test_base.TestValenceClient):
    def test_list_system(self):
        arglist = ['podmanager_uuid']
        verifylist = [
            ('podm_id', 'podmanager_uuid'),
        ]
        system1 = _get_mocked_response()
        system2 = copy.deepcopy(system1)
        system2['uuid'] = "system_uuid2"
        system2['name'] = "system_2"
        response = [system1, system2]
        resp = [system_client.System(self, res) for res in response]
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.systems.list_systems = mocker
        cmd = systems.ListSystems(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        result_list = [result[0], list(result[1])]
        self.assertEqual(sorted(result_list[0]), sorted(system1.keys()))
        self.assertEqual(sorted(result_list[1][0]), sorted(system1.values()))
        self.assertEqual(sorted(result_list[1][1]), sorted(system2.values()))
