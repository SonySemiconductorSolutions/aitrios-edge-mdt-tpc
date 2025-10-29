# Copyright 2025 Sony Semiconductor Solutions, Inc. All rights reserved.
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
from unittest.mock import Mock, patch
from edgemdt_tpc.data import IMX500
from model_compression_toolkit.wrapper.mct_wrapper import MCTWrapper
from model_compression_toolkit.wrapper.constants import TPC_VERSION, DEVICE_TYPE, EXTENDED_VERSION
from model_compression_toolkit.verify_packages import FOUND_TPC


@patch('edgemdt_tpc.get_target_platform_capabilities')
def test_get_tpc(mock_get_tpc):
    mock_tpc = Mock()
    mock_get_tpc.return_value = mock_tpc

    mct_wrapper = MCTWrapper()
    mct_wrapper.use_internal_tpc = False
    assert FOUND_TPC is True
    mct_wrapper._get_tpc()

    expected_params = {TPC_VERSION: mct_wrapper.params[TPC_VERSION],
                       DEVICE_TYPE: IMX500,
                       EXTENDED_VERSION: None}
    
    mock_get_tpc.assert_called_once_with(**expected_params)
    assert mct_wrapper.tpc == mock_tpc