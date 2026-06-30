from __future__ import annotations

import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from modules.thermo_loader import *


class EOSDatabase:

    def __init__(self, dir_data, verbose=0):

        self.dir_data = dir_data

        self.verbose = verbose

        self.df_thermo = scan_thermo_tables(dir_data, self.verbose)

        self.df_sources = scan_sources(dir_data, self.verbose)

        self.df_eos = scan_eos(dir_data, self.verbose)
    # -------------------------------------------------
    # Basic filtering
    # -------------------------------------------------

    def filter_out(
        self,
        field: str,
        contains: str,
    ) -> "EOSDatabase":
        """
        Return filtered copy.
        """

        db_new = EOSDatabase.__new__(EOSDatabase)

        db_new.dir_data = self.dir_data

        mask = (
            self.df_thermo[field]
            .astype(str)
            .str.contains(contains, case=False, na=False)
        )

        db_new.df_thermo = self.df_thermo[mask].copy()

        return db_new

    # -------------------------------------------------
    # Convenience methods
    # -------------------------------------------------

    def columns_thermo(self):

        return list(self.df_thermo.columns)
    
    def columns_source(self):

        return list(self.df_source.columns)

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

    def plot_rhopt(self,plt_show=True):

        # ---------------------------------
        # Required columns
        # ---------------------------------

        required = [
            "rho[kg/m^3]",
            "P[Pa]",
            "T[K]",
            "entry",
        ]

        missing = [
            col for col in required
            if col not in self.df_thermo.columns
        ]

        if missing:
            print(
                f"Missing required columns: {missing}"
            )
            return

        # ---------------------------------
        # Unique datasets
        # ---------------------------------

        unique_ids = sorted(
            self.df_thermo["entry"]
            .dropna()
            .unique()
        )

        n_ids = len(unique_ids)

        print(f"Found {n_ids} entries")

        if n_ids > 10:

            print(
                "ERROR: More than 10 entries.\n"
                "Aborting to avoid unreadable plot."
            )

            return

        # ---------------------------------
        # Marker styles
        # ---------------------------------

        markers = [
            "o",
            "s",
            "^",
            "D",
            "v",
            "P",
            "X",
            "*",
            "<",
            ">",
        ]

        # ---------------------------------
        # Create figure
        # ---------------------------------

        fig, ax = plt.subplots(
            figsize=(8, 6)
        )

        # ---------------------------------
        # Global temperature normalization
        # ---------------------------------

        Tmin = self.df_thermo["T[K]"].min()
        Tmax = self.df_thermo["T[K]"].max()

        norm = mcolors.Normalize(
            vmin=Tmin,
            vmax=Tmax,
        )


        # ---------------------------------
        # Plot each dataset separately
        # ---------------------------------

        for marker, uid in zip(markers, unique_ids):

            sub = self.df_thermo[
                self.df_thermo["entry"] == uid
            ]

            sc = ax.scatter(
                sub["rho[kg/m^3]"],
                sub["P[Pa]"] * 1e-9,
                c=sub["T[K]"],
                norm=norm,
                marker=marker,
                s=40,
                alpha=0.8,
                label=uid,
            )

        # ---------------------------------
        # Axes
        # ---------------------------------

        ax.set_xlabel(r"$\rho$ [kg/m$^3$]")
        ax.set_ylabel(r"$P$ [GPa]")

        ax.set_xscale("log")
        ax.set_yscale("log")

        # ---------------------------------
        # Colorbar
        # ---------------------------------

        cbar = plt.colorbar(sc, ax=ax)

        cbar.set_label(r"$T$ [K]")

        # ---------------------------------
        # Legend
        # ---------------------------------

        ax.legend(
            title="Entry",
            fontsize=8,
        )

        # ---------------------------------
        # Cosmetics
        # ---------------------------------

        ax.grid(
            alpha=0.3,
            which="both",
        )

        plt.tight_layout()

        if plt_show == True: plt.show()


 
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

    def __repr__(self):

        return (
            f"EOSDatabase(rows={len(self.df_thermo)}, "
            f"columns={len(self.df_thermo.columns)})"
        )