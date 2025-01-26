# Copyright 2025 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from typing import Optional

from ai_toolchain_tpc.data import generate_device_type
from model_compression_toolkit.target_platform_capabilities.schema.mct_current_schema import TargetPlatformCapabilities


def get_target_platform_capabilities(tpc_version: str,
                                     device_type: str,
                                     schema_version: str = 'schema_v1',
                                     extended_version: Optional[str] = None) -> TargetPlatformCapabilities:
    """
    Retrieves target platform capabilities model based on the specified device type, schema version and tpc version.

    Args:
        tpc_version (str): The version of the TPC to use.
        device_type (str): The type of device for the target platform.
        schema_version (str): The schema version to use (default: 'schema_v1').
        extended_version (Optional[str]): An optional extended version identifier.

    Returns:
        TargetPlatformCapabilities: The hardware configuration used for quantized model inference.
    """

    # Generate a dictionary containing schemas configurations for the specified device type.
    device_dict = generate_device_type(device_type=device_type)

    # Generate a dictionary containing target platform configurations for the specified schema version.
    schema_dict = device_dict(schema_version=schema_version)

    # Add the extended version tag if existed.
    if extended_version is not None:
        tpc_version = tpc_version + '_' + extended_version

    # Get the target platform model for the tpc version.
    tpc = schema_dict(tpc_version=tpc_version)

    return tpc
