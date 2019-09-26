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

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass()
class Node:
    id: str
    additional_properties: Dict[str, Any]


@dataclass()
class ReadGroup(Node):
    R1: Path
    R2: Optional[Path] = None
    R1_md5: Optional[str] = None
    R2_md5: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.R1.exists():
            raise FileNotFoundError(str(self.R1))
        if self.R2 is not None:
            if not self.R2.exists():
                raise FileNotFoundError(str(self.R2))


@dataclass()
class Library(Node):
    readgroups: List[ReadGroup]
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class Sample(Node):
    libraries: List[Library]
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class SampleGroup:
    samples: List[Sample]
