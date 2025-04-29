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
import importlib
from typing import Tuple, Optional

from model_compression_toolkit.target_platform_capabilities.schema.mct_current_schema import TargetPlatformCapabilities

# TPC versions.
V1 = '1.0'
V1_LUT = '1.0_lut'
V4 = '4.0'
V4_1 = '4.1'
V5 = '5.0'


def get_latest_version(version_dict: dict,
                       tpc_version: str) -> Tuple[Optional[str], str]:
    """
    Retrieves the relevant TPC version based on the requested TPC version. If only the major version is specified,
    the returned version will be the latest available.

    Args:
        version_dict (dict): Dictionary with all the available TPC versions.
        tpc_version (str): The version of the TPC to use.

    Returns:
        str: The tpc_version to be used for quantized model inference or None if no relevant version was found.
        str: The message explaining the result.
    """

    # Check for extended_version.
    parts = tpc_version.split("_")
    numeric_part = parts[0]
    extended_version = parts[1] if len(parts) > 1 else False

    # Check for integer.
    if not numeric_part.isdigit():
        return None, (f"Error: The specified TPC version '{tpc_version}' is not valid. "
                      f"Available versions are: {', '.join(version_dict.keys())}. "
                      "Please ensure you are requesting a supported version.")

    # Get versions that start with the major version.
    matching_versions = [v for v in version_dict if v.startswith(f"{numeric_part}.")]

    # Only consider extended_versions if they are explicitly requested.
    if extended_version:
        # If extended_version is provided, filter versions that end with that extended_version.
        matching_versions = [v for v in matching_versions if v.endswith(f"_{extended_version}")]
    else:
        # If no extended_version is provided, filter out any extended_versions.
        matching_versions = [v for v in matching_versions if "_" not in v]

    # If no matching versions, return None.
    if not matching_versions:
        return None, (f"Error: The specified TPC version '{tpc_version}' is not valid. "
                      f"Available versions are: {', '.join(version_dict.keys())}. "
                      "Please ensure you are requesting a supported version.")

    latest_version = max(matching_versions, key=lambda v: float(v.split('_')[0]))  # Sort numerically

    # Return the latest version.
    return latest_version, (f"Resolving TPC version '{tpc_version}' to the latest version: "
                            f"{latest_version}")


def generate_imx500_tpc(tpc_version: str) -> TargetPlatformCapabilities:
    """
    Retrieves target platform capabilities model based on the specified tpc version.

    Args:
        tpc_version (str): The version of the TPC to use.

    Returns:
        TargetPlatformCapabilities: The hardware configuration used for quantized model inference.
    """

    # Organize all tpc versions into tpcs_dict.
    tpcs_dict = {
        V1: "edgemdt_tpc.data.imx500.tpc_v1_0",
        V1_LUT: "edgemdt_tpc.data.imx500.tpc_v1_0_lut",
        V4: "edgemdt_tpc.data.imx500.tpc_v4_0",
        V4_1: "edgemdt_tpc.data.imx500.tpc_v4_1",
        V5: "edgemdt_tpc.data.imx500.tpc_v5_0",
    }

    if tpc_version not in tpcs_dict:
        # Get the latest TPC version.
        tpc_version, msg = get_latest_version(tpcs_dict, tpc_version)

        assert tpc_version is not None, msg

        print(msg)

    tpc_func = importlib.import_module(tpcs_dict[tpc_version])
    return getattr(tpc_func, "get_tp_model")()
