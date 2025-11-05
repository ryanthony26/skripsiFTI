import streamlit as st
from utils.load_data import load_md
from pathlib import Path

# --- Load CSS ---
st.markdown(f"<style>{Path('assets/styles/style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Klasifikasi Pola Cuaca Ekstrem dengan Metode <span class='highlight'>PCA-LDA</span></h1>", unsafe_allow_html=True)

st.markdown(load_md("assets/data/desc.md"), unsafe_allow_html=True)

colA, colB, colC = st.columns([1, 1, 1])
with colB:
    if st.button("🚀 Mulai Uji Sekarang"):
         with st.spinner("Membuka halaman pengujian..."):
             st.switch_page("pages/data.py")