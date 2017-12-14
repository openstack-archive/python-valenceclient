#   Copyright 2017 NEC, Corp.
#
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

from valenceclient.common import base


class System(base.Resource):
    def __repr__(self):
        return "<System %s>" % self._info


class SystemClient(base.CreateManager):
    resource_class = System
    _creation_attributes = ['podm_id']
    _resource_name = 'systems'

    def list_systems(self, request):
        return self._list(self._path(), **request)

    def show_system(self, system_id, request):
        return self._get(resource_id=system_id, **request)
