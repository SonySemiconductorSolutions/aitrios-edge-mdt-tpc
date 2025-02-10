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
from typing import Callable

from edgemdt_tpc.data.imx500 import generate_imx500_tpc

# Device types.
IMX500 = 'imx500'

def generate_device_type(device_type: str) -> Callable:
    """
    Returns a dictionary containing schema version mappings for the target platform capabilities models of the specified
    device type.

    Args:
        device_type (str): The type of device for the target platform.

    Returns:
        dict: A dictionary containing the schema versions mappings.
    """

    # Organize all device types into device_type_dict.
    device_type_dict = {
        IMX500: generate_imx500_tpc
    }

    # Check if the device type is supported.
    assert device_type in device_type_dict, (f"Error: The specified device type '{device_type}' is not valid. "
                                             f"Available devices are: {', '.join(device_type_dict.keys())}. "
                                             "Please ensure you are using a supported device.")
    return device_type_dict[device_type]
