import streamlit as st
from pathlib import Path
from utils.load_data import load_md

# --- Load CSS ---
st.markdown(f"<style>{Path('assets/styles/style.css').read_text()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="guide-header">
    <h1>📖 Panduan Pengguna</h1>
    <p>
        Pelajari cara menggunakan aplikasi ini dengan mudah.  
        Panduan berikut menjelaskan fungsi dari setiap modul serta alur kerja.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

guide_md = load_md("assets/data/panduan.md")

st.markdown(
    f"<div class='guide-content'><div>{guide_md}</div></div>",
    unsafe_allow_html=True
)

with st.container():
    st.markdown("""
    <div class="tip-card">
        💡 <b>Tips:</b>  
        Gunakan data cuaca yang memiliki format dan satuan yang konsisten untuk hasil analisis PCA-LDA yang lebih akurat.
    </div>
    """, unsafe_allow_html=True)

