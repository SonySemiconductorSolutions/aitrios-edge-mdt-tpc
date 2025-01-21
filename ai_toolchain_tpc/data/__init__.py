from imx_500 import generate_schema_imx500
def generate_device_type(device_type):
    device_type_dict = {
        'imx500': generate_schema_imx500
    }

    assert device_type in device_type_dict

    return device_type_dict[device_type]
