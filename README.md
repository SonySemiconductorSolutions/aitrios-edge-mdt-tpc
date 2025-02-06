<div align="center" markdown="1">
<p>
      <a href="https://sony.github.io/model_optimization/" target="_blank">
        <img src="/docsrc/images/tpc_header.png" width="1000"></a>
</p>
  
______________________________________________________________________


<p align="center">
  <a href="https://sony.github.io/model_optimization#prerequisites"><img src="https://img.shields.io/badge/pytorch-2.1%20%7C%202.2%20%7C%202.3%20%7C%202.4%20%7C%202.5-blue" /></a>
  <a href="https://sony.github.io/model_optimization#prerequisites"><img src="https://img.shields.io/badge/TensorFlow-2.12%20%7C%202.13%20%7C%202.14%20%7C%202.15-blue" /></a>
  <a href="https://sony.github.io/model_optimization#prerequisites"><img src="https://img.shields.io/badge/python-3.9%20%7C3.10%20%7C3.11-blue" /></a>
  <a href="https://github.com/sony/model_optimization/releases"><img src="https://img.shields.io/github/v/release/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC" /></a>
  <a href="https://github.com/sony/model_optimization/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" /></a>
  
 </p>    
</div>

__________________________________________________________________________________________________________

## <div align="center">Getting Started</div>
### Quick Installation
To install the TPC package, ensure you have Python ≥ 3.9 with either PyTorch ≥ 2.1 or TensorFlow ≥ 2.12. Then, run:
```
pip install ai_toolchain_tpc 
```

### Using the TPC

To initialize a TPC and integrate it with MCT, use the `get_target_platform_capabilities` function as follows:

```python
from ai_toolchain_tpc import get_target_platform_capabilities
import model_compression_toolkit as mct

# Get a TPC object representing the imx500 hardware and use it for PyTorch model quantization in MCT
tpc = get_target_platform_capabilities(tpc_version='4', device_type='imx500')

# Apply MCT on your pre-trained model using the TPC
quantized_model, quantization_info = mct.ptq.pytorch_post_training_quantization(in_module=pretrained_model,
                                                                                representative_data_gen=dataset,
                                                                                target_resource_utilization=tpc)
```
Note: tpc_version = '4' will install the latest tpc version with minor version 4. for instance, if tpc 4.3 is available, calling tpc_version=4 will utilize 4.3. (If you wish to utilize a specific tpc version, please explicitly mention it, for instance tpc_version = '4.3'

### Supported Versions

| **IMX500 Converter version** | **Supported TPC versions** |
|------------------------------|-----------------|
| 3.16                         | v1, v4          |

### Tutorials

This basic MCT [tutorial](https://github.com/sony/model_optimization/blob/main/tutorials/notebooks/mct_features_notebooks/pytorch/example_pytorch_post_training_quantization.ipynb) section will walk you through the basics of the using the Device attributes tool and the TPC in particular for quantizing your model. 


## <div align="center">Target Platform Capabilities (TPC)</div>

### About 

TPC is our way of describing the hardware that will be used to run and infer with models that are optimized using the MCT.
The TPC includes different parameters that are relevant to the hardware during inference (e.g., number of bits used in some operator for its weights/activations, fusing patterns, etc.)

<div align="center" markdown="1">
<p>
      <a href="https://sony.github.io/model_optimization/" target="_blank">
        <img src="/docsrc/images/tpc_arch.png" width="400"></a>
</p>
</div>

The default target-platform model is [imx500tpc v1]((./tpc_models/imx500_tpc/v1/tpc.py)), quantizes activations using 8 bits with power-of-two thresholds for activations and symmetric threshold for weights.
For mixed-precision quantization it uses either 2, 4, or 8 bits for quantizing the operators.


## <div align="center">License</div>
Device Attributes package is licensed under Apache License Version 2.0. By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.

<a href="https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" /></a>
