from __future__ import annotations

from pathlib import Path
import pandas as pd
import tomllib


def load_single_thermo(path_dat: Path) -> pd.DataFrame:
    """
    Load one thermo table and merge metadata into dataframe columns.
    """

    path_toml = path_dat.with_suffix(".toml")

    # -----------------------------
    # Read metadata
    # -----------------------------
    with open(path_toml, "rb") as f:
        metadata = tomllib.load(f)

    delimiter = metadata.get("data", {}).get("delimiter", r"\s+")

    # -----------------------------
    # Read table
    # -----------------------------
    df = pd.read_csv(
        path_dat,
        comment="#",
        sep=delimiter,
        engine="python",
    )

    # -----------------------------
    # Add metadata as dataframe columns
    # -----------------------------

    for section_name, section in metadata.items():
        # save unique_id
        if section_name == "unique_id":
            unique_id = section
            df["unique_id"] = unique_id

        # skip non-dictionaries
        if not isinstance(section, dict):
            continue

        for key, value in section.items():

            column_name = f"{section_name}_{key}"

            df[column_name] = value

            # useful provenance fields
            # df["table_path"] = str(path_dat)
            # df["table_name"] = path_dat.stem

    label = (
        path_dat.stem          # remove .dat
        .replace("_thermo", "") # remove suffix
        .split("_", 1)[1]       # remove unique_id
    )
    df["label"] = label
    df["entry"] = unique_id+"_"+label

    return df

# def load_single_eos(path_toml: Path) -> pd.DataFrame:
#     """
#     Load one eos and merge metadata into dataframe columns.
#     """

#     # -----------------------------
#     # Read metadata
#     # -----------------------------
#     with open(path_toml, "rb") as f:
#         metadata = tomllib.load(f)

#     delimiter = metadata.get("data", {}).get("delimiter", r"\s+")

#     # -----------------------------
#     # Read table
#     # -----------------------------
#     df = pd.read_csv(
#         path_toml,
#         comment="#",
#         sep=delimiter,
#         engine="python",
#     )

#     # -----------------------------
#     # Add metadata as dataframe columns
#     # -----------------------------

#     for section_name, section in metadata.items():
#         # save unique_id
#         if section_name == "unique_id":
#             unique_id = section
#             df["unique_id"] = unique_id

#         # skip non-dictionaries
#         if not isinstance(section, dict):
#             continue

#         for key, value in section.items():

#             column_name = f"{section_name}_{key}"

#             df[column_name] = value


#     label = (
#         path_toml.stem          # remove .dat
#         .replace("_eos", "") # remove suffix
#         .split("_", 1)[1]       # remove unique_id
#     )
#     df["label"] = label
#     df["entry"] = unique_id+"_"+label

#     return df



def scan_thermo_tables(dir_data, verbose=0) -> pd.DataFrame:
    """
    Scan all folders recursively and merge thermo tables.
    """

    dir_data = Path(dir_data)

    dfs = []

    for path_dat in dir_data.rglob("*_thermo.dat"):
        # skip folders and files starting with _
        if path_dat.parts[1].startswith("_") or path_dat.parts[2].startswith("_"):
            continue

        try:
            df = load_single_thermo(path_dat)
            dfs.append(df)

            if verbose==1: print(f"Loaded thermo file: {path_dat}")

        except Exception as e:
            print(f"Failed loading {path_dat}")
            print(e)

    if not dfs or len(dfs) == 0:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)

def scan_eos(dir_data, verbose=0):
    """
    Scan all folders recursively and merge information about eos.
    """

    dir_data = Path(dir_data)

    rows = []

    for path_dat in dir_data.rglob("*_eos.toml"):
        # skip folders and files starting with _
        if path_dat.parts[1].startswith("_") or path_dat.parts[2].startswith("_"):
            continue

        try:
            with open(path_dat,"rb") as f:
                meta = tomllib.load(f)

            if verbose==1: print(f"Loaded EOS file: {path_dat}")

        except Exception as e:
            print(f"Failed loading {path_dat}")
            print(e)

        row = {}

        for section, content in meta.items():
            # save unique_id
            if section == "unique_id":
                unique_id = content
                row["unique_id"] = unique_id

            if not isinstance(content,dict):
                continue

            for key, value in content.items():
                row[f"{section}_{key}"] = value

        row["source_file"] = (path_dat.name)

        label = (
            path_dat.stem          # remove .dat
            .replace("_eos", "") # remove suffix
            .split("_", 1)[1]       # remove unique_id
        )
        row["label"] = label
        row["entry"] = row["unique_id"]+"_"+label

        rows.append(row)

    return pd.DataFrame(rows)


def scan_sources(dir_data, verbose=1):
    """
    Scan all folders recursively and merge information about sources.
    """

    rows = []

    for file in Path(dir_data).rglob("*_source.toml"):
        # skip folders starting with _
        if file.parts[0]=="_":
            continue

        try:
            with open(file,"rb") as f:
                meta = tomllib.load(f)

            if verbose==1: print(f"Loaded EOS file: {file}")

        except Exception as e:
            print(f"Failed loading {file}")
            print(e)

        row = {}

        for section, content in meta.items():
            if not isinstance(content,dict):
                continue

            for key, value in content.items():
                row[f"{section}_{key}"] = value

        row["source_file"] = (file.name)

        rows.append(row)



    return pd.DataFrame(rows)