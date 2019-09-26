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

import yaml

from .samplestructure import SampleGroup


def samplegroup_to_biowdl_yaml(samplegroup: SampleGroup):
    samples = []
    for sample in samplegroup:
        libraries = []
        for library in sample:
            readgroups = []
            for readgroup in library:
                reads = {
                    "R1": readgroup.R1,
                    "R1_md5": readgroup.R1_md5,
                    "R2": readgroup.R2,
                    "R2_md5": readgroup.R2_md5,
                }
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
    return yaml.safe_dump({"samples": samples})
