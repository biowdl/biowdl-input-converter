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
import csv
from pathlib import Path
from typing import Any, Dict

import yaml


def getindexes(lst):
    indices = {}
    noreadgroup = False
    for x in ["sample", "library", "readgroup", "R1", "R1_md5", "R2",
              "R2_md5"]:
        try:
            indices[x] = lst.index(x)
        except ValueError:
            if x == "readgroup":
                noreadgroup = True
            else:
                raise
    return indices, noreadgroup


def dropnone(dictionary):
    return {k: v for k, v in dictionary.items() if v is not None}


def reformat(samples):
    """
    Format the dictionary according to the yaml format.
    None values are left out.
    """
    out = {"samples": []}
    for sample in samples:
        sampleentry = {"id": sample, "libraries": []}
        for library in samples[sample]:
            libraryentry = {"id": library, "readgroups": []}
            for readgroup in samples[sample][library]:
                libraryentry["readgroups"].append({
                    "id": readgroup,
                    "reads": dropnone(samples[sample][library][readgroup])
                })
            sampleentry["libraries"].append(libraryentry)
        out["samples"].append(sampleentry)
    return out


def samplesheet_to_yaml(samplesheet_file: Path):
    samples = {}  # type: Dict[str, Any]
    with samplesheet_file.open("r") as csvfile:
        dialect = csv.Sniffer().sniff("".join(
            [csvfile.readline() for _ in range(10)]), delimiters=";,\t")
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        header = next(reader)
        indices, noreadgroup = getindexes(header)
        for row in reader:
            sample = row[indices["sample"]]
            # In legacy cases readgroups were labbeled libraries,
            # proper libraries didn't exist, for the new format the are
            # the same as samples.
            if noreadgroup:
                lib = row[indices["sample"]]
                rg = row[indices["library"]]
            else:
                lib = row[indices["library"]]
                rg = row[indices["readgroup"]]

            if sample not in samples.keys():
                samples[sample] = {}
            if lib not in samples[sample].keys():
                samples[sample][lib] = {}
            if rg in samples[sample][lib].keys():
                raise ValueError("Duplicate readgroup id {}-{}-{}".format(
                    sample, lib, rg))
            samples[sample][lib][rg] = {
                "R1": row[indices["R1"]],
                "R1_md5": (row[indices["R1_md5"]] if
                           row[indices["R1_md5"]] != "" else None),
                "R2": row[indices["R2"]],
                "R2_md5": (row[indices["R2_md5"]] if
                           row[indices["R2_md5"]] != "" else None)}

    # output
    return yaml.safe_dump(reformat(samples), default_flow_style=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("samplesheet")
    args = parser.parse_args()
    yaml_string = samplesheet_to_yaml(Path(args.samplesheet))
    print(yaml_string, end="")


if __name__ == "__main__":
    main()
