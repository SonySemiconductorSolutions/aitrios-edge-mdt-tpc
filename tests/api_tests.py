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

import unittest
import importlib

import pytest

from edgemdt_tpc import get_target_platform_capabilities


class APIBaseTest:
    """
    Test to verify that the API returns the correct version number.
    """

    def __init__(self,
                 tpc_version,
                 device_type,
                 extended_version=None):
        self.tpc_version = tpc_version
        self.device_type = device_type
        self.extended_version = extended_version

    def get_tpc(self):
        return get_target_platform_capabilities(tpc_version=self.tpc_version,
                                                device_type=self.device_type,
                                                extended_version=self.extended_version)

    def run_test(self, expected_tpc_path, expected_tpc_version):
        tpc = self.get_tpc()
        expected_tpc_lib = importlib.import_module(expected_tpc_path)
        expected_tpc = getattr(expected_tpc_lib, "get_tp_model")()
        assert tpc == expected_tpc, f"Expected tpc_version to be {expected_tpc_version}"


class APITest(unittest.TestCase):
    def test_api_tpc_version(self):

        # TPC v1.0
        APIBaseTest(tpc_version='1.0', device_type="imx500").run_test(
            expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v1_0", expected_tpc_version='1.0')
        APIBaseTest(tpc_version='1', device_type="imx500").run_test(
            expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v1_0", expected_tpc_version='1.0')
        APIBaseTest(tpc_version='1.0', device_type="imx500", extended_version='lut').run_test(
            expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v1_0_lut", expected_tpc_version='1.0_lut')
        APIBaseTest(tpc_version='1', device_type="imx500", extended_version='lut').run_test(
            expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v1_0_lut", expected_tpc_version='1.0_lut')

        # TPC v4.0
        APIBaseTest(tpc_version='4.0', device_type="imx500").run_test(
            expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v4_0", expected_tpc_version='4.0')
        APIBaseTest(tpc_version='4', device_type="imx500").run_test(
            expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v4_0", expected_tpc_version='4.0')

    def test_api_false_tpc_version(self):

        # TPC v1.8
        with pytest.raises(AssertionError, match="Error: The specified TPC version '1.8' is not valid. Available "
                                                 "versions are: 1.0, 1.0_lut, 4.0. Please ensure you are requesting a"
                                                 " supported version."):
            APIBaseTest(tpc_version='1.8', device_type="imx500").run_test(
                expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v1_0", expected_tpc_version='1.8')

        # TPC v1.3
        with pytest.raises(AssertionError, match="Error: The specified TPC version '1.3' is not valid. Available "
                                                 "versions are: 1.0, 1.0_lut, 4.0. Please ensure you are requesting a"
                                                 " supported version."):
            APIBaseTest(tpc_version='1.3', device_type="imx500").run_test(
                expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v1_0", expected_tpc_version='1.3')

        # TPC v4.0_lut
        with pytest.raises(AssertionError, match="Error: The specified TPC version '4.0_lut' is not valid. Available "
                                                 "versions are: 1.0, 1.0_lut, 4.0. Please ensure you are "
                                                 "requesting a supported version."):
            APIBaseTest(tpc_version='4.0', device_type="imx500", extended_version='lut').run_test(
                expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v4_0", expected_tpc_version='4.0_lut')

        # Device type IMX400
        with pytest.raises(AssertionError, match="Error: The specified device type 'imx400' is not valid. Available "
                                                 "devices are: imx500. Please ensure you are using a supported "
                                                 "device."):
            APIBaseTest(tpc_version='1.0', device_type="imx400").run_test(
                expected_tpc_path="edgemdt_tpc.data.imx500.tpc_v4_0", expected_tpc_version='1.0')
