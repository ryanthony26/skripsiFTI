import numpy as np
import pandas as pd

def sanitize_numeric_columns(df):
    df = df.replace(
        to_replace=[
            "-", "--", " ", "NaN", "nan", "N/A", "n/a", "None",
            9999, 999.9, 8888, 88.8, -9999, -999, -99.9
        ],
        value=np.nan
    )

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

