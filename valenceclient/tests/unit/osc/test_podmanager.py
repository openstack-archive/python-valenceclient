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
from valenceclient.v1 import podmanagers as podm


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
        resp = podm.PodManager(self, response)
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.podmanagers.create_podmanager = mocker
        cmd = podmanager.CreatePodManager(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = list(cmd.take_action(parsed_args))
        filtered = [('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                     'updated_at'),
                    ('test-id', 'test-podm', 'http://localhost', 'redfishv1',
                     'Offline', '2017-08-07 06:56:34 UTC',
                     '2017-08-28 06:56:34 UTC')]
        self.assertEqual(filtered, result)


class TestShowPodmanager(test_base.TestValenceClient):
    def test_show_podmanager(self):
        podmanager_id = "test-id"
        arglist = [podmanager_id]
        verifylist = [('id', podmanager_id), ]
        response = {"uuid": "test-id",
                    "name": "test-podm",
                    "url": "http://localhost",
                    "driver": "redfishv1",
                    "status": "Offline",
                    "created_at": "2017-08-07 06:56:34 UTC",
                    "updated_at": "2017-08-28 06:56:34 UTC"}
        resp = podm.PodManager(self, response)
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.podmanagers.show_podmanager = mocker
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
        self.valenceclient.podmanagers.delete_podmanager = mocker
        cmd = podmanager.DeletePodManagers(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        mocker.assert_called_with('test-id')
        self.assertIsNone(result)


class TestUpdatePodmanager(test_base.TestValenceClient):
    def test_update_podmanager(self):
        arglist = ['test_uuid', '--name', 'updatedName']
        verifylist = [('id', 'test_uuid'), ('name', 'updatedName')]
        response = {"uuid": "test-uuid",
                    "name": "updatedName",
                    "url": "http://localhost",
                    "driver": "redfishv1",
                    "status": "Offline",
                    "created_at": "2017-08-07 06:56:34 UTC",
                    "updated_at": "2017-08-28 06:56:34 UTC"}
        resp = podm.PodManager(self, response)
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.podmanagers.update_podmanager = mocker
        cmd = podmanager.UpdatePodManager(self.app, self.namespace)
        parsed_args = self.check_parser(cmd, arglist, verifylist)
        result = cmd.take_action(parsed_args)
        filtered = ('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                    'updated_at'),\
                   ('test-uuid', 'updatedName', 'http://localhost',
                    'redfishv1', 'Offline', '2017-08-07 06:56:34 UTC',
                    '2017-08-28 06:56:34 UTC')
        self.assertEqual(filtered, result)


class TestListPodmanager(test_base.TestValenceClient):
    def test_list_podmanager(self):
        response = [{"uuid": "test-id",
                     "name": "test-podm",
                     "url": "http://localhost",
                     "driver": "redfishv1",
                     "status": "Offline",
                     "created_at": "2017-08-07 06:56:34 UTC",
                     "updated_at": "2017-08-28 06:56:34 UTC"},
                    {"uuid": "test-id2",
                     "name": "test-podm2",
                     "url": "http://localhost2",
                     "driver": "redfishv12",
                     "status": "Offline",
                     "created_at": "2017-08-07 06:56:32 UTC",
                     "updated_at": "2017-08-28 06:56:32 UTC"}
                    ]
        resp = [podm.PodManager(self, res) for res in response]
        mocker = mock.Mock(return_value=resp)
        self.valenceclient.podmanagers.list_podmanagers = mocker
        cmd = podmanager.ListPodManagers(self.app, self.namespace)
        result = cmd.take_action(parsed_args=None)
        result_list = [result[0], list(result[1])]
        filtered = [('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                     'updated_at'),
                    [('test-id', 'test-podm', 'http://localhost', 'redfishv1',
                      'Offline', '2017-08-07 06:56:34 UTC',
                      '2017-08-28 06:56:34 UTC'),
                     ('test-id2', 'test-podm2', 'http://localhost2',
                      'redfishv12', 'Offline', '2017-08-07 06:56:32 UTC',
                      '2017-08-28 06:56:32 UTC')]
                    ]
        self.assertEqual(filtered, result_list)
