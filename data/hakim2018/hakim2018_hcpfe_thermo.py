'''
Script that transforms the raw thermo data
"hakim2018_hcpfe_thermo_raw.dat"
into the database format file
"hakim2018_hcpfe_thermo.dat"
'''

import os
import sys
import pandas as pd

FOLDER = os.path.dirname("./data/hakim2018/")
INPUT_FILE = os.path.join(FOLDER, "hakim2018_hcpfe_thermo_raw.dat")
OUTPUT_FILE = os.path.join(FOLDER, "hakim2018_hcpfe_thermo.dat")

# Constants
NA = 6.02214076e23          # Avogadro number, mol^-1
M_Fe = 55.845e-3            # Iron molar mass, kg/mol
m_Fe = M_Fe / NA            # Atomic mass, kg per atom
n_atoms = 2                 # number of atoms per crystal lattice, iron hcp
mass_cell_kg = n_atoms * M_Fe / NA  # mass of crystal lattice kg

if __name__ == "__main__":
    input_path = INPUT_FILE
    output_path = OUTPUT_FILE

    # Input dataframe
    names = ["Volume (cm3/mol)", "Delta Energy (kJ/mol)", "Pressure (GPa)"]
    df = pd.read_csv(input_path, sep="\t", engine="python", comment="#", names=names)
    # Output dataframe
    df2 = pd.DataFrame()

    # Convert molar volume (cm^3/mol) to density (kg/m^3)
    df2["rho[kg/m^3]"] = M_Fe / (df["Volume (cm3/mol)"]*1e-3)   # V in cm^3/mol
    # Convert pressure from GPa to Pa
    df2["P[Pa]"] = df["Pressure (GPa)"] * 1e9
    # Convert Delta energy to J/mol
    df2["U[J/mol]"] = df["Delta Energy (kJ/mol)"] * 1e3
    # Temperature is 300 K
    df2["T[K]"] = 300.0

    # Export density and pressure in scientific notation
    list_columns_to_scientific = ["rho[kg/m^3]", 
                                  "P[Pa]", 
                                  "U[J/mol]"]
    for col in list_columns_to_scientific:
        df2[col] = df2[col].map(lambda x: f"{x:.6e}")

    # Export to final file
    df2.to_csv(output_path, sep="\t", index=False)
