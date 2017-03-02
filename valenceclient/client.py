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

from oslo_utils import importutils
from valenceclient.common.http import DEFAULT_VERSION
from valenceclient import exc


def get_client(valence_url, max_retries=None, retry_interval=None):

    if valence_url is None:
        raise exc.InvalidValenceUrl

    kwargs = {
        'valence_url': valence_url,
        'max_retries': max_retries,
        'retry_interval': retry_interval
    }
    module = importutils.import_versioned_module('valenceclient',
                                                 DEFAULT_VERSION,
                                                 'client')
    client_class = getattr(module, 'Client')
    return client_class(**kwargs)
