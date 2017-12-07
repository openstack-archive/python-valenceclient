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


class PodManager(base.Resource):
    def __repr__(self):
        return "<PodManager %s>" % self._info


class PodManagersClient(base.CreateManager):
    resource_class = PodManager
    _creation_attributes = ['name', 'url', 'driver', 'authentication']
    _resource_name = 'pod_managers'

    def list_podmanagers(self):
        return self._list(self._path())

    def create_podmanager(self, request):
        return self.create(**request)

    def delete_podmanager(self, podm_id):
        self._delete(resource_id=podm_id)

    def show_podmanager(self, podm_id):
        return self._get(resource_id=podm_id)

    def update_podmanager(self, podm_id, request):
        return self._update(resource_id=podm_id,
                            patch=request,
                            method='PATCH')
