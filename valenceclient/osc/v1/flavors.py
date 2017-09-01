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

from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils


class ListFlavors(command.Lister):
    _description = "Lists all flavors"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ListFlavors, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.list_flavors()
        columns = ('uuid', 'name', 'properties', 'created_at', 'updated_at')
        return (columns, (utils.get_dict_properties(s, columns) for s in obj))


class CreateFlavor(command.ShowOne):
    _description = "Create a Flavor"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(CreateFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=('Name for the flavor'))
        parser.add_argument(
            '--memory',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("Memory information, repeat option to set each key. "
                  "Accepted keys are type, capacity_mib"))
        parser.add_argument(
            '--processor',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("Processor information, repeat option to set each key. "
                  "Accepted keys are model, total_cores"))
        parser.add_argument(
            '--storage',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("Storage information, repeat option to set each key. "
                  "Accepted keys are type, size_gib"))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        properties = {}
        if parsed_args.processor:
            properties['processor'] = parsed_args.processor
        if parsed_args.memory:
            properties['memory'] = parsed_args.memory
        if parsed_args.storage:
            properties['storage'] = parsed_args.storage

        req = {
            'name': parsed_args.name,
            'properties': properties
        }

        client = self.app.client_manager.valence
        obj = client.create_flavor(req)
        columns = ('uuid', 'name', 'properties', 'created_at', 'updated_at')
        return (columns, (utils.get_dict_properties(obj, columns)))


class ShowFlavor(command.ShowOne):
    _description = "List flavor by id"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ShowFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('Uuid of flavor to display'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.list_flavor_by_id(parsed_args.id)
        columns = ('uuid', 'name', 'properties', 'created_at', 'updated_at')
        return (columns, (utils.get_dict_properties(obj, columns)))


class DeleteFlavors(command.Command):
    _description = "Delete flavors"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(DeleteFlavors, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            nargs='+',
            metavar='<id>',
            help=('Flavors id(s) to delete'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        count = 0
        for p in parsed_args.id:
            try:
                client.delete_flavor(p)
            except Exception as e:
                count = count + 1
                self.log.error("Flavor %s deletion failed with error %s",
                               p, str(e))

        if count > 0:
            total = len(parsed_args.id)
            msg = (("%(result)s of %(total)s flavors(s) "
                    "failed to delete.") % {'result': count, 'total': total})
            raise exceptions.CommandError(msg)


class UpdateFlavor(command.ShowOne):
    _description = "Update a Flavor"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(UpdateFlavor, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('Uuid of flavor to update'))
        parser.add_argument(
            '--name',
            help=('Name for the flavor'))
        parser.add_argument(
            '--memory',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("Memory information, repeat option to set each key. "
                  "Accepted keys are type, capacity_mib"))
        parser.add_argument(
            '--processor',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("Processor information, repeat option to set each key. "
                  "Accepted keys are model, total_cores"))
        parser.add_argument(
            '--storage',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("Storage information, repeat option to set each key. "
                  "Accepted keys are type, size_gib"))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        properties = {}
        if parsed_args.processor:
            properties['processor'] = parsed_args.processor
        if parsed_args.memory:
            properties['memory'] = parsed_args.memory
        if parsed_args.storage:
            properties['storage'] = parsed_args.storage

        req = {
            'name': parsed_args.name,
            'properties': properties
        }

        id = parsed_args.id
        client = self.app.client_manager.valence
        obj = client.update_flavor(id, req)
        columns = ('uuid', 'name', 'properties', 'created_at', 'updated_at')
        return (columns, (utils.get_dict_properties(obj, columns)))
