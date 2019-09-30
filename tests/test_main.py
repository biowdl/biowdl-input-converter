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

import shutil
import sys
import tempfile
from pathlib import Path

import biowdl_input_converter
from biowdl_input_converter import input_conversions, \
    output_conversions, samplesheet_to_json

import pytest

from . import FILESDIR

COMPLETE_CSV = csv_file = FILESDIR / Path("complete.csv")


@pytest.fixture()
def correct_md5sum_samplesheet():
    r1 = FILESDIR / Path("data") / Path("R1.fq")
    r2 = FILESDIR / Path("data") / Path("R2.fq")
    tempdir = Path(tempfile.mkdtemp())
    temp_csv = (tempdir / Path("correct_md5sum.csv")).absolute()
    with temp_csv.open("w") as csv_h:
        csv_h.writelines([
            '"sample","library","readgroup","R1","R1_md5","R2","R2_md5"\n',
            f'"s1","lib1","rg1",'
            f'"{str(r1.absolute())}","d8e8fca2dc0f896fd7cb4cb0031ba249",'
            f'"{str(r2.absolute())}",126a8a51b9d1bbd07fddc65819a542c3\n',
            ])
    yield temp_csv
    shutil.rmtree(str(tempdir))


def test_samplesheet_to_json_no_checks():
    output = samplesheet_to_json(COMPLETE_CSV, file_presence_check=False)
    correct_output = output_conversions.samplegroup_to_biowdl_new_json(
        input_conversions.samplesheet_csv_to_samplegroup(COMPLETE_CSV))
    assert output == correct_output


def test_samplesheet_to_old_style_json():
    output = samplesheet_to_json(COMPLETE_CSV, file_presence_check=False,
                                 old_style_json=True)
    correct_output = output_conversions.samplegroup_to_biowdl_old_json(
        input_conversions.samplesheet_csv_to_samplegroup(COMPLETE_CSV))
    assert output == correct_output


def test_yaml_samplesheet_to_json():
    samplesheet = FILESDIR / Path("complete.yml")
    output = samplesheet_to_json(samplesheet,
                                 file_presence_check=False)
    correct_output = output_conversions.samplegroup_to_biowdl_new_json(
        input_conversions.biowdl_yaml_to_samplegroup(samplesheet))
    assert output == correct_output


def test_unknown_samplesheet_format():
    samplesheet = Path("bla.customformat")
    with pytest.raises(NotImplementedError) as error:
        samplesheet_to_json(samplesheet)
    error.match("Unsupported extension: .customformat")


def test_samplesheet_md5_checks(correct_md5sum_samplesheet):
    samplesheet_to_json(correct_md5sum_samplesheet, file_presence_check=True,
                        file_md5_check=True)


def test_main(correct_md5sum_samplesheet, capsys):
    sys.argv = ["biowdl-input-converter",
                "--check-file-md5sums",
                str(correct_md5sum_samplesheet)]
    biowdl_input_converter.main()
    stdout = capsys.readouterr().out
    correct_output = output_conversions.samplegroup_to_biowdl_new_json(
        input_conversions.samplesheet_csv_to_samplegroup(
            correct_md5sum_samplesheet)) + '\n'
    assert stdout == correct_output


def test_main_validate(correct_md5sum_samplesheet, capsys):
    sys.argv = ["biowdl-input-converter",
                "--check-file-md5sums",
                "--validate",
                str(correct_md5sum_samplesheet)]
    biowdl_input_converter.main()
    stdout = capsys.readouterr().out
    assert stdout == ""
