import importlib
from typing import Tuple, Optional

from model_compression_toolkit.target_platform_capabilities.schema.mct_current_schema import TargetPlatformCapabilities


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
    # latest of all tpc or only major?

    # Check for extended_version.
    parts = tpc_version.split("_")
    numeric_part = parts[0]
    extended_version = parts[1] if len(parts) > 1 else False

    # Extract the major version part (e.g., "1" from "1.7").
    major_version = str(int(float(numeric_part)))

    # Get versions that start with the major version.
    matching_versions = [v for v in version_dict if v.startswith(f"{major_version}.")]

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

    # Get the latest version using the custom sort key.
    latest_version = max(matching_versions, key=lambda v: float(v.split('_')[0]))  # Sort numerically

    if float(tpc_version.split('_')[0]) > float(latest_version.split('_')[0]):
        return None, (f"Error: Requested version TPC version '{tpc_version}' is not available. "
                      f"The latest version is {latest_version}.")

    # Return the latest version.
    return version_dict.get(latest_version), (f"Resolving TPC version '{tpc_version}' to the latest version: "
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
        '1.0': "ai_toolchain_tpc.data.imx_500.tpc_v1_0",
        '1.0_lut': "ai_toolchain_tpc.data.imx_500.tpc_v1_0_lut",
        '1.0_pot': "ai_toolchain_tpc.data.imx_500.tpc_v1_0_pot",
        '4.0': "ai_toolchain_tpc.data.imx_500.tpc_v4_0",
    }

    if tpc_version not in tpcs_dict:
        # Get the latest TPC version.
        tpc_version, msg = get_latest_version(tpcs_dict, tpc_version)

        assert tpc_version is not None, msg

        print(msg)

    tpc_func = importlib.import_module(tpcs_dict[tpc_version])
    return getattr(tpc_func, "get_tp_model")()
