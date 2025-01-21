from V1.tpc_v1_0 import get_tp_model as get_schema_v1_imx500_tp_model_v1_0
from tpc_v1_0_lut import get_tp_model as get_schema_v1_imx500_tp_model_v1_0_lut
from tpc_v1_0_pot import get_tp_model as get_schema_v1_imx500_tp_model_v1_0_pot
from tpc_v2_0 import get_tp_model as get_schema_v1_imx500_tp_model_v2_0
from tpc_v2_0_lut import get_tp_model as get_schema_v1_imx500_tp_model_v2_0_lut
from tpc_v3_0 import get_tp_model as get_schema_v1_imx500_tp_model_v3_0
from tpc_v3_0_lut import get_tp_model as get_schema_v1_imx500_tp_model_v3_0_lut
from tpc_v4_0 import get_tp_model as get_schema_v1_imx500_tp_model_v4_0

def generate_schema_v1_imx500_tpc(tpc_version):
    tpcs_dict = {
        'v1.0': get_schema_v1_imx500_tp_model_v1_0,
        'v1.0_lut': get_schema_v1_imx500_tp_model_v1_0_lut,
        'v1.0_pot': get_schema_v1_imx500_tp_model_v1_0_pot,
        'v2.0': get_schema_v1_imx500_tp_model_v2_0,
        'v2.0_lut': get_schema_v1_imx500_tp_model_v2_0_lut,
        'v3.0': get_schema_v1_imx500_tp_model_v3_0,
        'v3.0_lut': get_schema_v1_imx500_tp_model_v3_0_lut,
        'v4.0': get_schema_v1_imx500_tp_model_v4_0,
    }

    assert tpc_version in tpcs_dict

    return tpcs_dict[tpc_version]()
