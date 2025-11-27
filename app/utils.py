import pandas as pd


def df_from_rows(rows):
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)