"""
This script loads the database to verify that new entries work as intended.

I
"""
# Testing source code import
try:
    from modules.eosdatabase import EOSDatabase
    from modules.functions import *
    print(f"Source code imported successfully.")
    print()
except:
    print("Couldn't import the database source code. Exiting.")
    exit()

# Testing loading database
database_fname = "./data"
try:
    database = EOSDatabase(database_fname, verbose = 1)
    print(f"Database located at '{database_fname}' loaded successfully.")
    print()
except:
    print(f"Couldn't load the database located at '{database_fname}'. Exiting.")
    exit()

print(f"All tests passed. Please use the 'EOSdatabase_demo_*.' notebook to verify that your entry has the expected behavior.")