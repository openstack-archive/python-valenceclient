# Copyright 2017 99cloud Inc.
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

import copy

import mock
import testtools

from valenceclient.common import base
from valenceclient.tests.unit import utils


TESTABLE_RESOURCE = {
    'uuid': '11111111-2222-3333-4444-555555555555',
    'attribute1': '1',
    'attribute2': '2',
}

CREATE_TESTABLE_RESOURCE = copy.deepcopy(TESTABLE_RESOURCE)
del CREATE_TESTABLE_RESOURCE['uuid']

INVALID_ATTRIBUTE_TESTABLE_RESOURCE = {
    'non-existent-attribute': 'blablabla',
    'attribute1': '1',
    'attribute2': '2',
}

UPDATED_TESTABLE_RESOURCE = copy.deepcopy(TESTABLE_RESOURCE)
NEW_ATTRIBUTE_VALUE = 'brand-new-attribute-value'
UPDATED_TESTABLE_RESOURCE['attribute1'] = NEW_ATTRIBUTE_VALUE

fake_responses = {
    '/redfish/v1/testableresources':
    {
        'GET': (
            {},
            {"testableresources": [TESTABLE_RESOURCE]},
        ),
        'POST': (
            {},
            CREATE_TESTABLE_RESOURCE,
        ),
    },
    '/redfish/v1/testableresources/%s' % TESTABLE_RESOURCE['uuid']:
    {
        'GET': (
            {},
            TESTABLE_RESOURCE,
        ),
        'DELETE': (
            {},
            None,
        ),
        'PATCH': (
            {},
            UPDATED_TESTABLE_RESOURCE,
        ),
    },

}


class TestableResource(base.Resource):
    def __repr__(self):
        return "<TestableResource %s>" % self._info


class TestableManager(base.CreateManager):
    resource_class = TestableResource
    _creation_attributes = ['attribute1', 'attribute2']
    _resource_name = 'testableresources'

    def _path(self, id=None):
        return ('/redfish/v1/testableresources/%s' % id if id
                else '/redfish/v1/testableresources')

    def get(self, testable_resource_id, fields=None):
        return self._get(resource_id=testable_resource_id,
                         fields=fields)

    def delete(self, testable_resource_id):
        return self._delete(resource_id=testable_resource_id)

    def update(self, testable_resource_id, patch):
        return self._update(resource_id=testable_resource_id,
                            patch=patch)


class ManagerTestCase(testtools.TestCase):

    def setUp(self):
        super(ManagerTestCase, self).setUp()
        self.api = utils.FakeAPI(fake_responses)
        self.manager = TestableManager(self.api)

    def test_create(self):
        resource = self.manager.create(**CREATE_TESTABLE_RESOURCE)
        expect = [
            ('POST',
             '/redfish/v1/testableresources',
             {},
             CREATE_TESTABLE_RESOURCE),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertTrue(resource)
        self.assertIsInstance(resource, TestableResource)

    def test__get(self):
        resource_id = TESTABLE_RESOURCE['uuid']
        resource = self.manager._get(resource_id)
        expect = [
            ('GET', '/redfish/v1/testableresources/%s' % resource_id,
             {}, None),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(resource_id, resource.uuid)
        self.assertEqual(TESTABLE_RESOURCE['attribute1'], resource.attribute1)

    def test__get_as_dict(self):
        resource_id = TESTABLE_RESOURCE['uuid']
        resource = self.manager._get_as_dict(resource_id)
        expect = [
            ('GET', '/redfish/v1/testableresources/%s' % resource_id,
             {}, None),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(TESTABLE_RESOURCE, resource)

    @mock.patch.object(base.Manager, '_get', autospec=True)
    def test__get_as_dict_empty(self, mock_get):
        mock_get.return_value = None
        resource_id = TESTABLE_RESOURCE['uuid']
        resource = self.manager._get_as_dict(resource_id)
        mock_get.assert_called_once_with(mock.ANY, resource_id, fields=None)
        self.assertEqual({}, resource)

    def test_get(self):
        resource = self.manager.get(TESTABLE_RESOURCE['uuid'])
        expect = [
            ('GET',
             '/redfish/v1/testableresources/%s' % TESTABLE_RESOURCE['uuid'],
             {},
             None),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(TESTABLE_RESOURCE['uuid'], resource.uuid)
        self.assertEqual(TESTABLE_RESOURCE['attribute1'], resource.attribute1)

    def test_update(self):
        patch = {'op': 'replace',
                 'value': NEW_ATTRIBUTE_VALUE,
                 'path': '/attribute1'}
        resource = self.manager.update(
            testable_resource_id=TESTABLE_RESOURCE['uuid'],
            patch=patch
        )
        expect = [
            ('PATCH',
             '/redfish/v1/testableresources/%s' % TESTABLE_RESOURCE['uuid'],
             {},
             patch),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(NEW_ATTRIBUTE_VALUE, resource.attribute1)

    def test_delete(self):
        resource = self.manager.delete(
            testable_resource_id=TESTABLE_RESOURCE['uuid']
        )
        expect = [
            ('DELETE',
             '/redfish/v1/testableresources/%s' % TESTABLE_RESOURCE['uuid'],
             {},
             None),
        ]
        self.assertEqual(expect, self.api.calls)
        self.assertIsNone(resource)
