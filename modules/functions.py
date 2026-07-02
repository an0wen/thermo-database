from __future__ import annotations

from pathlib import Path
import pandas as pd
import tomllib


def print_eos(eos):
    
    print_science(eos)
    print()
    print_description(eos)
    print()
    print_validity(eos)
    print()
    print_parameters(eos)
    print()

def print_science(eos):

    print("Science of entry: ",eos["entry"])
    print("-------")

    for key, value in eos.items():
        if key.startswith("science_"):
            name = key.replace("science_","")
            print(f"{name}: {value}")


def print_description(eos):

    print("Description of entry: ",eos["entry"])
    print("-----------")

    for key, value in eos.items():
        if key.startswith("description_"):
            name = key.replace("description_","")
            print(f"{name}: {value}")

def print_validity(eos):

    print("Validity of entry: ",eos["entry"])
    print("--------")

    for key, value in eos.items():
        if key.startswith("validity_"):
            name = key.replace("validity_","")
            print(f"{name}: {value}")

def print_parameters(eos):

    print("Parameters of entry: ",eos["entry"])
    print("----------")

    for key, value in eos.items():
        if key.startswith("parameters_"):
            name = key.replace("parameters_","")
            print(f"{name}: {value}")