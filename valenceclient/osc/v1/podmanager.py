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


class ListPodManagers(command.Lister):
    _description = "Lists all registered podmanagers"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ListPodManagers, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.podmanagers.list_podmanagers()
        columns = ('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at')
        return (columns, (utils.get_item_properties(s, columns) for s in obj))


class CreatePodManager(command.ShowOne):
    _description = "Creates new podmanager"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(CreatePodManager, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=('Name for the PodManager'))
        parser.add_argument(
            'url',
            metavar='<url>',
            help=('URL of the PodManager'))
        parser.add_argument(
            '--driver',
            metavar='<driver>',
            default='redfishv1',
            help=("PodManager driver, default is 'redfishv1'"))
        parser.add_argument(
            '--auth',
            metavar='<key=value>',
            required=True,
            action=parseractions.KeyValueAction,
            help=("auth information to connect to podmanager, repeat option "
                  "to set each key. Accepted keys are type, username, password"
                  "If type not specified 'basic' is taken by default"))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        auth = parsed_args.auth
        auth['type'] = auth.get('type', 'basic')

        req = {
            'name': parsed_args.name,
            'url': parsed_args.url,
            'driver': parsed_args.driver,
            'authentication': [{'type': auth['type'],
                                'auth_items': {
                                    'username': auth['username'],
                                    'password': auth['password']}}]
        }

        client = self.app.client_manager.valence
        obj = client.podmanagers.create_podmanager(req)
        columns = ('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at')
        return (columns, (utils.get_item_properties(obj, columns)))


class DeletePodManagers(command.Command):
    _description = "Delete podmanagers"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(DeletePodManagers, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            nargs='+',
            metavar='<id>',
            help=('Podmanagers id(s) to delete'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        count = 0
        for podm_id in parsed_args.id:
            try:
                client.podmanagers.delete_podmanager(podm_id)
            except Exception as e:
                count = count + 1
                self.log.error("podmanager %s deletion failed with error %s",
                               podm_id, str(e))

        if count > 0:
            total = len(parsed_args.id)
            msg = (("%(result)s of %(total)s podmanagers(s) "
                    "failed to delete.") % {'result': count, 'total': total})
            raise exceptions.CommandError(msg)


class ShowPodManager(command.ShowOne):
    _description = "Show podmanager"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(ShowPodManager, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('Podmanager id to show'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.valence
        obj = client.podmanagers.show_podmanager(parsed_args.id)
        columns = ('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at')
        return (columns, (utils.get_item_properties(obj, columns)))


class UpdatePodManager(command.ShowOne):
    _description = "Update podmanager"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(UpdatePodManager, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('Podmanager id'))
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=('Name for the PodManager'))
        parser.add_argument(
            '--driver',
            metavar='<driver>',
            help=("PodManager driver"))
        parser.add_argument(
            '--auth',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=("auth information to connect to podmanager, repeat option "
                  "to set each key. Accepted keys are type, username, password"
                  "If type not specified 'basic' is taken by default"))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        req = {}
        if parsed_args.name:
            req['name'] = parsed_args.name
        if parsed_args.driver:
            req['driver'] = parsed_args.driver
        if parsed_args.auth:
            auth = parsed_args.auth
            auth['type'] = auth.get('type', 'basic')
            req['authentication'] = [{'type': auth['type'],
                                      'auth_items': {
                                          'username': auth['username'],
                                          'password': auth['password']}}]

        id = parsed_args.id
        client = self.app.client_manager.valence
        obj = client.podmanagers.update_podmanager(id, req)
        columns = ('uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at')
        return (columns, (utils.get_item_properties(obj, columns)))
