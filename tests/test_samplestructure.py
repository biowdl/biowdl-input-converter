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

from biowdl_input_converter.samplestructure import Library, ReadGroup, \
    Sample, SampleGroup

import pytest

from . import FILESDIR


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


def test_readgroup_with_md5s_as_dict():
    readgroup = ReadGroup(
        id="rg1",
        R1="rg1_r1.fq",
        R1_md5="e583af1f8b00b53cda87ae9ead880224",
        R2="rg2_r1.fq",
        R2_md5="e2c66a521239b647abe000c3cccfd930"
    )
    rg_dict = dict(
        id="rg1",
        R1="rg1_r1.fq",
        R1_md5="e583af1f8b00b53cda87ae9ead880224",
        R2="rg2_r1.fq",
        R2_md5="e2c66a521239b647abe000c3cccfd930"
    )
    assert readgroup.as_dict() == rg_dict


def test_library_append_and_access():
    readgroup = ReadGroup(id="bla", R1="bla.fq")
    library = Library(id="blalib")
    library.append(readgroup)
    assert library[0] == readgroup


def test_incorrect_library_append():
    library = Library("lib1")
    with pytest.raises(TypeError) as error:
        library.append("rg1")
    assert error.match("Only readgroup ")


def test_sample_append_and_access():
    library = Library(id="blalib")
    sample = Sample(id="blasample")
    sample.append(library)
    assert sample[0] == library


def test_incorrect_sample_append():
    sample = Sample("sample1")
    with pytest.raises(TypeError) as error:
        sample.append("lib1")
    assert error.match("Only library")


def test_samplegroup_append_and_access():
    sample = Sample(id="blasample")
    samplegroup = SampleGroup()
    samplegroup.append(sample)
    assert samplegroup[0] == sample


def test_incorrect_samplegroup_append():
    samplegroup = SampleGroup()
    with pytest.raises(TypeError) as error:
        samplegroup.append("sample1")
    assert error.match("Only sample ")


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
