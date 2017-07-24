# Copyright 2017 Intel, Inc.
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

from sushy import utils

from valenceclient.redfish.resources.node import constants as node_cons

RESET_NODE_VALUE_MAP = {
    'On': node_cons.RESET_ON,
    'ForceOff': node_cons.RESET_FORCE_OFF,
    'GracefulShutdown': node_cons.RESET_GRACEFUL_SHUTDOWN,
    'GracefulRestart': node_cons.RESET_GRACEFUL_RESTART,
    'ForceRestart': node_cons.RESET_FORCE_RESTART,
    'Nmi': node_cons.RESET_NMI,
    'ForceOn': node_cons.RESET_FORCE_ON,
    'PushPowerButton': node_cons.RESET_PUSH_POWER_BUTTON,
}

RESET_NODE_VALUE_MAP_REV = utils.revert_dictionary(RESET_NODE_VALUE_MAP)

NODE_POWER_STATE_MAP = {
    'On': node_cons.NODE_POWER_STATE_ON,
    'Off': node_cons.NODE_POWER_STATE_OFF,
    'PoweringOn': node_cons.NODE_POWER_STATE_POWERING_ON,
    'PoweringOff': node_cons.NODE_POWER_STATE_POWERING_OFF,
}

NODE_POWER_STATE_MAP_REV = utils.revert_dictionary(NODE_POWER_STATE_MAP)

COMPOSED_NODE_STATE_MAP = {
    'Allocating': node_cons.COMPOSED_NODE_STATE_ALLOCATING,
    'Allocated': node_cons.COMPOSED_NODE_STATE_ALLOCATED,
    'Assembling': node_cons.COMPOSED_NODE_STATE_ASSEMBLING,
    'Assembled': node_cons.COMPOSED_NODE_STATE_ASSEMBLED,
    'Failed': node_cons.COMPOSED_NODE_STATE_FAILED,
}

COMPOSED_NODE_STATE_MAP_REV = utils.revert_dictionary(COMPOSED_NODE_STATE_MAP)

BOOT_SOURCE_TARGET_MAP = {
    'None': node_cons.BOOT_SOURCE_TARGET_NONE,
    'Pxe': node_cons.BOOT_SOURCE_TARGET_PXE,
    'Hdd': node_cons.BOOT_SOURCE_TARGET_HDD,
}

BOOT_SOURCE_TARGET_MAP_REV = utils.revert_dictionary(BOOT_SOURCE_TARGET_MAP)

BOOT_SOURCE_MODE_MAP = {
    'Legacy': node_cons.BOOT_SOURCE_MODE_LEGACY,
    'UEFI': node_cons.BOOT_SOURCE_MODE_UEFI,
}

BOOT_SOURCE_MODE_MAP_REV = utils.revert_dictionary(BOOT_SOURCE_MODE_MAP)

BOOT_SOURCE_ENABLED_MAP = {
    'Once': node_cons.BOOT_SOURCE_ENABLED_ONCE,
    'Continuous': node_cons.BOOT_SOURCE_ENABLED_CONTINUOUS,
    'Disabled': node_cons.BOOT_SOURCE_ENABLED_DISABLED,
}

BOOT_SOURCE_ENABLED_MAP_REV = utils.revert_dictionary(BOOT_SOURCE_ENABLED_MAP)

PROCESSOR_ARCH_VALUE_MAP = {
    'x86': node_cons.PROCESSOR_ARCH_x86,
    'IA-64': node_cons.PROCESSOR_ARCH_IA_64,
    'ARM': node_cons.PROCESSOR_ARCH_ARM,
    'MIPS': node_cons.PROCESSOR_ARCH_MIPS,
    'OEM': node_cons.PROCESSOR_ARCH_OEM,
}

PROCESSOR_ARCH_VALUE_MAP_REV = (
    utils.revert_dictionary(PROCESSOR_ARCH_VALUE_MAP))
