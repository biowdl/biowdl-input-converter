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

from biowdl_input_converter.utils import (check_duplicate_files,
                                          check_existence_list_of_files,
                                          check_md5sums,
                                          csv_to_dict_generator)

import pytest

from . import FILESDIR


def test_only_header():
    only_header_csv = FILESDIR / Path("only_header.csv")
    dict_list = list(csv_to_dict_generator(only_header_csv))
    assert dict_list == []


def test_empty_csv():
    empty_csv = FILESDIR / Path("empty.csv")
    with pytest.raises(ValueError) as error:
        list(csv_to_dict_generator(empty_csv))
    assert error.match("Could not parse CSV file")


def test_check_existence_list_of_files():
    check_existence_list_of_files([FILESDIR / "complete.csv",
                                   FILESDIR / "complete.yml"])


def test_check_existence_list_of_files_with_fails():
    with pytest.raises(FileNotFoundError) as error:
        check_existence_list_of_files([FILESDIR / "illuminati.txt",
                                       FILESDIR / "trolls.txt"])
    assert error.match("illuminati.txt")
    assert error.match("trolls.txt")


def test_check_md5sums():
    check_md5sums([(
        FILESDIR / "empty.csv", "d41d8cd98f00b204e9800998ecf8427e")])


def test_check_md5sums_with_fails():
    with pytest.raises(ValueError) as error:
        check_md5sums([
            (FILESDIR / "empty.csv", "d41d8cd98f00b204e9800998ecf8427e"),
            (FILESDIR / "extra_fields.csv", "XXXX"),
            (FILESDIR / "missing_field.csv", "XXXX")
        ])
    assert "empty.csv" not in str(error)
    assert error.match("extra_fields.csv")
    assert error.match("missing_field.csv")


def test_check_duplicate_files():
    check_duplicate_files(["bla", "bla2", "bla3"])


def test_check_duplicate_files_with_fails():
    with pytest.raises(ValueError) as error:
        check_duplicate_files(["bla", "bla", "bla", "bla",
                               "bla2",
                               "bla3", "bla3"])
    assert "bla2" not in str(error)
    assert "bla" in str(error)
    assert "bla3" in str(error)
