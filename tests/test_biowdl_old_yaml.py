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
from pathlib import Path

from biowdl_input_converter.input_conversions import biowdl_yaml_to_samplegroup
from biowdl_input_converter.output_conversions import \
    samplegroup_to_biowdl_old_json, samplegroup_to_biowdl_old_yaml

import yaml

from . import COMPLETE_WITH_CONTROL_SAMPLEGROUP, FILESDIR, \
    WITHOUT_MD5_SAMPLEGROUP


def test_import_biowdl_old_yaml_all_fields():
    samplegroup = biowdl_yaml_to_samplegroup(
        FILESDIR / Path("complete_with_control.yml"))
    assert COMPLETE_WITH_CONTROL_SAMPLEGROUP == samplegroup


def test_export_biowdl_old_yaml_all_fields():
    with (FILESDIR / Path("complete_with_control.yml")).open("r") as yaml_h:
        yaml_contents = yaml_h.read()
    yaml_exported = samplegroup_to_biowdl_old_yaml(
        COMPLETE_WITH_CONTROL_SAMPLEGROUP)
    # Load the yamls to assure they are functionally equivalent regardless of
    # order
    assert yaml.safe_load(yaml_exported) == yaml.safe_load(yaml_contents)


def test_import_biowdl_no_props_no_md5():
    samplegroup = biowdl_yaml_to_samplegroup(
        FILESDIR / Path("without_md5.yml"))
    assert WITHOUT_MD5_SAMPLEGROUP == samplegroup


def test_export_biowdl_no_props_no_md5():
    with (FILESDIR / Path("without_md5.yml")).open("r") as yaml_h:
        yaml_contents = yaml_h.read()
    yaml_exported = samplegroup_to_biowdl_old_yaml(
        WITHOUT_MD5_SAMPLEGROUP)
    # Load the yamls to assure they are functionally equivalent regardless of
    # order
    assert yaml.safe_load(yaml_exported) == yaml.safe_load(yaml_contents)


def test_old_style_conversion_yaml_to_json():
    samplegroup = biowdl_yaml_to_samplegroup(
        FILESDIR / Path("complete_with_control.yml"))
    json_result = """
    {"samples": [
        {"id": "s1", "libraries": [{"id": "lib1", "readgroups": [
            {"id": "rg1", "reads":
                {"R1": "r1.fq",
                "R1_md5": "hello",
                "R2": "r2.fq",
                "R2_md5": "hey"}}]}]},
        {"id": "s2", "control":"s1", "libraries": [{"id": "lib1",
            "readgroups": [
            {"id": "rg1", "reads":
            {"R1": "r1.fq",
             "R1_md5": "aa",
            "R2": "r2.fq",
              "R2_md5": "bb"}}]}]}]
    }
    """
    assert json.loads(
        samplegroup_to_biowdl_old_json(samplegroup)) == json.loads(json_result)
