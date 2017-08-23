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

"""OpenStackClient plugin for RSD(Rack Scale Design)."""

import logging

from osc_lib import utils

LOG = logging.getLogger(__name__)

DEFAULT_API_VERSION = '1'
API_VERSION_OPTION = 'os_valence_api_version'
API_NAME = 'valence'
API_VERSIONS = {
    '1': 'valenceclient.v1.client.Client',
}


def make_client(instance):
    """Returns a rsd client."""
    valence_client = utils.get_client_class(API_NAME,
                                            instance._api_version[API_NAME],
                                            API_VERSIONS)

    LOG.debug('Instantiating Valence client: %s', valence_client)

    client = valence_client(
        valence_api_version=instance._cli_options.valence_api_version,
        valence_url=instance._cli_options.valence_api_url)
    return client


def build_option_parser(parser):
    """Hook to add global options"""

    parser.add_argument(
        '--valence-api-version',
        metavar='<rsd-api-version>',
        default=utils.env(
            'VALENCE_API_VERSION',
            default=DEFAULT_API_VERSION),
        help='VALENCE API version, default=' +
             DEFAULT_API_VERSION +
             ' (Env: VALENCE_API_VERSION)')
    parser.add_argument(
        '--valence-api-url',
        metavar='<valence-api-url>',
        default='http://localhost:8181/',
        help='The base URL to Valence Server')
    return parser
