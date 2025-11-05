import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.pipeline import run_pipeline

st.header("Hasil Klasifikasi & Analisis Komparatif")

df = st.session_state.get("df_raw", None)
if df is None or df.empty:
    st.warning("⚠️ Tidak ada dataset yang tersimpan. Silakan upload & simpan data di menu **Data** terlebih dahulu.")
    st.stop()

df_name = st.session_state.get("df_name", "dataset")
if st.session_state.get("results_df_name") != df_name:
    st.session_state.pop("results", None)

st.subheader("⚙️ Pengaturan PCA")
col1, col2 = st.columns(2)
with col1:
    pca_mode = st.radio(
        "Pilih mode PCA:",
        ["Auto (Berdasarkan Variansi Kumulatif)", "Manual (Jumlah Komponen)"],
        horizontal=True,
        key="pca_mode"
    )
with col2:
    if pca_mode == "Auto (Berdasarkan Variansi Kumulatif)":
        explained_var = st.slider("Target Variansi Kumulatif", 0.70, 0.99, 0.95, 0.01, key="explained_var")
        manual_comp = None
    else:
        explained_var = None
        manual_comp = st.number_input("Jumlah Komponen PCA", min_value=2, max_value=10, value=3, key="manual_comp")

st.write("---")
run_btn = st.button("🚀 Jalankan Analisis", type="primary")


if run_btn:
    with st.spinner("Sedang menjalankan pipeline..."):
        result_pca_lda = run_pipeline(
            df.copy(),
            tmax_col="tx", rain_col="rr", wind_dir_col="ddd_x",
            explained_var=explained_var, manual_comp=manual_comp, use_pca=True
        )
        result_lda = run_pipeline(
            df.copy(),
            tmax_col="tx", rain_col="rr", wind_dir_col="ddd_x",
            use_pca=False
        )
        st.session_state["results"] = {"PCA_LDA": result_pca_lda, "LDA": result_lda}
        st.session_state["results_df_name"] = df_name
    st.success("✅ Analisis selesai!")

