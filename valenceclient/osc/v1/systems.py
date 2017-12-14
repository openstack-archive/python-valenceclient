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

from osc_lib.command import command
from osc_lib import utils


class ListSystems(command.Lister):
    _description = "Lists all systems"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ListSystems, self).get_parser(prog_name)
        parser.add_argument(
            'podm_id',
            metavar='<podm_id>',
            help=('Uuid of podmanager'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        req = {'podm_id': parsed_args.podm_id}
        client = self.app.client_manager.valence
        obj = client.systems.list_systems(req)
        columns = tuple(obj[0].to_dict().keys())
        return (columns, (utils.get_item_properties(s, columns) for s in obj))


class ShowSystem(command.ShowOne):
    _description = "List system by id"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ShowSystem, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('Id of system to display'))
        parser.add_argument(
            'podm_id',
            metavar='<podm_id>',
            help=('Uuid of podmanager'))

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        req = {
            'podm_id': parsed_args.podm_id
        }
        client = self.app.client_manager.valence
        obj = client.systems.show_system(parsed_args.id, req)
        columns = tuple(obj.to_dict().keys())
        return (columns, (utils.get_item_properties(obj, columns)))
