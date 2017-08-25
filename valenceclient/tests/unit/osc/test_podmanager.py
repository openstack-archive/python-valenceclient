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

from valenceclient.osc.v1 import podmanager
from valenceclient.tests.unit.osc import test_base


class TestCreatePodmanager(test_base.TestValenceClient):
    def test_create_podmanager(self):
        response = {"uuid": "test-id",
                    "name": "test-podm",
                    "url": "http://localhost",
                    "driver": "redfishv1",
                    "status": "Offline",
                    "created_at": "2017-08-07 06:56:34 UTC",
                    "updated_at": "2017-08-28 06:56:34 UTC"}

        arglist = ['test-podm', 'http://localhost',
                   '--auth', "username=user",
                   '--auth', "password=pass"]
        verifylist = [
            ('name', 'test-podm'),
            ('url', 'http://localhost'),
            ('auth', {'username': 'user', 'password': 'pass'}),

        ]

        mocker = mock.Mock(return_value=response)
        self.valenceclient.create_podmanager = mocker
        cmd = podmanager.CreatePodManager(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                     'updated_at'),
                    ('test-id', 'test-podm', 'http://localhost', 'redfishv1',
                     'Offline', '2017-08-07 06:56:34 UTC',
                     '2017-08-28 06:56:34 UTC')]
        self.assertEqual(filtered, result)


class TestShowPolicy(test_base.TestValenceClient):
    def test_show_policy(self):
        podmanager_id = "test-id"
        arglist = [podmanager_id]
        verifylist = [
            ('id', podmanager_id),
        ]
        response = {"uuid": "test-id",
                    "name": "test-podm",
                    "url": "http://localhost",
                    "driver": "redfishv1",
                    "status": "Offline",
                    "created_at": "2017-08-07 06:56:34 UTC",
                    "updated_at": "2017-08-28 06:56:34 UTC"}

        mocker = mock.Mock(return_value=response)
        self.valenceclient.show_podmanager = mocker
        cmd = podmanager.ShowPodManager(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                     'updated_at'),
                    ('test-id', 'test-podm', 'http://localhost', 'redfishv1',
                     'Offline', '2017-08-07 06:56:34 UTC',
                     '2017-08-28 06:56:34 UTC')]
        self.assertEqual(filtered, result)


class TestDeletePodmanager(test_base.TestValenceClient):
    def test_delete_podmanager(self):
        arglist = ['test-id']
        verifylist = [('id', ['test-id']), ]
        mocker = mock.Mock(return_value=None)
        self.valenceclient.delete_podmanager = mocker
        cmd = podmanager.DeletePodManagers(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        mocker.assert_called_with('test-id')
        self.assertIsNone(result)
