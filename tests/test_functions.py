from pathlib import Path

from biowdl_input_converter import samplesheet_to_yaml

import pytest

filesdir = Path(__file__).parent / Path("files")


def test_main_comma_complete():
    with (Path(filesdir) / Path("complete.yml")).open() as f:
        result = f.read()
    yaml_string = samplesheet_to_yaml(Path(filesdir) / Path("complete.csv"))
    assert yaml_string == result


def test_main_semicolon_without_md5():
    with (Path(filesdir) / Path("without_md5.yml")).open() as f:
        result = f.read()
    yaml_string = samplesheet_to_yaml(
        (Path(filesdir) / Path("without_md5.csv")))
    assert yaml_string == result


def test_main_tab_without_readgroup():
    with (Path(filesdir) / Path("without_readgroup.yml")).open() as f:
        result = f.read()
    yaml_string = samplesheet_to_yaml(
        (Path(filesdir) / Path("without_readgroup.tsv")))
    assert yaml_string == result


def test_main_missing_field():
    with pytest.raises(KeyError) as e:
        samplesheet_to_yaml((Path(filesdir) / Path("missing_field.csv")))
    e.match("sample")
