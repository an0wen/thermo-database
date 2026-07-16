from __future__ import annotations

import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tabulate import tabulate
from copy import deepcopy

from . import loader
from . import plotter
from . import filterer

class EOSDatabase:

    def __init__(self, dir_data, verbose=0):

        self.dir_data = dir_data

        self.verbose = verbose

        self.df_thermo = loader.load_thermo(dir_data, self.verbose)

        self.df_source = loader.load_sources(dir_data, self.verbose)

        self.df_eos = loader.load_eos(dir_data, self.verbose)

        print(f"All data loaded successfully from {dir_data}.")

    # -------------------------------------------------
    # Convenience methods
    # -------------------------------------------------

    def columns_source(self):

        return list(self.df_source.columns)

    def columns_thermo(self):

        return list(self.df_thermo.columns)

    def columns_eos(self):

        return list(self.df_eos.columns)
    
    def show_unique_eos(self):

        print(
            tabulate(
                self.df_eos[["entry"]],
                headers=["index", "entry"],
                tablefmt="plain",
                showindex=True,
                colalign=("right", "left"),   # index, column
            )
        )

    def unique_thermo(self, field: str):

        return sorted(self.df_thermo[field].dropna().unique())
    
    def unique_source(self, field: str):

        return sorted(self.df_thermo[field].dropna().unique())
    
    def print_species_thermo(self):

        print("Species in thermo database")
        print("--------------------------")

        required = ["science_material", "science_formula", "unique_id"]

        missing = [
            col for col in required
            if col not in self.df_thermo.columns
        ]

        if missing:
            print(f"Missing required columns: {missing}")
            return

        # Keep only relevant columns
        species = (
            self.df_thermo[
                ["science_material", "science_formula", "unique_id"]
            ]
            .drop_duplicates()
            .sort_values(["science_material", "science_formula", "unique_id"])
        )

        current_material = None

        for _, row in species.iterrows():

            material = row["science_material"]
            formula = row["science_formula"]
            citation = row["unique_id"]

            # print material header only once
            if material != current_material:

                print()
                print(material)

                current_material = material

            print(f"  - {formula} : {citation}")

    def summary_thermo(self):

        print("EOSDatabase summary thermo")
        print("--------------------------")
        print(f"Rows   : {len(self.df_thermo)}")
        print(f"Columns: {len(self.df_thermo.columns)}")
        print("--------------------------")
        if "unique_id" not in self.df_thermo.columns:
            print("No citation column found")
            return

        # avoid duplicates
        cols = ["unique_id"]

        if "science_formula" in self.df_thermo.columns:
            cols.append("science_formula")

        citations = (
            self.df_thermo[cols]
            .drop_duplicates()
            .sort_values(cols)
        )

        for _, row in citations.iterrows():

            if "science_formula" in cols:
                print(f"{row['unique_id']} ({row['science_formula']})")
            else:
                print(row["unique_id"])

    def export_tsv(
        self,
        filename: str,
        dir_output: str = "./output",
    ):

        # ---------------------------------
        # Create output directory if needed
        # ---------------------------------

        dir_output = Path(dir_output)
        dir_output.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------------------------------
        # Append export date
        # ---------------------------------

        today = datetime.now().strftime("%Y%m%d")

        output_filename = (
            f"{filename}_{today}.tsv"
        )

        path_output = dir_output / output_filename

        # ---------------------------------
        # Export dataframe
        # ---------------------------------

        self.df_thermo.to_csv(
            path_output,
            sep="\t",
            index=False,
        )

        print()
        print("Export complete")
        print(f"File: {path_output}")
        print(f"Rows exported: {len(self.df_thermo)}")

    def plot_thermo_rhopt(self,plt_show=True):

        plotter.plot_thermo_rhopt(self.df_thermo,plt_show)

 
    def print_species_eos(self):

        print("Species in eos database")
        print("-----------------------")

        required = ["science_material", "science_formula", "unique_id"]

        missing = [
            col for col in required
            if col not in self.df_eos.columns
        ]

        if missing:
            print(f"Missing required columns: {missing}")
            return

        # Keep only relevant columns
        species = (
            self.df_eos[
                ["science_material", "science_formula", "unique_id"]
            ]
            .drop_duplicates()
            .sort_values(["science_material", "science_formula", "unique_id"])
        )

        current_material = None

        for _, row in species.iterrows():

            material = row["science_material"]
            formula = row["science_formula"]
            citation = row["unique_id"]

            # print material header only once
            if material != current_material:

                print()
                print(material)

                current_material = material

            print(f"  - {formula} : {citation}")

    def summary_eos(self):

        print("EOSDatabase summary eos")
        print("-----------------------")
        print(f"Rows   : {len(self.df_eos)}")
        print(f"Columns: {len(self.df_eos.columns)}")
        print("-----------------------")
        if "unique_id" not in self.df_eos.columns:
            print("No citation column found")
            return

        # avoid duplicates
        cols = ["unique_id"]

        if "science_formula" in self.df_eos.columns:
            cols.append("science_formula")

        citations = (
            self.df_eos[cols]
            .drop_duplicates()
            .sort_values(cols)
        )

        for _, row in citations.iterrows():

            if "science_formula" in cols:
                print(f"{row['unique_id']} ({row['science_formula']})")
            else:
                print(row["unique_id"])


    def get_eos(self, entry):

        match = self.df_eos[self.df_eos["entry"] == entry]

        if len(match) == 0:
            raise ValueError(f"No EOS found for {entry}")

        if len(match) > 1:
            raise ValueError(f"Multiple EOS found for {entry}")

        # convert single row → dict
        eos = (match.iloc[0].dropna().to_dict())

        return eos
    
    def filter(
        self,
        field,
        **kwargs) -> "EOSDatabase":
        """
        Return filtered copy.
        Expected kwargs:
        - contains=None: string that the field must contain
        - remove=None: string for things to remove
        - keep_empty=True: bool, keep fields that are empty
        """

        db_new = deepcopy(self)

        db_new = filterer.filter(db_new, field, **kwargs)
        return db_new

    def __repr__(self):

        return (
            f"EOSDatabase(rows={len(self.df_thermo)}, "
            f"columns={len(self.df_thermo.columns)})"
        )