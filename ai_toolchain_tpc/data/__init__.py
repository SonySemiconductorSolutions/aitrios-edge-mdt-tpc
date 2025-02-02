from typing import Callable

from ai_toolchain_tpc.data.imx_500 import generate_imx500_tpc


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
        'imx500': generate_imx500_tpc
    }

    # Check if the device type is supported.
    assert device_type in device_type_dict, (f"Error: The specified device type '{device_type}' is not valid. "
                                             f"Available devices are: {', '.join(device_type_dict.keys())}. "
                                             "Please ensure you are using a supported device.")
    return device_type_dict[device_type]
