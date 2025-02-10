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

from edgemdt_tpc.data import generate_device_type, IMX500
from model_compression_toolkit.target_platform_capabilities.schema.mct_current_schema import TargetPlatformCapabilities


def get_target_platform_capabilities(tpc_version: str,
                                     device_type: str = IMX500,
                                     extended_version: Optional[str] = None) -> TargetPlatformCapabilities:
    """
    Retrieves target platform capabilities model based on the specified device type and tpc version.

    Args:
        tpc_version (str): The version of the TPC to use.
        device_type (str): The type of device for the target platform.
        extended_version (Optional[str]): An optional extended version identifier.

    Returns:
        TargetPlatformCapabilities: The hardware configuration used for quantized model inference.
    """
    tpc_version = str(tpc_version)

    # Generate a dictionary containing tpcs configurations for the specified device type.
    device_dict = generate_device_type(device_type=device_type)

    # Add the extended version tag if existed.
    if extended_version is not None:
        tpc_version = tpc_version + '_' + extended_version

    # Get the target platform model for the tpc version.
    tpc = device_dict(tpc_version=tpc_version)

    return tpc
