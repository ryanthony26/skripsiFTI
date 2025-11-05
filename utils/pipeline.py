import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from utils.sanitize import sanitize_numeric_columns
from utils.missing_value import newton_interpolate_df
from utils.transformation import transform_wind_direction
from utils.labelling import label_extremes_etccdi

def run_pipeline(
    df,
    tmax_col,
    rain_col,
    wind_dir_col,
    explained_var=None,
    manual_comp=None,
    use_pca=True,
):
 
    df = sanitize_numeric_columns(df)
    df = newton_interpolate_df(df)
    df = transform_wind_direction(df, wind_dir_col)

    df["label"], thresholds = label_extremes_etccdi(df, tmax_col, rain_col)

    X = df.drop(columns=["tanggal", "label"], errors="ignore").select_dtypes(include=[np.number])
    y = df["label"]

    # ✅ Simpan mapping nilai label → nama kelas asli
    unique_labels = sorted(y.unique())
    label_mapping = {i: lbl for i, lbl in enumerate(unique_labels)}

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )

    scaler = StandardScaler().fit(X_train_raw)
    X_train_scaled = scaler.transform(X_train_raw)
    X_test_scaled  = scaler.transform(X_test_raw)

    pca_model = None
    if use_pca:
        if explained_var is not None:
            pca = PCA(n_components=explained_var, svd_solver="full")
        else:
            pca = PCA(n_components=manual_comp)

        X_train_final = pca.fit_transform(X_train_scaled)
        X_test_final  = pca.transform(X_test_scaled)
        pca_model = pca

    else:
        X_train_final = X_train_scaled
        X_test_final  = X_test_scaled

    lda = LDA()
    lda.fit(X_train_final, y_train)
    y_pred = lda.predict(X_test_final)

    acc = accuracy_score(y_test, y_pred)
    report_text = classification_report(y_test, y_pred, zero_division=0)
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    # Proyeksi untuk visualisasi LDA
    try:
        X_scaled_all = scaler.transform(X)
        if use_pca and pca_model is not None:
            X_all_final = pca_model.transform(X_scaled_all)
        else:
            X_all_final = X_scaled_all

        lda_vis = LDA().fit(X_all_final, y)
        X_lda_proj = lda_vis.transform(X_all_final)

        n_comp = min(2, X_lda_proj.shape[1])
        lda_projection = pd.DataFrame(
            X_lda_proj[:, :n_comp],
            columns=[f"LD{i+1}" for i in range(n_comp)]
        )
        lda_projection["label"] = y.values

    except:
        lda_projection = None

    result = {
        "accuracy": acc,
        "report": report_text,
        "report_dict": report_dict,
        "confusion": cm,
        "thresholds": thresholds,
        "lda_projection": lda_projection,
        "label_mapping": label_mapping,
        "scaler": scaler,
        "lda_model": lda,
    }

    if pca_model is not None:
        result["pca_model"] = pca_model

    return result
