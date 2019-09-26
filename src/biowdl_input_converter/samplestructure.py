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
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass()
class Node:
    """Generic code that is common between all Nodes"""
    id: str


@dataclass()
class ReadGroup(Node):
    R1: Path
    R2: Optional[Path] = None
    R1_md5: Optional[str] = None
    R2_md5: Optional[str] = None
    # We need to define additional_properties again because the order in
    # dataclasses is determined by order in the code.
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Check if files exist.
        This method is activated after the generated init."""
        if not self.R1.exists():
            raise FileNotFoundError(str(self.R1))
        if self.R2 is not None:
            if not self.R2.exists():
                raise FileNotFoundError(str(self.R2))


@dataclass()
class Library(Node):
    readgroups: List[ReadGroup]
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.readgroups)


@dataclass()
class Sample(Node):
    libraries: List[Library]
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.libraries)


@dataclass()
class SampleGroup:
    samples: List[Sample]

    def __iter__(self):
        return iter(self.samples)

    @classmethod
    def from_yaml(cls, yaml_file: Path):
        """
        Converts BioWDL samplesheets to SampleGroup
        :param yaml_file: Path to a yaml file
        :return: a SampleGroup class
        """
        with yaml_file.open("r") as yaml_h:
            samplesheet_dict = yaml.safe_load(yaml_h)

        # We iterate through all levels of the dictionary here. pop() is used
        # here because it removes properties we know exist. Additional
        # properties remain. These are added as is.
        samples = []
        for sample in samplesheet_dict["samples"]:  # type: Dict[str, Any]
            libraries = []
            for library in sample.pop("libraries"):  # type: Dict[str, Any]
                readgroups = []
                for readgroup in library.pop("readgroups"):  # type: Dict[str, Any]  # noqa: E501
                    read_struct = readgroup.pop("reads")  # type: Dict[str, str]  # noqa: E501
                    readgroups.append(ReadGroup(
                        id=readgroup.pop("id"),
                        R1=Path(read_struct.pop("R1")),
                        R1_md5=read_struct.pop("R1_md5", None),
                        R2=Path(read_struct.pop("R2")),
                        R2_md5=read_struct.pop("R2_md5"),
                        additional_properties=readgroup
                    ))
                libraries.append(Library(
                    id=library.pop("id"),
                    readgroups=readgroups,
                    additional_properties=library
                ))
            samples.append(Sample(
                id=sample.pop("id"),
                libraries=libraries,
                additional_properties=sample
            ))

        return SampleGroup(samples)
