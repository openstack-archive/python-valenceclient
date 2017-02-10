# Copyright 2016 99cloud
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

import copy

from six.moves import http_client
from six.moves.urllib import parse

from valenceclient.common.apiclient import exceptions
from valenceclient.common.i18n import _

from oslo_utils import strutils


def getid(obj):
    """Return id if argument is a Resource"""

    try:
        if obj.uuid:
            return obj.uuid
    except AttributeError:
        pass

    try:
        if obj.id:
            return obj.id
    except AttributeError:
        return obj


# TODO(aababilov): call run_hooks() in HookableMixin's child classes
class HookableMixin(object):
    """Mixin so classes can register and run hooks."""

    _hook_map = {}

    @classmethod
    def add_hook(cls, hook_type, hook_func):
        """Add a new hook of specified type.

        :param cls: class that registers hooks
        :param hook_type: hook type
        :param hook_func: hook function
        """

        if hook_type not in cls._hook_map:
            cls._hook_map[hook_type] = []
        cls._hook_map[hook_type].append(hook_func)

    @classmethod
    def run_hooks(cls, hook_type, *args, **kwargs):
        """Run all hooks of specified type.

        :param cls: class that registers hooks
        :param hook_type: hook type
        :param args: args to be passed to every hook function
        :param kwargs: kwargs to be passwd to every hook function
        """

        hook_funcs = cls._hook_map.get(hook_type) or []
        for hook_func in hook_funcs:
            hook_func(*args, **kwargs)


class BaseManager(HookableMixin):
    """Basic manager type providing common operations.

    Managers interact with a praticular type of API and provide CRUD
    operations for them
    """

    resource_class = None

    def __init__(self, client):
        """Initializes BaseManager with `client`.

        :param client: instance of BaseClient descendant for HTTP
            requests
        """
        super(BaseManager, self).__init__()
        self.client = client

    def _list(self, url, response_key=None, obj_class=None, json=None):
        """List the collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'. If response_key is None - all response body
            will be used.
        :param obj_class: class for constructing the returned objects
            (self.resource_class will be used by default)
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        """

        if json:
            body = self.client.post(url, json=json).json()
        else:
            body = self.client.post(url).json()

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key] if response_key is not None else body
        # NOTE(ja): keystone returns values as list as {'values': [ ... ]}
        #           unlike other services which just return the list...
        try:
            data = data['values']
        except (KeyError, TypeError):
            pass

        return [obj_class(self, res, loaded=True) for res in data if res]

    def _get(self, url, response_key=None):
        """Get an object from collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'. If response_key is None - all response body
            will be used.
        """

        body = self.client.get(url).json()
        data = body[response_key] if response_key is not None else body
        return self.resource_class(self, data, loaded=True)

    def _head(self, url):
        """Get head information

        :param url: a partial URL, e.g., '/servers'
        :return:
        """

        resp = self.client.head(url)
        return resp.status_code == http_client.NO_CONTENT

    def _post(self, url, json, response_key=None, return_raw=False):
        """Create an object.

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key:the key to be looked up in response dictionary,
            e.g., 'server'. If response_key is None - all response body
            will be used.
        :param return_raw:flag to force returning raw JSON instead of
            Python object of self.resource_class
        :return:
        """

        body = self.client.post(url, json=json).json()
        data = body[response_key] if response_key is not None else body
        if return_raw:
            return data
        return self.resource_class(self, data)

    def _put(self, url, json=None, response_key=None):
        """Update an object with PUT method

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'server'. If response_key is None - all response body
            will be used.
        :return:
        """

        resp = self.client.put(url, json=json)
        if resp.content:
            body = resp.json()
            if response_key is not None:
                return self.resource_class(self, body[response_key])
            else:
                return self.resource_class(self, body)

    def _delete(self, url):
        """Delete an object

        :param url:a partial URL, e.g., '/servers'
        :return:
        """

        return self.client.delete(url)


