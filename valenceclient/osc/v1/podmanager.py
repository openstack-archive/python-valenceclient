#   Copyright 2017 Intel, Inc.
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

from osc_lib.command import command
from osc_lib import utils


class ListPodManagers(command.Lister):
    _description = "Lists all registered podmanagers"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ListPodManagers, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.list_podmanagers()
        columns = ['uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at']
        return (columns, (utils.get_dict_properties(s, columns) for s in obj))
