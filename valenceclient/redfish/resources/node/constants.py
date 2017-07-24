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

# Values comes from the Redfish System json-schema 1.0.0:
# http://redfish.dmtf.org/schemas/v1/ComputerSystem.v1_0_0.json#/definitions/ComputerSystem  # noqa

# Reset action constants

RESET_ON = 'on'
RESET_FORCE_OFF = 'force off'
RESET_GRACEFUL_SHUTDOWN = 'graceful shutdown'
RESET_GRACEFUL_RESTART = 'graceful restart'
RESET_FORCE_RESTART = 'force restart'
RESET_NMI = 'nmi'
RESET_FORCE_ON = 'force on'
RESET_PUSH_POWER_BUTTON = 'push power button'

# Node PowerState constants

NODE_POWER_STATE_ON = 'on'
"""The system is powered on"""

NODE_POWER_STATE_OFF = 'off'
"""The system is powered off, although some components may continue to
   have AUX power such as management controller"""

NODE_POWER_STATE_POWERING_ON = 'powering on'
"""A temporary state between Off and On. This temporary state can
   be very short"""

NODE_POWER_STATE_POWERING_OFF = 'powering off'
"""A temporary state between On and Off. The power off action can take
   time while the OS is in the shutdown process"""

# Composed Node State constants

COMPOSED_NODE_STATE_ALLOCATING = 'allocating'
"""Allocating resources for node is in progress. Next state can be
   Allocated or Failed"""

COMPOSED_NODE_STATE_ALLOCATED = 'allocated'
"""Node resources have been allocated, but assembly not started yet.
   After ComposedNode.Assemble action state will progress to Assembling"""

COMPOSED_NODE_STATE_ASSEMBLING = 'assembling'
"""Assembly process initiated, but not finished yet. When assembly
   is done it will change into Assembled"""

COMPOSED_NODE_STATE_ASSEMBLED = 'assembled'
"""Node successfully assembled"""

COMPOSED_NODE_STATE_FAILED = 'failed'
"""Allocation or assembly process failed, or in runtime one of composing
   components was removed or transitioned in error state"""

# Boot source target constants

BOOT_SOURCE_TARGET_NONE = 'none'
"""Boot from the normal boot device"""

BOOT_SOURCE_TARGET_PXE = 'pxe'
"""Boot from the Pre-Boot EXecution (PXE) environment"""

BOOT_SOURCE_TARGET_HDD = 'hdd'
"""Boot from a hard drive"""

# Boot source mode constants

BOOT_SOURCE_MODE_LEGACY = 'legacy'
BOOT_SOURCE_MODE_UEFI = 'uefi'

# Boot source enabled constants

BOOT_SOURCE_ENABLED_ONCE = 'once'
BOOT_SOURCE_ENABLED_CONTINUOUS = 'continuous'
BOOT_SOURCE_ENABLED_DISABLED = 'disabled'

# Processor related constants
# Values comes from the Redfish Processor json-schema 1.0.0:
# http://redfish.dmtf.org/schemas/v1/Processor.v1_0_0.json

# Processor Architecture constants

PROCESSOR_ARCH_x86 = 'x86 or x86-64'
PROCESSOR_ARCH_IA_64 = 'Intel Itanium'
PROCESSOR_ARCH_ARM = 'ARM'
PROCESSOR_ARCH_MIPS = 'MIPS'
PROCESSOR_ARCH_OEM = 'OEM-defined'
