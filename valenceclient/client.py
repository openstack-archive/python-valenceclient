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

def get_client(os_username, os_password, os_valence_url=None,
               max_retries=None, retry_interval=None):


    kwargs = {
        'os_username': os_username,
        'os_password': os_password,
        'os_valence_url': os_valence_url,
        'max_retries': max_retries,
        'retry_interval': retry_interval
    }

    return Client(**kwargs)

def Client(**kwargs):
    module = importutils.import_versioned_module('valenceclient','client')
    client_class = getattr(module, 'Client')
    return client_class(**kwargs)




































































