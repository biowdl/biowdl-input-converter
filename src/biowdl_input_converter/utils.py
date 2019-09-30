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
Contains general functions that are not specific to biowdl_input_converter.
"""

import csv
import hashlib
from pathlib import Path
from typing import Dict, Generator


def csv_to_dict_generator(csv_file: Path) -> Generator[Dict[str, str], None, None]:  # noqa: E501
    """
    Converts a csv_file into a generator. The generator yields each row
    (except the header) as a dictionary. {header_column1: value,
    header_column2: value etc.}
    :param csv_file: A pathlib.Path pointing to the csv file.
    :return: a generator that yields rows as Dict[str,str].
    """
    with csv_file.open("r") as csvfile:
        first_ten_lines = "".join([csvfile.readline() for _ in range(10)])
        try:
            dialect = csv.Sniffer().sniff(first_ten_lines, delimiters=";,\t")
        except csv.Error as csv_error:
            raise ValueError(f"Could not parse CSV file: {csv_error}")
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        try:
            header = next(reader)
        # A proper generator never raises a stop iteration. Instead it returns.
        except StopIteration:
            return

        for row in reader:
            row_dict = {heading: row[index]
                        for index, heading in enumerate(header)}
            yield row_dict


# Copied from pytest-workflow
def file_md5sum(filepath: Path, blocksize: int = 64 * 1024) -> str:
    """
    Generates a md5sum for a file. Reads file in blocks to save memory.
    :param filepath: a pathlib. Path to the file
    :param blocksize: An integer describing the blocksize when reading in the
    file. Default: 64 kb. This is faster than 8kb (3.4 vs 3.74 seconds on a
    2.3 GB file). After 64 kb the speed gains are very minimal for the increase
    in used memory.
    :return: a md5sum as hexadecimal string.
    """
    hasher = hashlib.md5()  # nosec: only used for file integrity
    with filepath.open('rb') as file_handler:  # Read the file in bytes
        # Hardcode the blocksize at 8192 bytes here.
        # This can be changed or made variable when the requirements compel us
        # to do so.
        for block in iter(lambda: file_handler.read(blocksize), b''):
            hasher.update(block)
    return hasher.hexdigest()
