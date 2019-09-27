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

from .utils import file_md5sum


@dataclass()
class ReadGroup:
    """
    Contains the paths and md5sums to a forward read (R1) and reverse read
    (R2) for a lane in the sequencer.
    """
    id: str
    R1: str
    R2: Optional[str] = None
    R1_md5: Optional[str] = None
    R2_md5: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self):
        """
        Returns a dict with all of this readgroups properties. If R2, R1_md5
        and/or R2_md5 are None they are excluded from the dict. This is to
        prevent 'R2: null' fields in the JSON or YAML outputs.
        Additional properties are also added to the dict.
        :return:
        """
        rg_dict = {"id": self.id, "R1": self.R1}
        rg_dict.update(self.additional_properties)
        if self.R1_md5 is not None:
            rg_dict["R1_md5"] = self.R1_md5
        if self.R2 is not None:
            rg_dict["R2"] = self.R2
        if self.R2_md5 is not None:
            rg_dict["R2_md5"] = self.R2_md5
        return rg_dict

    def test_files_exist(self):
        if not Path(self.R1).exists():
            raise FileNotFoundError(self.R1)
        if self.R2 is not None:
            if not Path(self.R2).exists():
                raise FileNotFoundError(self.R2)

    def test_file_checksums(self):
        if self.R1_md5 is not None:
            read1_md5 = file_md5sum(Path(self.R1))
            if not read1_md5 == self.R1_md5:
                raise ValueError(
                    f"md5sum '{self.R1_md5}' not equal to '{read1_md5}' for "
                    f"file {self.R1}.")
        if self.R2 is not None and self.R2_md5 is not None:
            read2_md5 = file_md5sum(Path(self.R2))
            if not read2_md5 == self.R2_md5:
                raise ValueError(
                    f"md5sum '{self.R2_md5}' not equal to '{read2_md5}' for "
                    f"file {self.R2}.")


@dataclass()
class Library:
    """
    Contains all the sequenced readgroups for this sample library. A sample
    library is a preparation of the sample's DNA to be sequenced. This can
    happen on multiple lanes in the sequencer (readgroups).
    """
    id: str
    readgroups: List[ReadGroup] = field(default_factory=list)
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.readgroups)

    def __getitem__(self, item: int):
        return self.readgroups[item]

    def append_readgroup(self, readgroup: ReadGroup):
        """
        Append a readgroup to this library.
        :param readgroup: a Readgroup object.
        """
        if isinstance(readgroup, ReadGroup):
            self.readgroups.append(readgroup)
        else:
            raise TypeError("Only readgroup objects can be appended to the "
                            "library.")

    def test_files_exist(self):
        for readgroup in self:
            readgroup.test_files_exist()

    def test_file_checksums(self):
        for readgroup in self:
            readgroup.test_file_checksums()


@dataclass()
class Sample:
    """
    The biological sample and its libraries. While in theory you can have
    multiple preparations of the sample for sequencing (libraries) in practice
    there is usually only one.
    """
    id: str
    libraries: List[Library] = field(default_factory=list)
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.libraries)

    def __getitem__(self, item: int):
        return self.libraries[item]

    def append_library(self, library: Library):
        """
        Append a library to this sample
        :param library: a library object
        """
        if isinstance(library, Library):
            self.libraries.append(library)
        else:
            raise TypeError("Only library objects can be appended to the "
                            "sample.")

    def test_files_exist(self):
        for library in self:
            library.test_files_exist()

    def test_file_checksums(self):
        for library in self:
            library.test_file_checksums()


@dataclass()
class SampleGroup:
    """A group of samples that are analysed together"""
    samples: List[Sample] = field(default_factory=list)

    def __iter__(self):
        return iter(self.samples)

    def __getitem__(self, item: int):
        return self.samples[item]

    def append_sample(self, sample: Sample):
        """
        Append a sample object to the sample group.
        :param sample: a Sample object.
        """
        if isinstance(sample, Sample):
            self.samples.append(sample)
        else:
            raise TypeError("Only sample objects can be appended to the "
                            "samplegroup.")

    def test_files_exist(self):
        for sample in self:
            sample.test_files_exist()

    def test_file_checksums(self):
        for sample in self:
            sample.test_file_checksums()

    @classmethod
    def from_dict_of_dicts(cls, dict_of_dicts: Dict[str, Any]):
        """
        Converts a dictionary of dictionaries to a SampleGroup object.
        :param dict_of_dicts: the dict of dicts.
        """
        samplegroup = SampleGroup()
        # Additional properties are popped, so they are no longer part of
        # items in the dictionaries.
        for sample_id, sample_dict in dict_of_dicts.items():
            sample = Sample(
                sample_id,
                additional_properties=sample_dict.pop(
                    "additional_properties", {}))
            for lib_id, lib_dict in sample_dict.items():
                library = Library(
                    lib_id,
                    additional_properties=lib_dict.pop(
                        "additional_properties", {})
                )
                for rg_id, rg_dict in lib_dict.items():
                    library.append_readgroup(ReadGroup(
                        id=rg_id,
                        R1=rg_dict["R1"],
                        R1_md5=rg_dict.get("R1_md5", None),
                        R2=rg_dict.get("R2", None),
                        R2_md5=rg_dict.get("R2_md5", None),
                        additional_properties=rg_dict.get(
                            "additional_properties", {})
                    ))
                sample.append_library(library)
            samplegroup.append_sample(sample)
        return samplegroup
