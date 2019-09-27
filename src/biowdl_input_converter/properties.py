# Copyright (c) 2019 Leiden University Medical Center
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module contains the PipelineProperties object.
This module can be used later to contain the code that determines which
properties are present in required in the pipelines. Be it in python code,
or by reading in YAML configs that are included in the package (or not).
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass()
class PipelineProperties:
    """
    sample, library and readgroup are of Dict[str, bool]. The str ID notes
    the name of the property and the bool whether it is required.
    """
    sample: Dict[str, bool] = field(default_factory=list)
    library: Dict[str, bool] = field(default_factory=list)
    readgroup: Dict[str, bool] = field(default_factory=list)
