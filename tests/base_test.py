import numpy as np
import os
import subprocess
import sys
import unittest
import pytest

from torchvision.models import mobilenet_v2

import model_compression_toolkit as mct

from ai_toolchain_tpc.get_tpc import get_target_platform_capabilities


class BaseModelTest:
    def __init__(self,
                 tpc_version,
                 converter_version,
                 schema_version,
                 device_type,
                 extended_version=None,
                 save_folder='./',
                 input_shape=(3, 224, 224),
                 batch_size=1,
                 num_calibration_iter=1,
                 num_of_inputs=1):
        self.tpc_version = tpc_version
        self.schema_version = schema_version
        self.device_type = device_type
        self.extended_version = extended_version
        self.converter_version = converter_version
        self.save_folder = save_folder
        self.input_shape = (batch_size,) + input_shape
        self.num_calibration_iter = num_calibration_iter
        self.num_of_inputs = num_of_inputs

    def get_input_shapes(self):
        return [self.input_shape for _ in range(self.num_of_inputs)]

    def generate_inputs(self):
        return [np.random.randn(*in_shape) for in_shape in self.get_input_shapes()]

    def representative_data_gen(self):
        for _ in range(self.num_calibration_iter):
            yield self.generate_inputs()

    def get_tpc(self):
        return get_target_platform_capabilities(tpc_version=self.tpc_version,
                                                device_type=self.device_type,
                                                schema_version=self.schema_version,
                                                extended_version=self.extended_version)

    def run_mct(self, tpc, float_model, onnx_path):
        quantized_model, _ = mct.ptq.pytorch_post_training_quantization(
            in_module=float_model,
            representative_data_gen=self.representative_data_gen,
            target_platform_capabilities=tpc)

        # Save ONNX model
        mct.exporter.pytorch_export_model(quantized_model, save_model_path=onnx_path,
                                          repr_dataset=self.representative_data_gen)

    def check_libs(self):
        # Check if Java is installed
        result = subprocess.run(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            from IPython.display import display, HTML
            display(
                HTML(
                    "<p style='color: red; font-weight: bold;'>Java is not installed. Please install Java 17 to proceed.</p>"))
            raise SystemExit("Stopping execution: Java is not installed.")

        # Check if IMX500 Converter is installed
        result = subprocess.run(["imxconv-pt", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            from IPython.display import display, HTML
            display(
                HTML(
                    "<p style='color: red; font-weight: bold;'>IMX500 Converter is not installed. Please install "
                    "imx500-converter[pt] to proceed.</p>"))
            raise SystemExit("Stopping execution: IMX500 Converter is not installed.")

        # Check which version of IMX500 Converter is installed
        installed_conv = result.stdout.split(' ')[-1].split('\n')[0]
        if installed_conv != self.converter_version:
            # TODO: install converter version
            print(f"The installed IMX500 converter version is {installed_conv}, which differs from the requested "
                  f"version {self.converter_version}.")

    def run_test(self, float_model):
        os.makedirs(self.save_folder, exist_ok=True)
        onnx_path = os.path.join(self.save_folder, 'qmodel.onnx')

        tpc = self.get_tpc()
        self.run_mct(tpc=tpc, float_model=float_model, onnx_path=onnx_path)

        # Check if Java and IMX500 Converter is installed
        self.check_libs()

        # Run IMX500 Converter
        cmd = ["imxconv-pt", "-i", onnx_path, "-o", self.save_folder, "--overwrite-output"]

        env_bin_path = os.path.dirname(sys.executable)
        os.environ["PATH"] = f"{env_bin_path}:{os.environ['PATH']}"
        env = os.environ.copy()

        subprocess.run(cmd, env=env, check=True)


class TPCTest(unittest.TestCase):
    def test_check_tpc_version(self):
        # TODO:
        # Get versions from main matrix.
        float_model = mobilenet_v2()
        save_folder = './mobilenet_pt'

        # TPC v1.0
        BaseModelTest(tpc_version='1.0', device_type="imx500", schema_version='schema_v1', converter_version='3.14.3',
                      save_folder=save_folder).run_test(float_model)
        BaseModelTest(tpc_version='1.0', device_type="imx500", schema_version='schema_v1', extended_version='lut',
                      converter_version='3.14.3', save_folder=save_folder).run_test(float_model)
        BaseModelTest(tpc_version='1.0', device_type="imx500", schema_version='schema_v1', extended_version='pot',
                      converter_version='3.14.3', save_folder=save_folder).run_test(float_model)

        # TPC v2.0
        BaseModelTest(tpc_version='2.0', device_type="imx500", schema_version='schema_v1', converter_version='3.14.3',
                      save_folder=save_folder).run_test(float_model)
        BaseModelTest(tpc_version='2.0', device_type="imx500", schema_version='schema_v1', extended_version='lut',
                      converter_version='3.14.3', save_folder=save_folder).run_test(float_model)

        # TPC v3.0
        BaseModelTest(tpc_version='3.0', device_type="imx500", schema_version='schema_v1', converter_version='3.14.3',
                      save_folder=save_folder).run_test(float_model)
        BaseModelTest(tpc_version='3.0', device_type="imx500", schema_version='schema_v1', extended_version='lut',
                      converter_version='3.14.3', save_folder=save_folder).run_test(float_model)

        # TPC v4.0
        BaseModelTest(tpc_version='4.0', device_type="imx500", schema_version='schema_v1', converter_version='3.14.3',
                      save_folder=save_folder).run_test(float_model)

    def test_false_versions(self):
        float_model = mobilenet_v2()
        save_folder = './mobilenet_pt'

        # TPC v1.8
        with pytest.raises(AssertionError, match="Error: Requested version TPC version '1.8' is not available. The "
                                                 "latest version is 1.0."):
            BaseModelTest(tpc_version='1.8', device_type="imx500", schema_version='schema_v1',
                          converter_version='3.14.3',
                          save_folder=save_folder).run_test(float_model)

        # TPC v4.0_lut
        with pytest.raises(AssertionError, match="Error: The specified TPC version '4.0_lut' is not valid. Available "
                                                 "versions are: 1.0, 1.0_lut, 1.0_pot, 2.0, 2.0_lut, 3.0, 3.0_lut, "
                                                 "4.0. Please ensure you are using a supported version."):
            BaseModelTest(tpc_version='4.0', device_type="imx500", schema_version='schema_v1', extended_version='lut',
                          converter_version='3.14.3',
                          save_folder=save_folder).run_test(float_model)

        # Device type IMX400
        with pytest.raises(AssertionError, match="Error: The specified device type 'imx400' is not valid. Available "
                                                 "devices are: imx500. Please ensure you are using a supported "
                                                 "device."):
            BaseModelTest(tpc_version='1.0', device_type="imx400", schema_version='schema_v1',
                          converter_version='3.14.3',
                          save_folder=save_folder).run_test(float_model)

        # Schema version schema_v4
        with pytest.raises(AssertionError, match="Error: The specified Schema version 'schema_v4' is not valid. "
                                                 "Available versions are: schema_v1. Please ensure you are using a "
                                                 "supported version."):
            BaseModelTest(tpc_version='1.0', device_type="imx500", schema_version='schema_v4',
                          converter_version='3.14.3',
                          save_folder=save_folder).run_test(float_model)

