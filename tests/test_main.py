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

from biowdl_input_converter import input_conversions, main, \
    output_conversions, samplesheet_to_json

from . import FILESDIR

COMPLETE_CSV = csv_file = FILESDIR / Path("complete.csv")


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


