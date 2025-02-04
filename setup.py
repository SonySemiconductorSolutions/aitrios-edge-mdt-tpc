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

from setuptools import setup, find_packages


def read_install_requires():
    print("Reading install requirements")
    return [r.split('\n')[0] for r in open('requirements.txt', 'r').readlines()]


setup(packages=find_packages(include=["ai_toolchain_tpc", "ai_toolchain_tpc.*"], exclude=["*tests*"]),
      install_requires=read_install_requires())