if "results" in st.session_state:
    res = st.session_state["results"]
   
    st.write("---")
    tab1, tab2 = st.tabs([
        "📈 Kinerja Model",
        "🧩 Variansi PCA",
    ])

    with tab1:
        st.subheader("📈 Perbandingan Kinerja Model PCA-LDA vs LDA")

        col1, col2 = st.columns(2)
        for model_name, color, col in [
            ("PCA_LDA", "Blues", col1),
            ("LDA", "Oranges", col2)
        ]:
            with col:
                model_label = "PCA + LDA" if model_name == "PCA_LDA" else "LDA"
                st.markdown(f"#### 🔹 {model_label}")
                acc = res[model_name]["accuracy"]
                st.metric("Akurasi Rata-rata", f"{acc:.3f}")

                # === Classification Report ===
                st.markdown("**Laporan Klasifikasi**")
                report_dict = res[model_name].get("report_dict", None)

                if report_dict:
                    report_df = pd.DataFrame(report_dict).T

                    # Ubah index angka → nama kelas asli
                    label_map = res[model_name].get("label_mapping", None)
                    if label_map:
                        report_df.index = [label_map.get(i, i) for i in report_df.index]

                    # Urutkan kolom
                    ordered = ["precision", "recall", "f1-score", "support"]
                    report_df = report_df[[c for c in ordered if c in report_df.columns]]

                    # ✅ Format angka 3 decimal, kecuali support → integer
                    for col in ["precision", "recall", "f1-score"]:
                        if col in report_df.columns:
                            report_df[col] = report_df[col].apply(lambda x: f"{x:.3f}" if isinstance(x, float) else x)

                    if "support" in report_df.columns:
                        report_df["support"] = report_df["support"].astype(int)

                    report_df.index.name = "Kelas"

                    st.table(report_df)

                # === Confusion Matrix ===
                st.markdown("**Confusion Matrix**")
                cm = res[model_name]["confusion"]

                # ✅ Ambil label kelas asli
                label_map = res[model_name].get("label_mapping", None)
                if label_map:
                    class_labels = [label_map[i] for i in range(cm.shape[0])]
                else:
                    class_labels = [str(i) for i in range(cm.shape[0])]

                fig, ax = plt.subplots()
                im = ax.imshow(cm, cmap=color)

                ax.set_xticks(np.arange(len(class_labels)))
                ax.set_yticks(np.arange(len(class_labels)))
                ax.set_xticklabels(class_labels, rotation=30, ha="right")
                ax.set_yticklabels(class_labels)
                ax.set_xlabel("Predicted")
                ax.set_ylabel("Actual")
                ax.set_title(f"Confusion Matrix — {model_label}")

                for i in range(cm.shape[0]):
                    for j in range(cm.shape[1]):
                        ax.text(j, i, cm[i, j], ha="center", va="center", color="black")

                fig.colorbar(im, ax=ax)
                st.pyplot(fig)

        st.write("---")
        st.subheader("🎯 Visualisasi Pemisahan Kelas (LDA Projection)")

        col_pca, col_lda = st.columns(2)

        class_colors = {
            "Normal": "tab:blue",
            "Hujan Ekstrem": "tab:green",
            "Suhu Ekstrem": "tab:red"
        }

        for model_name, color_map, col in [
            ("PCA_LDA", "Blues", col_pca),
            ("LDA", "Oranges", col_lda)
        ]:
            with col:
                model_label = "PCA + LDA" if model_name == "PCA_LDA" else "LDA"
                st.markdown(f"#### 🔹 {model_label}")

                if "lda_projection" in res[model_name]:
                    lda_proj = res[model_name]["lda_projection"]

                    fig_lda, ax_lda = plt.subplots()

                    if "LD2" in lda_proj.columns:
                        for lbl in np.unique(lda_proj["label"]):
                            subset = lda_proj[lda_proj["label"] == lbl]
                            color = class_colors.get(lbl, None)
                            ax_lda.scatter(subset["LD1"], subset["LD2"], label=str(lbl), alpha=0.7, color=color)
                        ax_lda.set_xlabel("LD1")
                        ax_lda.set_ylabel("LD2")
                    else:
                        for lbl in np.unique(lda_proj["label"]):
                            subset = lda_proj[lda_proj["label"] == lbl]
                            color = class_colors.get(lbl, None)
                            ax_lda.scatter(subset.index, subset["LD1"], label=str(lbl), alpha=0.7, color=color)
                        ax_lda.set_xlabel("Sampel")
                        ax_lda.set_ylabel("LD1")

                    ax_lda.set_title(f"Distribusi Data Berdasarkan Linear Discriminants\n({model_label})")
                    ax_lda.legend(title="Kelas")
                    st.pyplot(fig_lda)

                else:
                    st.info(f"Belum ada data proyeksi LDA untuk {model_label}.")

    with tab2:
        if "pca_model" in res["PCA_LDA"]:
            st.subheader("🧩 Analisis Variansi PCA")
            pca_model = res["PCA_LDA"]["pca_model"]
            explained_var_ratio = pca_model.explained_variance_ratio_
            cum_var = explained_var_ratio.cumsum()

            fig_var, ax_var = plt.subplots()
            ax_var.plot(range(1, len(cum_var) + 1), cum_var, marker="o")
            ax_var.axhline(0.95, color="red", linestyle="--", label="95% Variansi")
            ax_var.set_xlabel("Jumlah Komponen PCA")
            ax_var.set_ylabel("Variansi Kumulatif")
            ax_var.set_title("Kumulatif Variansi yang Dijelaskan oleh Komponen PCA")
            ax_var.legend()
            st.pyplot(fig_var)

        else:
            st.info("Model PCA belum tersedia untuk analisis variansi.")
else:
    st.info("Klik tombol **Jalankan Analisis** untuk melihat hasil perbandingan model.")
