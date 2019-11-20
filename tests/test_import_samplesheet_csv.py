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

from biowdl_input_converter.input_conversions import \
    samplesheet_csv_to_samplegroup
from biowdl_input_converter.output_conversions import \
    samplegroup_to_biowdl_old_yaml

import pytest

from . import FILESDIR


def test_main_comma_complete():
    with (FILESDIR / Path("complete.yml")).open() as f:
        result = f.read()
    samplegroup = samplesheet_csv_to_samplegroup(
        FILESDIR / Path("complete.csv"))
    assert samplegroup_to_biowdl_old_yaml(samplegroup) == result


def test_main_semicolon_without_md5():
    with (FILESDIR / Path("without_md5.yml")).open() as f:
        result = f.read()
    samplegroup = samplesheet_csv_to_samplegroup(
        FILESDIR / Path("without_md5.csv"))
    assert samplegroup_to_biowdl_old_yaml(samplegroup) == result


def test_main_tab_without_readgroup():
    with (FILESDIR / Path("without_readgroup.yml")).open() as f:
        result = f.read()
    samplegroup = samplesheet_csv_to_samplegroup(
        FILESDIR / Path("without_readgroup.tsv"))
    assert samplegroup_to_biowdl_old_yaml(samplegroup) == result


def test_main_missing_field():
    with pytest.raises(KeyError) as e:
        samplesheet_csv_to_samplegroup(
            FILESDIR / Path("missing_field.csv"))
    assert e.match("sample")


def test_extra_field():
    samplesheet = samplesheet_csv_to_samplegroup(
        FILESDIR / Path("extra_fields.csv"))
    assert samplesheet[0].additional_properties["extra_field1"] == "xf1"
    assert samplesheet[0].additional_properties["extra_field2"] == "xf2"
    assert samplesheet[1].additional_properties["extra_field1"] == "xfI"
    assert samplesheet[1].additional_properties["extra_field2"] is None


def test_mixed_empty_and_filled_additional_properties():
    samplesheet = samplesheet_csv_to_samplegroup(
        FILESDIR / Path("mixed_empty_filled_addprops.csv"))
    assert len(samplesheet.samples) == 1
    assert samplesheet[0].additional_properties["extra_field2"] == "xf2"


def test_conflicting_properties():
    with pytest.raises(ValueError) as error:
        samplesheet_csv_to_samplegroup(
            FILESDIR / Path("conflicting_properties.csv")
        )
    error.match("Conflicting fields in column 'extra_field1' for sample 's1'")


def test_no_optional_fields():
    samplesheet = samplesheet_csv_to_samplegroup(
        FILESDIR / Path("no_optional_fields.csv"))
    assert samplesheet[0].id == "s1"
    assert samplesheet[0].libraries[0].id == "lib1"
    assert samplesheet[0].libraries[0].readgroups[0].id == "rg1"
    assert samplesheet[0].libraries[0].readgroups[0].R1 == "r1.fq"
    assert samplesheet[0].libraries[0].readgroups[0].R1_md5 is None
    assert samplesheet[0].libraries[0].readgroups[0].R2 is None
    assert samplesheet[0].libraries[0].readgroups[0].R2_md5 is None
    assert samplesheet[0].libraries[0].readgroups[0].additional_properties == {}  # noqa: E501

    assert samplesheet[1].id == "s2"
    assert samplesheet[1].libraries[0].id == "lib1"
    assert samplesheet[1].libraries[0].readgroups[0].id == "rg1"
    assert samplesheet[1].libraries[0].readgroups[0].R1 == "r1.fq"
    assert samplesheet[1].libraries[0].readgroups[0].R1_md5 is None
    assert samplesheet[1].libraries[0].readgroups[0].R2 is None
    assert samplesheet[1].libraries[0].readgroups[0].R2_md5 is None
    assert samplesheet[1].libraries[0].readgroups[0].additional_properties == {}  # noqa: E501


def test_duplicate_readgroup():
    with pytest.raises(ValueError) as error:
        samplesheet_csv_to_samplegroup(
            FILESDIR / Path("duplicate_readgroup.csv"))
    assert error.match("Duplicate readgroup id s2-lib1-rg1")
