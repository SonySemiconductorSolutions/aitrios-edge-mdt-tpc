<div align="center" markdown="1">
<p>
      <a href="https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/" target="_blank">
        <img src="/docsrc/images/tpc_header.png" width="1000"></a>
</p>
  
______________________________________________________________________


<p align="center">
  <a href="https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/releases"><img src="https://img.shields.io/github/v/release/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC" /></a>
  <a href="https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" /></a>
 </p>    
</div>

__________________________________________________________________________________________________________

## <div align="center">Getting Started</div>
### Quick Installation
To install the TPC package, run:
```
pip install edgemdt_tpc 
```

**Important note**: To use TPC, you’ll need to have Model-Compression-Toolkit (MCT) installed on your machine. If MCT is not already installed, the latest version will be automatically installed.

### Using the TPC

To initialize a TPC and integrate it with MCT, use the `get_target_platform_capabilities` function as follows:

```python
from edgemdt_tpc import get_target_platform_capabilities
import model_compression_toolkit as mct

# Get a TPC object representing the imx500 hardware and use it for PyTorch model quantization in MCT
tpc = get_target_platform_capabilities(tpc_version='4.0', device_type='imx500')

# Apply MCT on your pre-trained model using the TPC
quantized_model, quantization_info = mct.ptq.pytorch_post_training_quantization(in_module=pretrained_model,
                                                                                representative_data_gen=dataset,
                                                                                target_resource_utilization=tpc)
```


## <div align="center">Supported Versions</div>

<details id="supported-versions">
  <summary>Supported Versions Table</summary>

|                       | TPC 1.0                                                                                                                                                                                                                                                          | TPC 4.0                                                                                                                                                                                                                                                            |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IMX500 Converter 3.14 | [![Run Tests](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/actions/workflows/run_tests_conv314_tpc10.yml/badge.svg)](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/actions/workflows/run_tests_conv314_tpc10.yml) | <p align="center"> Not supported </p>                                                                                                                                                                                                                              |
| IMX500 Converter 3.16 | [![Run Tests](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/actions/workflows/run_tests_conv316_tpc10.yml/badge.svg)](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/actions/workflows/run_tests_conv316_tpc10.yml) | [![Run Tests](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/actions/workflows/run_tests_conv316_tpc40.yml/badge.svg)](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/actions/workflows/run_tests_conv316_tpc40.yml) |

</details>

## <div align="center">Target Platform Capabilities (TPC)</div>

### About 

TPC is our way of describing the hardware that will be used to run and infer with models that are optimized using the MCT.
The TPC includes different parameters that are relevant to the hardware during inference (e.g., number of bits used in some operator for its weights/activations, fusing patterns, etc.)

<div align="center" markdown="1">
<p>
      <a href="https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/" target="_blank">
        <img src="/docsrc/images/tpc_arch.png" width="400"></a>
</p>
</div>

## <div align="center">License</div>
Device Attributes package is licensed under Apache License Version 2.0. By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.

<a href="https://github.com/SonySemiconductorSolutions/EdgeMDT-TPC/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" /></a>
