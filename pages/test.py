import streamlit as st
import pandas as pd
import numpy as np

st.header("Uji Coba Prediksi Manual (PCA–LDA)")

if "results" not in st.session_state or "PCA_LDA" not in st.session_state["results"]:
    st.error("⚠️ Silakan jalankan pembuatan model terlebih dahulu di halaman Hasil.")
    st.stop()

res = st.session_state["results"]["PCA_LDA"]

pca_model = res.get("pca_model")
lda_model = res.get("lda_model")
scaler = res.get("scaler")

if any(m is None for m in [pca_model, lda_model, scaler]):
    st.error("❌ Model belum siap. Jalankan kembali analisis.")
    st.stop()

with st.form("manual_pred_form"):
    tn = st.number_input("🌡️ Suhu Minimum (TN)")
    tx = st.number_input("🌡️ Suhu Maksimum (TX)")
    tavg = st.number_input("🌤️ Suhu Rata-rata (TAVG)")
    rh_avg = st.number_input("💧 Kelembapan Rata-rata (RH_AVG)")
    rr = st.number_input("🌧️ Curah Hujan (RR)")
    ss = st.number_input("☀️ Lama Penyinaran (SS)")
    ff_x = st.number_input("🌬️ Kecepatan Angin Maksimum (FF_X)")
    ddd_x = st.number_input("🧭 Arah Angin Maksimum (DDD_X)")
    ff_avg = st.number_input("🌬️ Kecepatan Angin Rata-rata (FF_AVG)")

    submitted = st.form_submit_button("🔍 Jalankan Klasifikasi")

if submitted:
    from utils.sanitize import sanitize_numeric_columns
    from utils.transformation import transform_wind_direction

    user_df = pd.DataFrame([{
        "tn": tn, "tx": tx, "tavg": tavg, "rh_avg": rh_avg, "rr": rr,
        "ss": ss, "ff_x": ff_x, "ddd_x": ddd_x, "ff_avg": ff_avg
    }])

    user_df = sanitize_numeric_columns(user_df)
    user_df = transform_wind_direction(user_df, "ddd_x")
    print(user_df)

    X_scaled = scaler.transform(user_df)
    X_transformed = pca_model.transform(X_scaled)

    y_pred = lda_model.predict(X_transformed)
    y_prob = lda_model.predict_proba(X_transformed)[0]

    st.success(f"✅ **Prediksi:** `{y_pred[0]}`")
    st.dataframe(
        pd.DataFrame({"Kelas": lda_model.classes_, "Probabilitas": np.round(y_prob, 3)}),
        hide_index=True
    )
