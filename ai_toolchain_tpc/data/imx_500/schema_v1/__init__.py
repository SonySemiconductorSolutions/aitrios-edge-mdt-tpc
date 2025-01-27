from typing import Tuple, Optional

from model_compression_toolkit.target_platform_capabilities.schema.mct_current_schema import TargetPlatformCapabilities

from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v1_0 import get_tp_model as get_schema_v1_imx500_tp_model_v1_0
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v1_0_lut import get_tp_model as get_schema_v1_imx500_tp_model_v1_0_lut
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v1_0_pot import get_tp_model as get_schema_v1_imx500_tp_model_v1_0_pot
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v2_0 import get_tp_model as get_schema_v1_imx500_tp_model_v2_0
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v2_0_lut import get_tp_model as get_schema_v1_imx500_tp_model_v2_0_lut
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v3_0 import get_tp_model as get_schema_v1_imx500_tp_model_v3_0
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v3_0_lut import get_tp_model as get_schema_v1_imx500_tp_model_v3_0_lut
from ai_toolchain_tpc.data.imx_500.schema_v1.tpc_v4_0 import get_tp_model as get_schema_v1_imx500_tp_model_v4_0


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
    # TODO:
    # act only on ints?

    # Check for subversion.
    parts = tpc_version.split("_")
    numeric_part = parts[0]
    subversion = parts[1] if len(parts) > 1 else False

    # Extract the major version part (e.g., "1" from "1.7").
    major_version = str(int(float(numeric_part)))

    # Get versions that start with the major version
    matching_versions = [v for v in version_dict if v.startswith(f"{major_version}.")]

    # Only consider subversions if they are explicitly requested.
    if subversion:
        # If subversion is provided, filter versions that end with that subversion.
        matching_versions = [v for v in matching_versions if v.endswith(f"_{subversion}")]
    else:
        # If no subversion is provided, filter out any subversions.
        matching_versions = [v for v in matching_versions if "_" not in v]

    # If no matching versions, return None.
    if not matching_versions:
        return None, (f"Error: The specified TPC version '{tpc_version}' is not valid. "
                      f"Available versions are: {', '.join(version_dict.keys())}. "
                      "Please ensure you are using a supported version.")

    # Get the latest version using the custom sort key.
    latest_version = max(matching_versions, key=lambda v: float(v.split('_')[0]))  # Sort numerically

    if float(tpc_version.split('_')[0]) > float(latest_version.split('_')[0]):
        return None, (f"Error: Requested version TPC version '{tpc_version}' is not available. "
              f"The latest version is {latest_version}.")


    # Return the latest version.
    return version_dict.get(latest_version), (f"Resolving TPC version '{tpc_version}' to the latest version: "
                                              f"{latest_version}")


def generate_schema_v1_imx500_tpc(tpc_version: str) -> TargetPlatformCapabilities:
    """
    Retrieves target platform capabilities model based on the specified tpc version.

    Args:
        tpc_version (str): The version of the TPC to use.

    Returns:
        TargetPlatformCapabilities: The hardware configuration used for quantized model inference.
    """

    # Organize all tpc versions into tpcs_dict.
    tpcs_dict = {
        '1.0': get_schema_v1_imx500_tp_model_v1_0,
        '1.0_lut': get_schema_v1_imx500_tp_model_v1_0_lut,
        '1.0_pot': get_schema_v1_imx500_tp_model_v1_0_pot,
        '2.0': get_schema_v1_imx500_tp_model_v2_0,
        '2.0_lut': get_schema_v1_imx500_tp_model_v2_0_lut,
        '3.0': get_schema_v1_imx500_tp_model_v3_0,
        '3.0_lut': get_schema_v1_imx500_tp_model_v3_0_lut,
        '4.0': get_schema_v1_imx500_tp_model_v4_0,
    }

    if tpc_version in tpcs_dict:
        # Exact version provided.
        return tpcs_dict[tpc_version]()

    # Get the latest TPC version.
    tpc_version, msg = get_latest_version(tpcs_dict, tpc_version)

    assert tpc_version is not None, msg

    print(msg)

    return tpcs_dict[tpc_version]()
