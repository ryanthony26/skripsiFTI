import streamlit as st
import pandas as pd

st.title("Upload & Validasi Dataset")

REQUIRED_FEATURES = ["TANGGAL", "TN", "TX", "TAVG", "RH_AVG", "RR", "SS", "FF_X", "DDD_X", "FF_AVG"]

def read_any(file):
    name = file.name.lower()
    return pd.read_csv(file) if name.endswith(".csv") else pd.read_excel(file)

# --- State initialization ---
for key, val in {
    "df_raw": None,
    "df_name": None,
    "just_reset": False
}.items():
    st.session_state.setdefault(key, val)

# --- Helper functions ---
def reset_dataset():
    st.session_state.df_raw = None
    st.session_state.df_name = None
    if "results" in st.session_state:
        st.session_state.pop("results")
    st.session_state.just_reset = True
    st.rerun()

def save_dataset(df, file_name):
    st.session_state.df_raw = df
    st.session_state.df_name = file_name
    st.rerun()

# --- Toast reset ---
if st.session_state.just_reset:
    st.toast("Dataset berhasil direset!", icon="🗑️")
    st.session_state.just_reset = False

# --- If data saved ---
if st.session_state.df_raw is not None:
    st.success(f"✅ Dataset '{st.session_state.df_name}' sudah tersimpan dalam session.")
    
    if st.button("🔄 Reset Dataset"):
        reset_dataset()

    st.dataframe(st.session_state.df_raw.head(20))

    if st.button("➡️ Lanjut ke Hasil & Analisis"):
        st.switch_page("pages/result.py")

else:
    # --- Template CSV ---
    with st.expander("📄 Butuh template CSV?"):
        if st.button("Buat & Unduh Template"):
            df_temp = pd.DataFrame([{
                "TANGGAL": "2025-01-01",
                "TN": 23.4,
                "TX": 32.5,
                "TAVG": 28.1,
                "RH_AVG": 82.3,
                "RR": 15.6,
                "SS": 7.2,
                "FF_X": 10.5,
                "DDD_X": 180,
                "FF_AVG": 5.4
            }])
            st.download_button(
                label="⬇️ Download template_dataset.csv",
                data=df_temp.to_csv(index=False),
                file_name="template_dataset.csv",
                mime="text/csv"
            )

    # --- Upload baru ---
    file = st.file_uploader("📤 Upload dataset (CSV/XLSX)", type=["csv", "xlsx", "xls"])
    if file:
        try:
            df = read_any(file)
            df.columns = df.columns.str.strip().str.lower()
            st.dataframe(df.head(20))

            missing = [c for c in [f.lower() for f in REQUIRED_FEATURES] if c not in df.columns]
            if missing:
                st.error(f"Kolom wajib berikut belum ada di dataset: {', '.join(missing)}")
            else:
                date_col = "tanggal" if "tanggal" in df.columns else "date"
                df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="raise")
                df = df.sort_values(date_col).reset_index(drop=True)
                st.success("✅ Kolom tanggal valid dan data sudah diurutkan.")

                if st.button("💾 Simpan Dataset"):
                    save_dataset(df, file.name)

        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
