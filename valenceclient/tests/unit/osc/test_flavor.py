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

from valenceclient.osc.v1 import flavors
from valenceclient.tests.unit.osc import test_base
from valenceclient.v1 import flavor_client


def _get_mocked_response():
    return {"created_at": "2017-08-31 11:54:13 UTC",
            "name": "flavor1",
            "properties": {
                "memory": {
                    "capacity_mib": "2000",
                    "type": "DDR3"
                },
                "processor": {
                    "model": "Intel",
                    "total_cores": "2"
                },
            },
            "updated_at": "2017-08-31 11:54:13 UTC",
            "uuid": "flavor_uuid"
            }


class TestCreateFlavor(test_base.TestValenceClient):
    def test_create_flavor(self):
        arglist = ['flavor1', '--memory', 'capacity_mib=2000',
                   '--memory', 'type=DDR3', '--processor', 'model=AMD',
                   '--processor', 'total_cores=2']

        verifylist = [
            ('name', 'flavor1'),
            ('memory', {'capacity_mib': '2000', 'type': 'DDR3'}),
            ('processor', {'model': 'AMD', 'total_cores': '2'}),
        ]

        response = flavor_client.Flavor(self, _get_mocked_response())
        mocker = mock.Mock(return_value=response)
        self.valenceclient.flavors.create_flavor = mocker
        cmd = flavors.CreateFlavor(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = _get_mocked_response()
        for key, value in zip(result[0], result[1]):
            self.assertEqual(value, filtered[key])


class TestShowFlavor(test_base.TestValenceClient):
    def test_show_flavor(self):
        arglist = ['flavor_uuid']
        verifylist = [
            ('id', 'flavor_uuid'),
        ]
        response = flavor_client.Flavor(self, _get_mocked_response())
        mocker = mock.Mock(return_value=response)
        self.valenceclient.flavors.show_flavor = mocker
        cmd = flavors.ShowFlavor(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('uuid', 'name', 'properties', 'created_at',
                     'updated_at'),
                    ('flavor_uuid', 'flavor1',
                     {"memory": {"capacity_mib": "2000", "type": "DDR3"},
                      "processor": {"model": "Intel", "total_cores": "2"},
                      },
                     '2017-08-31 11:54:13 UTC', '2017-08-31 11:54:13 UTC')]
        self.assertEqual(filtered, result)


class TestDeleteFlavor(test_base.TestValenceClient):
    def test_delete_flavor(self):
        arglist = ['test-id']
        verifylist = [('id', ['test-id']), ]
        mocker = mock.Mock(return_value=None)
        self.valenceclient.flavors.delete_flavor = mocker
        cmd = flavors.DeleteFlavors(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        mocker.assert_called_with('test-id')
        self.assertIsNone(result)


class TestListFlavor(test_base.TestValenceClient):
    def test_list_flavor(self):
        response = [
            {
                "created_at": "2017-11-21 06:34:39 UTC",
                "name": "flavorMemory",
                "properties": {
                    "memory": {
                        "capacity_mib": "2000",
                        "type": "DDR3"
                    }
                },
                "updated_at": "2017-11-22 05:26:41 UTC",
                "uuid": "test_uuid1"
            },
            {
                "created_at": "2017-10-09 05:36:43 UTC",
                "name": "flavorProcessor",
                "properties": {
                    "processor": {
                        "model": "Intel",
                        "total_cores": "2"
                    }
                },
                "updated_at": "2017-10-09 05:36:43 UTC",
                "uuid": "test_uuid2"
            }
        ]
        resp = [flavor_client.Flavor(self, res) for res in response]
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.flavors.list_flavors = mocker
        cmd = flavors.ListFlavors(self.app, self.namespace)
        result = cmd.take_action(parsed_args=None)
        result_list = [result[0], list(result[1])]
        filtered = [('uuid', 'name', 'properties', 'created_at', 'updated_at'),
                    [('test_uuid1', 'flavorMemory',
                      {"memory": {"capacity_mib": "2000", "type": "DDR3"}},
                      '2017-11-21 06:34:39 UTC', '2017-11-22 05:26:41 UTC'),
                     ('test_uuid2', 'flavorProcessor',
                      {"processor": {"model": "Intel", "total_cores": "2"}},
                      '2017-10-09 05:36:43 UTC', '2017-10-09 05:36:43 UTC')]]
        self.assertEqual(result_list, filtered)


class TestUpdateFlavor(test_base.TestValenceClient):
    def test_update_flavor(self):
        arglist = ['test-uuid', '--name', 'updatedName']
        verifylist = [('id', 'test-uuid'),
                      ('name', 'updatedName')]
        response = {
            "created_at": "2017-11-21 06:34:39 UTC",
            "name": "updatedName",
            "properties": {
                "processor": {
                    "model": "Intel",
                    "total_cores": "2"
                }
            },
            "updated_at": "2017-12-13 05:55:25 UTC",
            "uuid": "test-uuid"
        }
        resp = flavor_client.Flavor(self, response)
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.flavors.update_flavor = mocker
        cmd = flavors.UpdateFlavor(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        filtered = ('uuid', 'name', 'properties', 'created_at', 'updated_at'),\
                   ('test-uuid', 'updatedName',
                    {"processor": {"model": "Intel", "total_cores": "2"}},
                    '2017-11-21 06:34:39 UTC', '2017-12-13 05:55:25 UTC')
        self.assertEqual(filtered, result)
