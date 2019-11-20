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
All conversions to samplestructure.SampleGroup from a variety of formats.
"""

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
    """
    Converts a samplesheet file to a SampleGroup class
    :param samplesheet_file: a pathlib.Path to a file.
    :return: a SampleGroup object
    """
    samples = {}  # type: Dict[str, Any]
    for row_dict in csv_to_dict_generator(samplesheet_file):
        sample = row_dict.pop("sample")
        # In legacy cases readgroups were labelled libraries,
        # proper libraries didn't exist, for the new format the are
        # the same as samples.
        if "readgroup" in row_dict.keys():
            lib = row_dict.pop("library")
            readgroup = row_dict.pop("readgroup")
        else:
            lib = sample
            readgroup = row_dict.pop("library")

        rg_id = f"{sample}-{lib}-{readgroup}"
        if sample not in samples.keys():
            samples[sample] = {}
        if lib not in samples[sample].keys():
            samples[sample][lib] = {}
        if readgroup in samples[sample][lib].keys():
            raise ValueError(f"Duplicate readgroup id {rg_id}")
        read1_md5 = row_dict.pop("R1_md5", None)
        read2_md5 = row_dict.pop("R2_md5", None)
        read2 = row_dict.pop("R2", None)
        samples[sample][lib][readgroup] = {
            "R1": row_dict.pop("R1"),
            "R1_md5": read1_md5 if read1_md5 != "" else None,
            "R2": read2 if read2 != "" else None,
            "R2_md5": read2_md5 if read2_md5 != "" else None
        }
        # Add all remaining properties to additional properties at the
        # sample level
        if "additional_properties" not in samples[sample].keys():
            samples[sample]["additional_properties"] = {}
        for key, value in row_dict.items():
            existing_value = samples[sample][
                "additional_properties"].get(key, None)

            updated_value = value if value != "" else None

            if existing_value is None:
                samples[sample]["additional_properties"][key] = updated_value
            else:
                if (updated_value is not None
                        and existing_value != updated_value):
                    raise ValueError(
                        f"Conflicting fields in column '{key}' for sample "
                        f"'{sample}'!"
                    )

    return SampleGroup.from_dict_of_dicts(samples)