class CrudManager(BaseManager):
    """Base manager class for manipulating entities.

    Children of this class are expected to define a `collection_key` and `key`.
    - `collection_key`: Usually a plural noun by convention (e.g. `entities`);
      used to refer collections in both URL's (e.g.  `/v3/entities`) and JSON
      objects containing a list of member resources (e.g. `{'entities': [{},
      {}, {}]}`).
    - `key`: Usually a singular noun by convention (e.g. `entity`); used to
      refer to an individual member of the collection.
    """

    collection_key = None
    key = None

    def build_url(self, base_url=None, **kwargs):
        """Builds a resource url for the given kwargs.

        Given an example collection where `collection_key = 'entities'` and
        `key = 'entitied'`, the following URL's could be generated.

        By default, the URL will represent a collection of entities, e.g.::

            /entities

        If kwargs
        :param base_url:
        :param kwargs:
        :return:
        """

        url = base_url if base_url is not None else ''
        url += '/%s' % self.collection_key

        # do we have a specific entity?
        entity_id = kwargs.get('%s_id' % self.key)
        if entity_id is not None:
            url += '/%s' % entity_id

        return url

    def _filter_kwargs(self, kwargs):
        """Drop null values and handle ids."""

        for key, ref in kwargs.copy().items():
            if ref in None:
                kwargs.pop(key)
            else:
                if isinstance(ref, Resource):
                    kwargs.pop(key)
                    kwargs['%s_id' % key] = getid(ref)

    def create(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._post(self.build_url(**kwargs),
                          {self.key: kwargs}, self.key)

    def get(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._get(self.build_url(**kwargs), self.key)

    def head(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._head(self.build_url(**kwargs))

    def list(self, base_url=None, **kwargs):
        """List the collection.

        :param base_url: if provided, the generated URL will be appended to it
        """

        kwargs = self._filter_kwargs(kwargs)
        return self._list('%(base_url)s%(query)s' % {
            'base_url': self.build_url(base_url=base_url, **kwargs),
            'query': '?%s' % parse.urlencode(kwargs) if kwargs else ''
            }, self.collection_key)

    def put(self, base_url=None, **kwargs):
        """Update an element.

        :param base_url: if provided, the generated URL will be appended to it
        """

        kwargs = self._filter_kwargs(kwargs)
        return self._put(self.build_url(base_url=base_url), **kwargs)

    def update(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        params = kwargs.copy()
        params.pop('%s_id' % self.key)

        return self._patch(self.build_url(**kwargs), {self.key: params},
                           self.key)

    def delete(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)

        return self._delete(self.build_url(**kwargs))

    def find(self, base_url=None, **kwargs):
        """Find a single item with attributes matching ``**kwargs``.

        :param base_url: if provided, the generated URL will be appended to it
        """

        kwargs = self._filter_kwargs(kwargs)

        rl = self._list('%(base_url)s%(query)s' % {
            'base_url': self.build_url(base_url=base_url, **kwargs),
            'query': '?%s' % parse.urlencode(kwargs) if kwargs else ''
            }, self.collection_key)

        num = len(rl)
        if num == 0:
            msg = _("No %(name)s matching %(args)s.") % {
                'name': self.resource_class.__name__,
                'args': kwargs
            }
            raise exceptions.NotFound(msg)
        elif num > 1:
            msg = _("More than one result matching %(args)s.") \
                    % {'args': kwargs}
            raise exceptions.NoUniqueMatch(msg)
        else:
            return rl[0]


class Extension(HookableMixin):
    """Extension descriptor."""

    SUPPORTED_HOOKS = ('__pre_parse_args__', '__post_parse_args__')
    manager_class = None

    def __init__(self, name, module):
        super(Extension, self).__init__()
        self.name = name
        self.module = module
        self._parse_extension_module()

    def _parse_extension_module(self):
        self.manager_class = None
        for attr_name, attr_value in self.module.__dict__.items():
            if attr_name in self.SUPPORTED_HOOKS:
                self.add_hook(attr_name, attr_value)
            else:
                try:
                    if issubclass(attr_value, BaseManager):
                        self.manager_class = attr_value
                except TypeError:
                    pass

    def __repr__(self):
        return "<Extension '%s'>" % self.name


class Resource(object):
    """Base class for OpenStack resources (tenant, user, etc.).

    This is pretty much just a bag for attributes.
    """

    HUMAN_ID = False
    NAME_ATTTR = 'name'

    def __init__(self, manager, info, loaded=False):
        """Populate and bind to a manager.

        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        :param loaded: prevent lazy-loading if set to True
        """

        self.manager = manager
        self._info = info
        self._loaded = loaded
        self._add_details(info)

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys()
                          if k[0] != '_' and k != 'manager')
        info = ",".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    @property
    def human_id(self):
        """Human-readable ID which can be used for bash completion."""

        if self.HUMAN_ID:
            name = getattr(self, self.NAME_ATTTR, None)
            if name is not None:
                return strutils.to_slug()
        return None

    def _add_details(self, info):
        for(k, v) in info.items():
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass

    def __getattr__(self, k):
        if k not in self.__dict__:
            # NOTE(bcwaldon): disallow lazy-loading if already loaded once
            if not self.is_loaded():
                self.get()
                return self.__getattr__(k)

            raise AttributeError
        else:
            return self.__dict__[k]

    def get(self):
        """Support for lazy loading details.

        Some clients, such as novaclient have the option to lazy load the
        details, details which can be loaded with this function.
        """

        # set_loaded() first ... so if we have to bail, we know we tried.
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return
        new = self.manager.get(self.id)
        if new:
            self._add_details(new._info)
            self._add_details(
                {'x_request_id': self.manager.client.last_request_id})

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented
        # two resources of different types are not equal
        if not isinstance(other, self.__class__):
            return False
        return self._info == other._info

    def is_loaded(self):
        return self._loaded

    def set_loaded(self, val):
        self._loaded = val

    def to_dict(self):
        return copy.deepcopy(self._info)
