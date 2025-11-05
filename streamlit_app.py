import streamlit as st

st.set_page_config(layout="wide")

home_page = st.Page(
    page="pages/home.py",
    title="Beranda",
    icon=":material/home:",
    default=True
)

train_page = st.Page(
    page="pages/data.py",
    title="Data",
    icon=":material/upload_file:",
)

result_page = st.Page(
    page="pages/result.py",
    title="Hasil",
    icon=":material/bar_chart:",
)

test_page = st.Page(
    page="pages/test.py",
    title="Uji",
    icon=":material/labs:",
)

guide_page = st.Page(
    page="pages/guide.py",
    title="Panduan",
    icon=":material/developer_guide:",
)

about_page = st.Page(
    page="pages/about.py",
    title="Tentang App",
    icon=":material/info:",
)

pg = st.navigation(
    {
        "Menu": [home_page, train_page, result_page, test_page, guide_page, about_page],
    }
)

pg.run()

