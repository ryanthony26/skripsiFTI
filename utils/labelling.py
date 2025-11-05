import numpy as np
import pandas as pd

def label_extremes_etccdi(df, tmax_col, rain_col, p_tx90=90.0, p_r95=95.0):
    df[tmax_col] = pd.to_numeric(df[tmax_col], errors="coerce")
    df[rain_col] = pd.to_numeric(df[rain_col], errors="coerce")

    # Threshold ETCCDI
    tx90_thr = np.nanpercentile(df[tmax_col].dropna(), p_tx90)
    wet = df[df[rain_col] > 0][rain_col]
    r95_thr = np.nanpercentile(wet.dropna(), p_r95) if len(wet) else np.nan

    labels = []
    for _, row in df.iterrows():
        tmax_val, rain_val = row[tmax_col], row[rain_col]
        is_hot = tmax_val > tx90_thr
        is_rain = rain_val > r95_thr and rain_val > 0
        if is_rain:
            labels.append("Hujan Ekstrem")
        elif is_hot:
            labels.append("Suhu Ekstrem")
        else:
            labels.append("Normal")

    return pd.Series(labels, name="label"), {"TX90p": tx90_thr, "R95p": r95_thr}
