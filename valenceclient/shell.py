# Copyright 2017 99cloud, Inc.
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


import argparse
import getpass
import logging
import sys

from oslo_utils import encodeutils
from oslo_utils import importutils

import six


import valenceclient
from valenceclient.client import Client
from valenceclient.common import cliutils
from valenceclient.common import http
from valenceclient.common.i18n import _
from valenceclient.common import utils
from valenceclient import exc

LAST_API_VERSION = ('1', 'latest')

class HelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        super(HelpFormatter, self).start_section(heading)


class ValenceShell(object):

    def get_base_parse(self):
        parser = argparse.ArgumentParser(
            prog='valence',
            epilog=_("See 'valence help COMMAND' for help on a "
                     "specified command."),
            add_help=False,
            formatter_class=HelpFormatter,
        )
        parser.add_argument('--help',
                            action='store_true',
                            help=argparse.SUPPRESS)
        # parser.add_argument('--version',
        #                    action='store_true',
        #                    help=valenceclient.__version__)
        parser.add_argument('--debug',
                            default=bool(cliutils.env('VALENCECLIENT_DEBUG')),
                            action='store_true',
                            help=_("Defaults to env[VALENCECLIENT_DEBUG]"))
        # parser.add_argument('--json',
        #                    default=True,
        #                    action='store_true',
        #                    help=_('Print JSON response without formatting.'))
        parser.add_argument('--valence-url',
                            action='store_true',
                            default=cliutils.env('OS_VALENCE_URL'),
                            help="Defaults to env[OS_VALENCE_URL]")

        parser.add_argument('--valence-api-version',
                            default=cliutils.env(
                                'VALENCE_API_VERSION', default='1'),
                            help=_('Accepts 1.x (where "x" is microversion) '
                                   'or "latest", Defaults to '
                                   'env[VALENCE_API_VERSION] or 1'))

        msg = _('Maximum number of retries in case of conflict error '
                '(HTTP 409). Defaults to env[VALENCE_MAX_RETRIES] or %d. '
                'Use 0 to disable retrying.') % http.DEFAULT_MAX_RETRIES
        parser.add_argument('--max-retries',
                            type=int,
                            help=msg,
                            default=cliutils.env(
                                'VALENCE_RETRY_INTERVAL',
                                default=int(http.DEFAULT_RETRY_INTERVAL)
                            ))
        msg = _('Amount of time (in seconds) between retries '
                'in case of conflict error (HTTP 409). '
                'Defaults to env[VALENCE_RETRY_INTERVAL] '
                'or %d.') % http.DEFAULT_RETRY_INTERVAL
        parser.add_argument('--retry-interval',
                            type=int,
                            help=msg,
                            default=cliutils.env(
                                'VALENCE_RETRY_INTERVAL',
                                default=str(http.DEFAULT_RETRY_INTERVAL)))
        return parser

    def get_subcommand_parse(self, version):
        parser = self.get_base_parse()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>',
                                           dest='subparse_name')

        submodule = importutils.import_versioned_module('valenceclient',
                                                        version,
                                                        'shell')
        submodule.enhance_parser(parser, subparsers, self.subcommands)

        utils.define_commands_from_module(subparsers, self, self.subcommands)
        return parser

    def _setup_debugging(self, debug):
        if debug:
            logging.basicConfig(
                format="%(levelname)s (%(module)s:%(lineno)d) %(message)s",
                level=logging.DEBUG
            )
        else:
            logging.basicConfig(
                format="%(levelname)s %(message)s",
                level=logging.CRITICAL
            )

    def do_bash_completion(self):
        """Prints all of the commands and options for bash-completion."""

        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in sc._optionals._option_string_actions.keys():
                options.add(option)

        commands.remove('bash-completion')

    def _check_version(self, api_version):
        if api_version == 'latest':
            return LAST_API_VERSION
        else:
            try:
                versions = tuple(int(i) for i in api_version.split('.'))
            except ValueError:
                versions = ()
            if len(versions) == 1:
                # Default value of valence_api_version is '1'.
                # If user not specify the value of api version, not passing
                # headers at all.
                os_valence_api_version = None
            elif len(versions) == 2:
                os_valence_api_version = api_version
                if versions[1] == 0:
                    os_valence_api_version = None
            else:
                msg = _("The requested API version %(ver)s is an unexpected "
                        "format. Acceptable formats are 'X', 'X.Y', or the "
                        "literal string '%(latest)s'."
                        ) % {'ver': api_version, 'latest': 'latest'}
                raise exc.CommandError(msg)

            api_major_version = versions[0]
            return (api_major_version, os_valence_api_version)

    @cliutils.arg('command', metavar='<subcommand>', nargs='?',
                  help=_('Display help for <subcommand>'))
    def do_help(self, args):
        """Display help about this program or one of its subcommands"""
        if getattr(args, 'command', None):
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError(_("'%s' is not valid subcommand")
                                       % args.command)
        else:
            self.parse.print_help()

    def main(self, argv):
        parser = self.get_base_parse()
        (options, args) = parser.parse_known_args(argv)
        self._setup_debugging(options.debug)

        (api_major_version, os_valence_api_version) = (
            self._check_version(options.valence_api_version))
        subcommand_parse = self.get_subcommand_parse(api_major_version)
        self.parse = subcommand_parse

        if options.help or not argv:
            self.do_help(options)
            return 0

        args = subcommand_parse.parse_args(argv)

        if args.func == self.do_help:
            self.do_help(args)
            return 0
        elif args.func == self.do_bash_completion():
            self.do_bash_completion()
            return 0
        if args.valence_url is None:
            raise exc.CommandError(_("You must provide an url via "
                                     "either --os-valence-url or via "
                                     "env[OS_VALENCE_URL]"))
        if args.max_retries < 0:
            raise exc.CommandError(_("You must provide value >= 0 for "
                                     "--max-retries"))
        if args.retry_interval < 1:
            raise exc.CommandError(_("You must provide value >= 1 for "
                                     "--retry-interval"))

        client_args = ('valence_url', 'max_retries', 'retry_interval')
        kwargs = {}
        for key in client_args:
            kwargs[key] = getattr(args, key)
        kwargs['os_valence_api_version'] = os_valence_api_version
        client = Client(args.valence_url,
                        os_valence_api_version,
                        args.max_retries,
                        args.retry_interval)
        try:
            args.func(client, args)
        except exc.CommandError as e:
            subcommand_parse = self.subcommands[args.subparse_name]
            subcommand_parse.error(e)


def main():
    try:
        ValenceShell().main(sys.argv[1:])
    except KeyboardInterrupt:
        print(_("... terminating valence client"), file=sys.stderr)
        return 130
    except Exception as e:
        print(encodeutils.safe_encode(six.text_type(e)), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
