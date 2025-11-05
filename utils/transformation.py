import numpy as np
import pandas as pd
def transform_wind_direction(df, wind_dir_col):
    if wind_dir_col and wind_dir_col in df.columns:
        df[wind_dir_col] = pd.to_numeric(df[wind_dir_col], errors="coerce")
        rad = np.deg2rad(df[wind_dir_col])
        df[f"{wind_dir_col}_sin"] = np.sin(rad)
        df[f"{wind_dir_col}_cos"] = np.cos(rad)
        df = df.drop(columns=[wind_dir_col])
    return df
