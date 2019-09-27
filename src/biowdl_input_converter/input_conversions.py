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

from pathlib import Path
from typing import Any, Dict

import yaml

from .samplestructure import Library, ReadGroup, Sample, SampleGroup
from .utils import csv_to_dict_generator


def biowdl_yaml_to_samplegroup(yaml_file: Path) -> SampleGroup:
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
    samplegroup = SampleGroup()
    for sample_dict in samplesheet_dict["samples"]:  # type: Dict[str, Any]
        sample = Sample(id=sample_dict.pop("id"))
        for lib_dict in sample_dict.pop("libraries"):  # type: Dict[str, Any]
            library = Library(id=lib_dict.pop("id"))
            for rg_dict in lib_dict.pop("readgroups"):  # type: Dict[str, Any]
                read_struct = rg_dict.pop("reads")  # type: Dict[str, str]
                library.append_readgroup(ReadGroup(
                    id=rg_dict.pop("id"),
                    R1=read_struct["R1"],
                    R1_md5=read_struct.get("R1_md5", None),
                    R2=read_struct.get("R2", None),
                    R2_md5=read_struct.get("R2_md5", None),
                    additional_properties=rg_dict
                ))
            library.additional_properties.update(lib_dict)
            sample.append_library(library)
        sample.additional_properties.update(sample_dict)
        samplegroup.append_sample(sample)
    return samplegroup


def samplesheet_csv_to_samplegroup(samplesheet_file: Path) -> SampleGroup:
    samples = {}  # type: Dict[str, Any]
    for row_dict in csv_to_dict_generator(samplesheet_file):
        sample = row_dict.pop("sample")
        # In legacy cases readgroups were labbeled libraries,
        # proper libraries didn't exist, for the new format the are
        # the same as samples.
        if "readgroup" in row_dict.keys():
            lib = row_dict.pop("library")
            rg = row_dict.pop("readgroup")
        else:
            lib = sample
            rg = row_dict.pop("library")
        if sample not in samples.keys():
            samples[sample] = {}

        if lib not in samples[sample].keys():
            samples[sample][lib] = {}
        if rg in samples[sample][lib].keys():
            raise ValueError("Duplicate readgroup id {}-{}-{}".format(
                sample, lib, rg))
        read1_md5 = row_dict.pop("R1_md5")
        read2_md5 = row_dict.pop("R2_md5")
        samples[sample][lib][rg] = {
            "R1": row_dict.pop("R1"),
            "R1_md5": read1_md5 if read1_md5 != "" else None,
            "R2": row_dict.pop("R2"),
            "R2_md5": read2_md5 if read2_md5 != "" else None
        }
        # Add all remaining properties
        for key, value in row_dict.items():
            samples[sample][lib][rg][key] = value if value != "" else None

    return SampleGroup.from_dict_of_dicts(samples)
