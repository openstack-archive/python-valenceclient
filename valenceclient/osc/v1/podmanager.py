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
        obj = client.list_podmanagers()
        columns = ['uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at']
        return (columns, (utils.get_dict_properties(s, columns) for s in obj))


class CreatePodManager(command.ShowOne):
    _description = "Creates new podmanager"
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(CreatePodManager, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            required=True,
            help=('Name for the PodManager'))
        parser.add_argument(
            '--url',
            required=True,
            help=('URL of the PodManager'))
        parser.add_argument(
            '--driver',
            metavar='<driver>',
            default='redfishv1',
            help=("PodManager driver, default is 'redfishv1'"))
        parser.add_argument(
            '--auth-type',
            metavar='<auth_type>',
            choices=['basic'],
            default='basic',
            help=("PodManager authentication type, default is 'basic'"))
        parser.add_argument(
            '--username',
            required=True,
            metavar='<username>',
            help=('Username to connect to podmanager'))
        parser.add_argument(
            '--password',
            required=True,
            metavar='<password>',
            help=('Password to connect to podmanager'))
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        auth = [{
            "type": parsed_args.auth_type,
            "auth_items": {
                "username": parsed_args.username,
                "password": parsed_args.password,
            }
        }]

        req = {
            'name': parsed_args.name,
            'url': parsed_args.url,
            'driver': parsed_args.driver,
            'authentication': auth
        }

        client = self.app.client_manager.valence
        obj = client.create_podmanager(req)
        columns = ['uuid', 'name', 'url', 'driver', 'status', 'created_at',
                   'updated_at']
        return (columns, (utils.get_dict_properties(obj, columns)))


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
        for p in parsed_args.id:
            try:
                client.delete_podmanager(p)
            except Exception as e:
                count = count + 1
                self.log.error("podmanager %s deletion failed with error %s",
                               p, str(e))

        if count > 0:
            total = len(parsed_args.id)
            msg = (("%(result)s of %(total)s podmanagers(s) "
                    "failed to delete.") % {'result': count, 'total': total})
            raise exceptions.CommandError(msg)
