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

"""
Base utilities to build API operation managers and objects on top of
"""

import abc
import copy
import six
from valenceclient.common.apiclient import base
from valenceclient import exc


def getid(obj):
    """Wrapper to get object's ID

    Abstracts the common pattern of allowing both an object or an
    object's ID (UUID) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return obj


@six.add_metaclass(abc.ABCMeta)
class Manager(object):
    """Provides CRUD operations with a particular API."""

    def __init__(self, api):
        self.api = api

    def _path(self, resource_id=None):
        """Return a request path for a given resource identifier.

        :param resource_id: identifier of the resource to generate the request
            path
        """
        return ('/v1/%s/%s' % (self._resource_name, resource_id) if
                resource_id else '/v1/%s' % self._resource_name)

    @abc.abstractproperty
    def resource_class(self):
        """The resource class"""

    @abc.abstractproperty
    def _resource_name(self):
        """The resource name"""

    def _get(self, resource_id, fields=None, **kwargs):
        """Retrieve a resource.

        :param resource_id: Identifier of the resource.
        :param fields: List of specific fields to be returned.
        """

        if fields is not None:
            resource_id = '/%s' % resource_id
            resource_id += ','.join(fields)

        try:
            return self._list(self._path(resource_id), **kwargs)[0]
        except ValueError:
            return None

    def _get_as_dict(self, resource_id, fields=None):
        """Retrieve a resource as a dictionary

        :param resource_id: Identifier of the resource.
        :param fields: List of specific fields to be returned.
        :returns: a dictionary representing the resource; may be empty
        """

        resource = self._get(resource_id, fields=fields)
        if resource:
            return resource.to_dict()
        else:
            return {}

    def _list(self, url, obj_class=None, **kwargs):
        resp, body = self.api.json_request('GET', url, **kwargs)
        if obj_class is None:
            obj_class = self.resource_class

        if not isinstance(body, list):
            body = [body]

        return [obj_class(self, res, loaded=True) for res in body if res]

    def _update(self, resource_id, patch, method='PATCH'):
        """Update a resource.

        :param resource_id: Resource identifier.
        :param patch: New version of a given resource.
        :param method: Name of the method for the request.
        """

        url = self._path(resource_id)
        resp, body = self.api.json_request(method, url, body=patch)
        # PATCH/PUT requests may not return a body
        if body:
            return self.resource_class(self, body)

    def _delete(self, resource_id):
        """Delete a resource.

        :param resource_id: Resource identifier.
        """
        self.api.json_request('DELETE', self._path(resource_id))

    def _manage(self, path, **request):
        """Manage a resource

        :param path: api path to manage resource
        :param request: A dictionary containing attributes to manage resource
        :return: A managed resource
        """
        url = self._path() + path
        resp, body = self.api.json_request('POST', url, **request)
        if body:
            return self.resource_class(self, body)


@six.add_metaclass(abc.ABCMeta)
class CreateManager(Manager):
    """Provides creation operations with a particular API."""

    @abc.abstractproperty
    def _creation_attributes(self):
        """A list of required creation attributes for a resource type"""

    def create(self, **kwargs):
        """Create a resource based on a kwargs dictionary of attributes.

        :param kwargs: A dictionary containing the attributes of the resource
                       that will be created.
        :raises exc.InvalidAttribution: For invalid attributes that are not
                                      needed to create the resource.
        """
        new = {}
        invalid = []
        for (key, value) in kwargs.items():
            if key in self._creation_attributes:
                new[key] = value
            else:
                invalid.append(key)
        if invalid:
            raise exc.InvalidAttribution(
                'The attribution(s) "%s(attrs)s" are invalid:  they are not '
                'needed to create %(resource)s.' %
                {'resource': self._resource_name,
                 'attrs': '","'.join(invalid)})

        url = self._path()
        resp, body = self.api.json_request('POST', url, body=new)
        if body:
            return self.resource_class(self, body)


class Resource(base.Resource):
    """Represents a particular instance of an object (tenant, user, etc).

    This is pretty much just a bag for attributes.
    """

    def to_dict(self):
        return copy.deepcopy(self._info)
