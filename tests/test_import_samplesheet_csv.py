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

from biowdl_input_converter import input_conversions, output_conversions

import pytest

filesdir = Path(__file__).parent / Path("files")


def test_main_comma_complete():
    with (Path(filesdir) / Path("complete.yml")).open() as f:
        result = f.read()
    samplegroup = input_conversions.samplesheet_csv_to_samplegroup(
        Path(filesdir) / Path("complete.csv"))
    assert output_conversions.samplegroup_to_biowdl_old_yaml(
        samplegroup) == result


def test_main_semicolon_without_md5():
    with (Path(filesdir) / Path("without_md5.yml")).open() as f:
        result = f.read()
    samplegroup = input_conversions.samplesheet_csv_to_samplegroup(
        Path(filesdir) / Path("without_md5.csv"))
    assert output_conversions.samplegroup_to_biowdl_old_yaml(
        samplegroup) == result


def test_main_tab_without_readgroup():
    with (Path(filesdir) / Path("without_readgroup.yml")).open() as f:
        result = f.read()
    samplegroup = input_conversions.samplesheet_csv_to_samplegroup(
        Path(filesdir) / Path("without_readgroup.tsv"))
    assert output_conversions.samplegroup_to_biowdl_old_yaml(
        samplegroup) == result


def test_main_missing_field():
    with pytest.raises(KeyError) as e:
        input_conversions.samplesheet_csv_to_samplegroup(
            Path(filesdir) / Path("missing_field.csv"))
    e.match("sample")


def test_extra_field():
    samplesheet = input_conversions.samplesheet_csv_to_samplegroup(
        Path(filesdir) / Path("extra_fields.csv"))
    assert samplesheet[0].additional_properties["extra_field1"] == "xf1"
    assert samplesheet[0].additional_properties["extra_field2"] == "xf2"
    assert samplesheet[1].additional_properties["extra_field1"] == "xfI"
    assert samplesheet[1].additional_properties["extra_field2"] == "xfII"
