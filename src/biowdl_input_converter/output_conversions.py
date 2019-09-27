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

import json

import yaml

from .samplestructure import SampleGroup


def samplegroup_to_biowdl_old_structure(samplegroup: SampleGroup):
    samples = []
    for sample in samplegroup:
        libraries = []
        for library in sample:
            readgroups = []
            for readgroup in library:
                reads = {
                    "R1": readgroup.R1,
                }
                if readgroup.R1_md5 is not None:
                    reads["R1_md5"] = readgroup.R1_md5
                if readgroup.R2 is not None:
                    reads["R2"] = readgroup.R2
                if readgroup.R2_md5 is not None:
                    reads["R2_md5"] = readgroup.R2_md5
                readgroup_dict = {
                    "reads": reads,
                    "id": readgroup.id
                }
                readgroup_dict.update(readgroup.additional_properties)
                readgroups.append(readgroup_dict)
            library_dict = {
                "readgroups": readgroups,
                "id": library.id
            }
            library_dict.update(library.additional_properties)
            libraries.append(library_dict)
        sample_dict = {
            "libraries": libraries,
            "id": sample.id
        }
        sample_dict.update(sample.additional_properties)
        samples.append(sample_dict)
    return {"samples": samples}


def samplegroup_to_biowdl_old_yaml(samplegroup: SampleGroup):
    return yaml.safe_dump(samplegroup_to_biowdl_old_structure(samplegroup))


def samplegroup_to_biowdl_old_json(samplegroup: SampleGroup):
    return json.dumps(samplegroup_to_biowdl_old_structure(samplegroup))


def samplegroup_to_biowdl_new_structure(samplegroup: SampleGroup):
    samples = []
    for sample in samplegroup:
        sample_dict = {"readgroups": [], "id": sample.id}
        for library in sample:
            for readgroup in library:
                rg_dict = {"id": readgroup.id,
                           "lib_id": library.id,
                           "R1": readgroup.R1}
