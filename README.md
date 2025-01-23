<div align="center" markdown="1">
<p>
      <a href="https://sony.github.io/model_optimization/" target="_blank">
        <img src="/ai_toolchain_tpc/docsrc/images/tpc_header.png" width="1000"></a>
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

## <div align="center">Getting Started</div>
### Quick Installation
Pip install the Device Attributes package in a Python>=3.9 environment with PyTorch>=2.1 or Tensorflow>=2.12.
```
pip install tpc
```
For installing the nightly version or installing from source, refer to the [installation guide](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/blob/main/INSTALLATION.md).

**Important note**: In order to use TPC, you’ll need to have MCT installed on your machine. in case it's not installed - the lates MCT version will be automatically installed.

### Tutorials and Examples 

Our [tutorials](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/blob/main/tutorials/README.md) section will walk you through the basics of the Device attributes tool and the TPC in particular, covering various use cases. 

### Glossary:

- Schema - Defined by MCT - Defines the TPC modules and holds supported OPset to FW mapping.
- TPC model - A python file that is defined by TPC - describes edge device capabilities. 

## <div align="center">Target Platform Capabilities (TPC)</div>

### About 

TPC is our way of describing the hardware that will be used to run and infer with models that are optimized using the MCT.
The TPC includes different parameters that are relevant to the hardware during inference (e.g., number of bits used in some operator for its weights/activations, fusing patterns, etc.)

The default target-platform model is [imx500tpc v1]((./tpc_models/imx500_tpc/v1/tpc.py)), quantizes activations using 8 bits with power-of-two thresholds for activations and symmetric threshold for weights.
For mixed-precision quantization it uses either 2, 4, or 8 bits for quantizing the operators.

### Using the TPC

The simplest way to initiate a TPC and use it in MCT is by using the function `get_tpc` as follows:

```tpc_info = tpc.get_tpc(tpc_version, device_type, schema_version)```

>[!NOTE]
> - schema version is set to default in case you don't provide it <br>
> - tpc version is set to latest in case you don't provide it

For example:

```python
from tensorflow.keras.applications.mobilenet import MobileNet
import model_compression_toolkit as mct
import target_platform_capabilities as tpc
import numpy as np

# Get a TPC object that models the hardware for the quantized model inference.
# The model determines the quantization methods to use during the MCT optimization process.
# Here, we use the default (imx500) target-platform model attached to a Tensorflow
# layers representation.
tpc_info = tpc.get_tpc('imx500', 'default')

quantized_model, quantization_info = mct.ptq.keras_post_training_quantization(MobileNet(),
                                                                              lambda: [np.random.randn(1, 224, 224, 3)],
                                                                              # Random representative dataset 
                                                                              target_platform_capabilities=tpc_info)
```

## <div align="center">Contributions</div>
We'd love your input! Device Attributes would not be possible without help from our community, and welcomes contributions from anyone! 

*Checkout our [Contribution guide](https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/blob/main/CONTRIBUTING.md) for more details.

Thank you 🙏 to all our contributors!

## <div align="center">License</div>
Device Attributes package is licensed under Apache License Version 2.0. By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.

<a href="https://github.com/SonySemiconductorSolutions/IMX500-AI-Toolchain-TPC/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" /></a>
