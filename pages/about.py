import streamlit as st
from PIL import Image
from utils.load_data import load_md

informasi = {
    "Principal Component Analysis": """
Principal Component Analysis (PCA) adalah metode reduksi dimensi yang digunakan untuk menyederhanakan
data berdimensi tinggi dengan tetap mempertahankan variasi terbesar dalam dataset. PCA membantu menyoroti
pola utama dalam data.
""",

    "Linear Discriminant Analysis": """
Linear Discriminant Analysis (LDA) adalah teknik klasifikasi yang mencari kombinasi fitur yang memaksimalkan
pemisahan antar kelas. 
""",

    "ETCCDI (Expert Team on Climate Change Detection and Indices)": """
ETCCDI adalah kelompok pakar internasional yang mengembangkan standar dan indeks statistik untuk
mendeteksi perubahan iklim dan kejadian cuaca ekstrem. Indeks ETCCDI banyak digunakan dalam penelitian
iklim karena menggunakan metode yang konsisten dan dapat dibandingkan antar wilayah dan waktu.
"""

}
photo = Image.open("assets/images/Ijazah.png")

c1, c2 = st.columns([1, 3], vertical_alignment="center")
with c1:
    st.image(photo, width=160, output_format="PNG")
with c2:
    st.markdown(load_md("assets/data/biodata.md"))

st.markdown("### Sinopsis")
st.write(load_md("assets/data/sinopsis.md"))

st.markdown("### Informasi Terkait")

for judul, isi in informasi.items():
    with st.expander(judul):
        st.write(isi)
