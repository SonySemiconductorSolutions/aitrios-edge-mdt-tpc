from V1 import generate_schema_v1_imx500_tpc

def generate_schema_imx500(schema_version):
    schema_dict = {
        'V1': generate_schema_v1_imx500_tpc
    }

    assert schema_version in schema_dict

    return schema_dict[schema_version]
