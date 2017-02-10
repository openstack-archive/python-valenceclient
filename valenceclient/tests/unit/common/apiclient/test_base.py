# Copyright 2016 99cloud, Inc.
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


from oslotest import base as test_base
from valenceclient.common.apiclient import base


class TestBase(test_base.BaseTestCase):

    def test_resource_repr(self):
        r = base.Resource(None, dict(foo="bar", baz="spam"))
        self.assertEqual("<Resource baz=spam, foo=bar>", repr(r))

    def test_getid(self):
        self.assertEqual(4, base.getid(4))

        class TmpObject(object):
            id = 4
        self.assertEqual(4, base.getid(TmpObject))
