import csv
import argparse
from pathlib import Path
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
    samples = {}
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
