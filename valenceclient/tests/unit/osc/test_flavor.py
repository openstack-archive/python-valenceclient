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
                "storage": {
                    "size_gib": "100",
                    "type": "ssd"
                }
            },
            "updated_at": "2017-08-31 11:54:13 UTC",
            "uuid": "flavor_uuid"
            }


class TestCreateFlavor(test_base.TestValenceClient):
    def test_create_flavor(self):
        arglist = ['flavor1', '--memory', 'capacity_mib=2000',
                   '--memory', 'type=DDR3', '--processor', 'model=AMD',
                   '--processor', 'total_cores=2', '--storage',
                   'size_gib=100', '--storage', 'type=ssd']

        verifylist = [
            ('name', 'flavor1'),
            ('memory', {'capacity_mib': '2000', 'type': 'DDR3'}),
            ('processor', {'model': 'AMD', 'total_cores': '2'}),
            ('storage', {'size_gib': '100', 'type': 'ssd'})
        ]

        mocker = mock.Mock(return_value=_get_mocked_response())
        self.valenceclient.create_flavor = mocker
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
        response = _get_mocked_response()
        mocker = mock.Mock(return_value=response)
        self.valenceclient.list_flavor_by_id = mocker
        cmd = flavors.ShowFlavor(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('uuid', 'name', 'properties', 'created_at',
                     'updated_at'),
                    ('flavor_uuid', 'flavor1',
                     {"memory": {"capacity_mib": "2000", "type": "DDR3"},
                      "processor": {"model": "Intel", "total_cores": "2"},
                      "storage": {"size_gib": "100", "type": "ssd"}
                      },
                     '2017-08-31 11:54:13 UTC', '2017-08-31 11:54:13 UTC')]
        self.assertEqual(filtered, result)


class TestDeleteFlavor(test_base.TestValenceClient):
    def test_delete_flavor(self):
        arglist = ['test-id']
        verifylist = [('id', ['test-id']), ]
        mocker = mock.Mock(return_value=None)
        self.valenceclient.delete_flavor = mocker
        cmd = flavors.DeleteFlavors(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        mocker.assert_called_with('test-id')
        self.assertIsNone(result)
