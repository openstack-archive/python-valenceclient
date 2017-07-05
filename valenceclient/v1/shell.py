from valenceclient.common import utils
from valenceclient.v1 import node_shell
from valenceclient.v1 import system_shell

COMMAND_MODULES = [
    node_shell,
    system_shell
]


def enhance_parser(parser, subparsers, cmd_mapper):
    """Enhance parser with API version specific options.
    Take a basic (nonversioned) parser and enhance it with
    commands and options specific for this version of API.
    :param parser: top level parser
    :param subparsers: top level parser's subparsers collection
                       where subcommands will go
    """
    for command_module in COMMAND_MODULES:
        utils.define_commands_from_module(subparsers, command_module,
                                          cmd_mapper)