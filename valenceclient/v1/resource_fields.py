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

from valenceclient.common.i18n import _


class Resource(object):
    """Resource class
    This class is used to manage the various fields that a resource (e.g.
    Chassis, Node, Port) contains.  An individual field consists of a
    'field_id' (key) and a 'label' (value).  The caller only provides the
    'field_ids' when instantiating the object.
    Ordering of the 'field_ids' will be preserved as specified by the caller.
    It also provides the ability to exclude some of these fields when they are
    being used for sorting.
    """

    FIELDS = {
        'id': 'uuid',
        'uuid': 'id',
        'bmcmac': 'bmcmac',
        'bmcip': 'bmcip',
        'nw': 'nw',
        'location': 'location',
        'ram': 'ram',
        'storage': 'storage',
        'cpu': 'cpu',
        'arch': 'arch',
        'systemurl': 'systemurl'

    }

    def __init__(self, field_ids, sort_excluded=None):
        """Create a Resource object
        :param field_ids:  A list of strings that the Resource object will
                           contain.  Each string must match an existing key in
                           FIELDS.
        :param sort_excluded: Optional. A list of strings that will not be used
                              for sorting.  Must be a subset of 'field_ids'.
        :raises: ValueError if sort_excluded contains value not in field_ids
        """
        self._fields = tuple(field_ids)
        self._labels = tuple([self.FIELDS[x] for x in field_ids])
        if sort_excluded is None:
            sort_excluded = []
        not_existing = set(sort_excluded) - set(field_ids)
        if not_existing:
            raise ValueError(
                _("sort_excluded specified with value not contained in "
                  "field_ids.  Unknown value(s): %s") % ','.join(not_existing))
        self._sort_fields = tuple(
            [x for x in field_ids if x not in sort_excluded])
        self._sort_labels = tuple([self.FIELDS[x] for x in self._sort_fields])

    @property
    def fields(self):
        return self._fields

    @property
    def labels(self):
        return self._labels

    @property
    def sort_fields(self):
        return self._sort_fields

    @property
    def sort_labels(self):
        return self._sort_labels


NODE_DETAIL_RESOURCE = Resource(
    ['id',
     'uuid',
     'bmcmac',
     'bmcip',
     'nw',
     'location',
     'ram',
     'storage',
     'cpu',
     'arch',
     'systemurl'
     ])


NODE_RESOURCE = Resource(
    ['id',
     'uuid',
     'bmcip',
     'location',
     ])

SYSTEM_DETAIL_RESOURCE = Resource(
    ['id',
     'uuid',
     'bmcmac',
     'bmcip',
     'nw',
     'location',
     'ram',
     'storage',
     'cpu',
     'arch',
     ])


SYSTEM_RESOURCE = Resource(
    ['id',
     'uuid',
     'bmcip',
     'location',
     ])
