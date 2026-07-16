from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

'''
Module containing all plotting routines.
'''

def plot_thermo_rhopt(df_thermo,plt_show=True):

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
        if col not in df_thermo.columns
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
        df_thermo["entry"]
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

    Tmin = df_thermo["T[K]"].min()
    Tmax = df_thermo["T[K]"].max()

    norm = mcolors.Normalize(
        vmin=Tmin,
        vmax=Tmax,
    )


    # ---------------------------------
    # Plot each dataset separately
    # ---------------------------------

    for marker, uid in zip(markers, unique_ids):

        sub = df_thermo[
            df_thermo["entry"] == uid
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
