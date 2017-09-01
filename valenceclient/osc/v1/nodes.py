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


class ListNodes(command.Lister):
    _description = "Lists all composed nodes"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ListNodes, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.list_nodes()
        columns = ('uuid', 'name', 'resource_uri', 'index')
        return (columns, (utils.get_dict_properties(s, columns) for s in obj))


class ComposeNode(command.ShowOne):
    _description = "Compose a Node - using flavor_id or properties"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ComposeNode, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=('Name for the Node'))
        parser.add_argument(
            '--flavor_id',
            metavar='<flavor_id>',
            help=('Uuid of flavor to attach to node'))
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
            '--podm_id',
            metavar='<podm_id>',
            help=('Uuid of podmanager'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        req = {}

        req['name'] = parsed_args.name

        if parsed_args.podm_id:
            req['podm_id'] = parsed_args.podm_id
        if parsed_args.flavor_id:
            req['flavor_id'] = parsed_args.flavor_id
        else:
            properties = {}
            if parsed_args.processor:
                properties['processor'] = parsed_args.processor
            if parsed_args.memory:
                properties['memory'] = parsed_args.memory
            req['properties'] = properties

        client = self.app.client_manager.valence
        obj = client.compose_node(req)
        columns = ('uuid', 'name', 'resource_uri', 'index')
        return (columns, (utils.get_dict_properties(obj, columns)))


class ShowNode(command.ShowOne):
    _description = "Lists composed nodes by id"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ShowNode, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<node_id>',
            help=('Uuid of node to display'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.list_node_by_id(parsed_args.id)
        columns = tuple(obj.keys())
        return (columns, (utils.get_dict_properties(obj, columns)))


class DeleteNodes(command.Command):
    _description = "Delete nodes"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(DeleteNodes, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            nargs='+',
            metavar='<node_id>',
            help=('Nodes id(s) to delete'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        count = 0
        for node_id in parsed_args.id:
            try:
                client.delete_node(node_id)
            except Exception as e:
                count = count + 1
                self.log.error("Node %s deletion failed with error %s",
                               node_id, str(e))

        if count > 0:
            total = len(parsed_args.id)
            msg = (("%(result)s of %(total)s nodes(s) "
                    "failed to delete.") % {'result': count, 'total': total})
            raise exceptions.CommandError(msg)


class ManageNode(command.ShowOne):
    _description = "Manage a Composed Node"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ManageNode, self).get_parser(prog_name)
        parser.add_argument(
            'node_index',
            metavar='<node_index>',
            help=('Index of node to be managed'))
        parser.add_argument(
            'podm_id',
            metavar='<podm_id>',
            help=('Uuid of podmanager'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        req = {
            'node_index': parsed_args.node_index,
            'podm_id': parsed_args.podm_id
        }

        client = self.app.client_manager.valence
        obj = client.manage_node(req)
        columns = ('uuid', 'name', 'resource_uri', 'index')
        return (columns, (utils.get_dict_properties(obj, columns)))
