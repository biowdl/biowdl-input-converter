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

from biowdl_input_converter.output_conversions import \
    samplegroup_to_biowdl_new_json

from . import COMPLETE_WITH_CONTROL_SAMPLEGROUP, \
    WITHOUT_MD5_SAMPLEGROUP


def test_complete_with_controls_to_biowdl_new_json():
    result_json = """
    {"samples": [
        {"readgroups": [
            {"lib_id": "lib1",
             "id": "rg1",
             "R1": "r1.fq",
             "R1_md5": "hello",
             "R2": "r2.fq",
             "R2_md5": "hey"
             }
        ],
            "id": "s1"},
        {"readgroups": [
            {"lib_id": "lib1",
             "id": "rg1",
             "R1": "r1.fq",
             "R1_md5": "aa",
             "R2": "r2.fq",
             "R2_md5": "bb"
             }
        ],
            "id": "s2",
            "control": "s1"}]
    }
    """
    result_json_loaded = json.loads(result_json)
    assert result_json_loaded == json.loads(samplegroup_to_biowdl_new_json(
        COMPLETE_WITH_CONTROL_SAMPLEGROUP))


def test_without_md5sum_to_biowdl_new_json():
    result_json = """
    {"samples": [
        {"readgroups": [
            {"lib_id": "lib1",
             "id": "rg1",
             "R1": "r1.fq",
             "R2": "r2.fq"
             }
        ],
            "id": "s1"},
        {"readgroups": [
            {"lib_id": "lib1",
             "id": "rg1",
             "R1": "r1.fq",
             "R2": "r2.fq"
             }
        ],
            "id": "s2"}]
    }
    """
    result_json_loaded = json.loads(result_json)
    assert result_json_loaded == json.loads(samplegroup_to_biowdl_new_json(
        WITHOUT_MD5_SAMPLEGROUP))
