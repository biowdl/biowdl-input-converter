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

from biowdl_input_converter.samplestructure import Library, ReadGroup, \
    Sample, SampleGroup


def test_readgroup_as_dict():
    readgroup = ReadGroup(
        id="rg1",
        R1="rg1_r1.fq",
        R2="rg2_r1.fq",
        additional_properties=dict(useless_prop="awesomeness")
    )
    rg_dict = dict(
        id="rg1",
        R1="rg1_r1.fq",
        R2="rg2_r1.fq",
        useless_prop="awesomeness"
    )
    assert readgroup.as_dict() == rg_dict


def test_library_append_and_access():
    readgroup = ReadGroup(id="bla", R1="bla.fq")
    library = Library(id="blalib")
    library.append_readgroup(readgroup)
    assert library[0] == readgroup


def test_sample_append_and_access():
    library = Library(id="blalib")
    sample = Sample(id="blasample")
    sample.append_library(library)
    assert sample[0] == library


def test_samplegroup_append_and_access():
    sample = Sample(id="blasample")
    samplegroup = SampleGroup()
    samplegroup.append_sample(sample)
    assert samplegroup[0] == sample


def test_samplegroup_from_dict_of_dicts():
    dict_of_dicts = {
        "sample1": {
            "lib1": {
                "rg1": {
                    "R1": "r1.fq"
                }
            }
        }
    }
    samplegroup = SampleGroup([
        Sample(id="sample1", libraries=[
            Library(id="lib1", readgroups=[
                ReadGroup(id="rg1", R1="r1.fq")
            ])])
    ])
    assert SampleGroup.from_dict_of_dicts(dict_of_dicts) == samplegroup
