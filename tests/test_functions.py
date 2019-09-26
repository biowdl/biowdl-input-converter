from pathlib import Path

import pytest
from biowdl_input_converter import getindexes, dropnone, reformat, \
    samplesheet_to_yaml

filesdir = Path(__file__).parent / Path("files")


def test_getindexes_withreadgroup():
    assert getindexes(["sample", "library", "readgroup", "R1", "R1_md5", "R2",
                       "R2_md5"]) == ({"sample": 0, "library": 1,
                                       "readgroup": 2, "R1": 3, "R1_md5": 4,
                                       "R2": 5, "R2_md5": 6}, False)


def test_getindexes_withoutreadgroup():
    assert getindexes(["sample", "library", "R1", "R1_md5", "R2",
                       "R2_md5"]) == ({"sample": 0, "library": 1, "R1": 2,
                                       "R1_md5": 3, "R2": 4, "R2_md5": 5},
                                      True)


def test_getindexes_missingfield():
    with pytest.raises(ValueError):
        getindexes(["library", "readgroup", "R1", "R1_md5", "R2", "R2_md5"])


def test_dropnone():
    assert dropnone({"A": None, "B": 1}) == {"B": 1}


def test_reformat():
    result = {"samples": [
        {"id": "s1", "libraries": [
            {"id": "lib1", "readgroups": [
                {"id": "rg1", "reads": {
                    "R1": "r1.fq", "R1_md5": ":3", "R2": "r2.fq",
                    "R2_md5": ":p"}
                },{"id": "rg2", "reads": {
                    "R1": "r3.fq", "R1_md5": ":O", "R2": "r4.fq",
                    "R2_md5": ":X"}}]}]},
        {"id": "s2", "libraries": [
            {"id": "lib2", "readgroups": [
                {"id": "rg3", "reads": {
                    "R1": "r5.fq", "R1_md5": ":)", "R2": "r6.fq",
                    "R2_md5": ":("}}]},
            {"id": "lib3", "readgroups": [
                {"id": "rg4", "reads": {
                    "R1": "r7.fq", "R2": "r8.fq"}}]}]}]}
    testdict = {
        "s1": {"lib1": {"rg1": {
                "R1": "r1.fq", "R1_md5": ":3", "R2": "r2.fq", "R2_md5": ":p"},
            "rg2": {
                "R1": "r3.fq", "R1_md5": ":O", "R2": "r4.fq",
                "R2_md5": ":X"}}},
        "s2": {"lib2": {"rg3": {
                "R1": "r5.fq", "R1_md5": ":)", "R2": "r6.fq", "R2_md5": ":("}},
            "lib3": { "rg4": {
                "R1": "r7.fq", "R1_md5": None, "R2": "r8.fq",
                    "R2_md5": None}}}}
    assert reformat(testdict) == result


def test_main_comma_complete():
    with (Path(filesdir) / Path("complete.yml")).open() as f:
        result = f.read()
    yaml_string = samplesheet_to_yaml(Path(filesdir) / Path("complete.csv"))
    assert yaml_string == result


def test_main_semicolon_without_md5():
    with (Path(filesdir) / Path("without_md5.yml")).open() as f:
        result = f.read()
    yaml_string = samplesheet_to_yaml((Path(filesdir) / Path("without_md5.csv")))
    assert yaml_string == result


def test_main_tab_without_readgroup():
    with (Path(filesdir) / Path("without_readgroup.yml")).open() as f:
        result = f.read()
    yaml_string = samplesheet_to_yaml((Path(filesdir) / Path("without_readgroup.tsv")))
    assert yaml_string == result


def test_main_missing_field():
    with pytest.raises(ValueError):
        samplesheet_to_yaml((Path(filesdir) / Path("missing_field.csv")))
