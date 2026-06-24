from eosdatabase import EOSDatabase

# main program
def main():

    db = EOSDatabase("./data")

    db.summary()

    print()

    print("Available formulas:")
    print(db.unique("formula"))

    print()

    iron_db = db.filter_out(
        field="formula",
        contains="Fe",
    )

    print(iron_db.df.head())


if __name__ == "__main__":
    main()