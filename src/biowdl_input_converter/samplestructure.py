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
Create a fixed sample structure that can be used as a stable intermediate
between conversions. This way we don't have to write any to any conversions.

Dataclasses are used to create this structure. Dataclasses generate an
__init__, __repr__, __eq__ and more for you. They make writing this module
easier.
See this excellent talk on dataclasses,
https://www.youtube.com/watch?v=T-TwcmT6Rcw, or the python docs,
https://docs.python.org/3/library/dataclasses.html, for more information.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass()
class Node:
    """Generic code that is common between all Nodes"""
    id: str


@dataclass()
class ReadGroup(Node):
    R1: str
    R2: Optional[str] = None
    R1_md5: Optional[str] = None
    R2_md5: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class Library(Node):
    readgroups: List[ReadGroup]
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.readgroups)

    def __getitem__(self, item: int):
        return self.readgroups[item]


@dataclass()
class Sample(Node):
    libraries: List[Library]
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.libraries)

    def __getitem__(self, item: int):
        return self.libraries[item]


@dataclass()
class SampleGroup:
    samples: List[Sample]

    def __iter__(self):
        return iter(self.samples)

    def __getitem__(self, item: int):
        return self.samples[item]

    @classmethod
    def from_dict_of_dicts(cls, dict_of_dicts: Dict[str, Any]):
        samples = []
        for sample_id, sample_dict in dict_of_dicts.items():
            libraries = []
            for lib_id, lib_dict in sample_dict.items():
                readgroups = []
                for rg_id, rg_dict in lib_dict.items():
                    readgroups.append(ReadGroup(
                        id=rg_id,
                        R1=rg_dict["R1"],
                        R1_md5=rg_dict.get("R1_md5", None),
                        R2=rg_dict.get("R2", None),
                        R2_md5=rg_dict.get("R2_md5", None),
                        additional_properties=rg_dict.get(
                            "additional_properties", {})
                    ))
                libraries.append(Library(
                    id=lib_id,
                    readgroups=readgroups,
                    additional_properties=lib_dict.get(
                        "additional_properties", {})
                ))
            samples.append(Sample(
                id=sample_id,
                libraries=libraries,
                additional_properties=sample_dict.get(
                    "additional_properties", {})
            ))
        return SampleGroup(samples)
