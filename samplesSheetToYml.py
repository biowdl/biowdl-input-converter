import csv

import yaml

def getindexes(lst):
    indices = {}
    for x in ["sample", "library","readgroup", "R1", "R1_md5", "R2", "R2_md5"]:
        indices[x] = lst.index(x)
    return indices


def reformat(samples):
    """
    Format the dictionary according to the yaml format
    """
    out = {"samples": []}
    for sample in samples:
        sampleentry = {"id": sample, "libraries": []}
        for library in samples[sample]:
            libraryentry = {"id": library, "readgroups": []}
            for readgroup in samples[sample][library]:
                libraryentry["readgroups"].append(
                    {"id": readgroup,
                    "reads":samples[sample][library][readgroup]})
            sampleentry["libraries"].append(libraryentry)
        out["samples"].append(sampleentry)
    return out


def main():
    samples = {}
    with open("test.tsv", "r") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,\t")
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        header = next(reader)
        indices = getindexes(header)
        for row in reader:
            sample = row[indices["sample"]]
            lib = row[indices["library"]]
            rg = row[indices["readgroup"]]

            if not sample in samples.keys():
                samples[sample] = {}
            if not lib in samples[sample].keys():
                samples[sample][lib] = {}
            if rg in samples[sample][lib].keys():
                raise ValueError("Duplicate readgroup id {}-{}-{}".format(
                    sample, lib, rg))
            samples[sample][lib][rg] = {
                "R1": row[indices["R1"]],
                "R1_md5": row[indices["R1_md5"]] if row[indices["R1_md5"]] != "" else None,
                "R2": row[indices["R2"]],
                "R2_md5": row[indices["R2_md5"]] if row[indices["R2_md5"]] != "" else None}

    # output
    print(yaml.dump(reformat(samples), default_flow_style=False))


if __name__ == "__main__":
    main()
