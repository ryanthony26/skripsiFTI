import numpy as np
import pandas as pd

def newton_order2_interpolate(series):
    x = np.arange(len(series))
    y = series.values.astype(float)

    for i in range(len(y)):
        if np.isnan(y[i]):
            idx = np.where(~np.isnan(y))[0]
            idx = idx[np.argsort(abs(idx - i))][:3]  

            if len(idx) < 3:
                continue

            x0, x1, x2 = x[idx]
            y0, y1, y2 = y[idx]

            a0 = y0
            a1 = (y1 - y0) / (x1 - x0)
            a2 = ((y2 - y1) / (x2 - x1) - a1) / (x2 - x0)

            y[i] = a0 + a1*(x[i] - x0) + a2*(x[i] - x0)*(x[i] - x1)

    return pd.Series(y, index=series.index)


def newton_interpolate_df(df):
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = newton_order2_interpolate(df[col])
    return df

