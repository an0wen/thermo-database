from __future__ import annotations


'''
Module containing all filtering routines.
'''



# -------------------------------------------------
# Basic filtering
# -------------------------------------------------

def filter(db_new,field,contains=None,remove=None,keep_empty=True
    ) -> "EOSDatabase":
    """
    Return filtered copy.
    """

    mask = (
        db_new.df_thermo[field]
        .astype(str)
        .str.contains(contains, case=False, na=False)
    )

    db_new.df_thermo = db_new.df_thermo[mask].copy()

    return db_new