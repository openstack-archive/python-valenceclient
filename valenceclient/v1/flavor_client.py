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


class Flavor(base.Resource):
    def __repr__(self):
        return "<Flavor %s>" % self._info


class FlavorClient(base.CreateManager):
    resource_class = Flavor
    _creation_attributes = ['name', 'properties']
    _resource_name = 'flavors'

    def list_flavors(self):
        return self._list(self._path())

    def create_flavor(self, request):
        return self.create(**request)

    def delete_flavor(self, flavor_id):
        self._delete(resource_id=flavor_id)

    def show_flavor(self, flavor_id):
        return self._get(resource_id=flavor_id)

    def update_flavor(self, flavor_id, request):
        return self._update(resource_id=flavor_id,
                            patch=request,
                            method='PATCH')
