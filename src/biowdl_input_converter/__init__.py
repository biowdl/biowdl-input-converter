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

"""
biowdl-input-converter converts samplesheets to json files that are readable
by cromwell.
"""

import argparse
from pathlib import Path

from . import input_conversions, output_conversions


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse samplesheets for BioWDL pipelines.")
    parser.add_argument("samplesheet", type=str,
                        help="The input samplesheet. Format will be "
                             "automatically detected.")
    parser.add_argument("-o", "--output",
                        help="The output file to which the json is written. "
                             "Default: stdout")
    parser.add_argument("--validate", action="store_true",
                        help="Do not generate output but only validate the "
                             "samplesheet.")
    parser.add_argument("--old", action="store_true", dest="old_style_json",
                        help="Output old style JSON as used in BioWDL "
                             "germline-DNA and RNA-seq version 1 pipelines")
    parser.add_argument("--skip-file-check", action="store_true",
                        help="Skip the checking if files in the samplesheet "
                             "are present.")
    parser.add_argument("--check-file-md5sums", action="store_true",
                        help="Do a md5sum check for reads which have md5sums "
                             "added in the samplesheet.")
    return parser


def samplesheet_to_json(samplesheet: Path,
                        old_style_json: bool = False,
                        file_presence_check: bool = True,
                        file_md5_check: bool = False) -> str:
    """
    Converts a samplesheet file to JSON
    :param samplesheet:
    :param old_style_json: Return a BioWDL old-style pipeline JSON
    :param file_presence_check: Check if the files in the samplesheet are
    present
    :param file_md5_check: Check if the md5sums for the files are correct
    :return: a JSON string presenting the BioWDL JSON.
    """
    if samplesheet.suffix in [".tsv", ".csv"]:
        samplegroup = input_conversions.samplesheet_csv_to_samplegroup(
            samplesheet)
    # JSON can also be parsed by a YAML parser.
    elif samplesheet.suffix in [".yaml", ".yml", ".json"]:
        samplegroup = input_conversions.biowdl_yaml_to_samplegroup(
            samplesheet)
    else:
        raise NotImplementedError(
            f"Unsupported extension: {samplesheet.suffix}")

    if file_presence_check:
        samplegroup.test_files_exist()
    if file_md5_check:
        samplegroup.test_file_checksums()

    if old_style_json:
        output_json = output_conversions.samplegroup_to_biowdl_old_json(
            samplegroup)
    else:
        output_json = output_conversions.samplegroup_to_biowdl_new_json(
            samplegroup)
    return output_json


def main():
    args = argument_parser().parse_args()
    output_json = samplesheet_to_json(
        samplesheet=Path(args.samplesheet),
        old_style_json=args.old_style_json,
        file_presence_check=not args.skip_file_check,
        file_md5_check=args.check_file_md5sums)

    # Only generate output if not validating.
    if not args.validate:
        if args.output is not None:
            with open(args.output, "w") as output_h:
                output_h.write(output_json + "\n")
        else:
            print(output_json)


if __name__ == "__main__":
    main()
