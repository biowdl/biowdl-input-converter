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

import argparse
import sys
from pathlib import Path

from . import input_conversions, output_conversions


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("samplesheet", type=str)
    parser.add_argument("-o", "--output", default=sys.stdout)
    parser.add_argument("--old", action="store_false", dest="new_style_json",
                        help="Output old style JSON as used in BioWDL "
                             "germline-DNA and RNA-seq version 1 pipelines")
    return parser


def samplesheet_to_yaml(input_file: Path):
    samplesheet = input_conversions.samplesheet_csv_to_samplegroup(input_file)
    return output_conversions.samplegroup_to_biowdl_old_yaml(samplesheet)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("samplesheet")
    args = parser.parse_args()
    yaml_string = samplesheet_to_yaml(Path(args.samplesheet))
    print(yaml_string, end="")


if __name__ == "__main__":
    main()
