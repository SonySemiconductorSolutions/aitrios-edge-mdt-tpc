from typing import Callable

from ai_toolchain_tpc.data.imx_500.schema_v1 import generate_schema_v1_imx500_tpc


def generate_schema_imx500(schema_version: str) -> Callable:
    """
    Returns a dictionary containing target platform capabilities models mappings of the specified schema version.

    Args:
        schema_version (str): The schema version for the target platform.

    Returns:
        dict: A dictionary containing the target platform capabilities mappings.
    """

    # Organize all schema versions into schema_dict.
    schema_dict = {
        'schema_v1': generate_schema_v1_imx500_tpc
    }

    # Check if the schema version is supported.
    assert schema_version in schema_dict, (f"Error: The specified Schema version '{schema_version}' is not valid. "
                                           f"Available versions are: {', '.join(schema_dict.keys())}. "
                                           "Please ensure you are using a supported version.")

    return schema_dict[schema_version]
