#   Copyright 2017 Intel, Inc.
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

from valenceclient.common import http
from valenceclient.v1 import node_client
from valenceclient.v1 import podmanager


class Client(object):
    def __init__(self, **kwargs):
        self.http_client = http.HTTPClient(**kwargs)
        self.podmanagers = podmanager.PodManagersClient(self.http_client)
        self.nodes = node_client.NodeClient(self.http_client)
