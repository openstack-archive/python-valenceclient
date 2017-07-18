# Copyright 2012 Red Hat, Inc.
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

# W0603: Using the global statement
# W0621: Redefining name %s from outer scope
# pylint: disable=W0603,W0621

from __future__ import print_function

import getpass
import inspect
import json
import os
import sys
import textwrap

from oslo_utils import encodeutils
from oslo_utils import strutils
import prettytable
import six
from six import moves

from valenceclient.common.i18n import _


class MissingArgs(Exception):
    """Supplied arguments are not sufficient for calling a function."""
    def __init__(self, missing):
        self.missing = missing
        msg = _("Missing arguments: %s") % ", ".join(missing)
        super(MissingArgs, self).__init__(msg)


def validate_args(fn, *args, **kwargs):
    """Check that the supplied args are sufficient for calling a function.

    >>> validate_args(lambda a: None)
    Traceback (most recent call last):
        ...
    MissingArgs: Missing argument(s): a
    >>> validate_args(lambda a, b, c, d: None, 0, c=1)
    Traceback (most recent call last):
        ...
    MissingArgs: Missing argument(s): b, d

    :param fn: the function to check
    :param args: the positional arguments supplied
    :param kwargs: the keyword arguments supplied
    """
    argspec = inspect.getargspec(fn)

    num_defaults = len(argspec.defaults or [])
    required_args = argspec.args[:len(argspec.args) - num_defaults]

    def isbound(method):
        return getattr(method, '__self__', None) is not None

    if isbound(fn):
        required_args.pop(0)

    missing = [arg for arg in required_args if arg not in kwargs]
    missing = missing[len(args):]
    if missing:
        raise MissingArgs(missing)


def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def env(*args, **kwargs):
    """Returns the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(func, 'arguments'):
        func.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in func.arguments:
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.arguments.insert(0, (args, kwargs))


def print_list(objs, fields, formatters=None, sortby_index=0,
               mixed_case_fields=None, field_labels=None, json_flag=False):
    """Print a list of objects or dict as a table, one row per object or dict.

    :param objs: iterable of :class:`Resource`
    :param fields: attributes that correspond to columns, in order
    :param formatters: `dict` of callables for field formatting
    :param sortby_index: index of the field for sorting table rows
    :param mixed_case_fields: fields corresponding to object attributes that
        have mixed case names (e.g., 'serverId')
    :param field_labels: Labels to use in the heading of the table, default to
        fields.
    :param json_flag: print the list as JSON instead of table
    """
    def _get_name_and_data(field):
        if field in formatters:
            # The value of the field has to be modified.
            # For example, it can be used to add extra fields.
            return (field, formatters[field](o))

        field_name = field.replace(' ', '_')
        if field not in mixed_case_fields:
            field_name = field.lower()
        if isinstance(o, dict):
            data = o.get(field_name, '')
        else:
            data = getattr(o, field_name, '')
        return (field_name, data)

    formatters = formatters or {}
    mixed_case_fields = mixed_case_fields or []
    field_labels = field_labels or fields
    if len(field_labels) != len(fields):
        raise ValueError(_("Field labels list %(labels)s has different number "
                           "of elements than fields list %(fields)s"),
                         {'labels': field_labels, 'fields': fields})

    if sortby_index is None:
        kwargs = {}
    else:
        kwargs = {'sortby': field_labels[sortby_index]}
    pt = prettytable.PrettyTable(field_labels)
    pt.align = 'l'

    json_array = []

    for o in objs:
        row = []
        for field in fields:
            row.append(_get_name_and_data(field))
        if json_flag:
            json_array.append(dict(row))
        else:
            pt.add_row([r[1] for r in row])

    if json_flag:
        print(json.dumps(json_array, indent=4, separators=(',', ': ')))
    elif six.PY3:
        print(encodeutils.safe_encode(pt.get_string(**kwargs)).decode())
    else:
        print(encodeutils.safe_encode(pt.get_string(**kwargs)))


def print_dict(dct, dict_property="Property", wrap=0, dict_value='Value',
               json_flag=False):
    """Print a `dict` as a table of two columns.

    :param dct: `dict` to print
    :param dict_property: name of the first column
    :param wrap: wrapping for the second column
    :param dict_value: header label for the value (second) column
    :param json_flag: print `dict` as JSON instead of table
    """
    if json_flag:
        print(json.dumps(dct, indent=4, separators=(',', ': ')))
        return
    pt = prettytable.PrettyTable([dict_property, dict_value])
    pt.align = 'l'
    for k, v in sorted(dct.items()):
        # convert dict to str to check length
        if isinstance(v, dict):
            v = six.text_type(v)
        if wrap > 0:
            v = textwrap.fill(six.text_type(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, six.string_types) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            pt.add_row([k, v])

    if six.PY3:
        print(encodeutils.safe_encode(pt.get_string()).decode())
    else:
        print(encodeutils.safe_encode(pt.get_string()))


def get_password(max_password_prompts=3):
    """Read password from TTY."""
    verify = strutils.bool_from_string(env("OS_VERIFY_PASSWORD"))
    pw = None
    if hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
        # Check for Ctrl-D
        try:
            for __ in moves.range(max_password_prompts):
                pw1 = getpass.getpass("OS Password: ")
                if verify:
                    pw2 = getpass.getpass("Please verify: ")
                else:
                    pw2 = pw1
                if pw1 == pw2 and pw1:
                    pw = pw1
                    break
        except EOFError:
            pass
    return pw


def service_type(stype):
    """Adds 'service_type' attribute to decorated function.

    Usage:

    .. code-block:: python

       @service_type('volume')
       def mymethod(f):
       ...
    """
    def inner(f):
        f.service_type = stype
        return f
    return inner


def get_service_type(f):
    """Retrieves service type from function."""
    return getattr(f, 'service_type', None)


def pretty_choice_list(l):
    return ', '.join("'%s'" % i for i in l)


def exit(msg=''):
    if msg:
        print(msg, file=sys.stderr)
    sys.exit(1)
