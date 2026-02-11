import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard Kuesioner", layout="wide")

st.title("📊 Dashboard Kuesioner Kepuasan")

# =========================
# LOAD DATA DENGAN AMAN
# =========================

@st.cache_data
def load_data():
    return pd.read_excel("data_kuesioner.xlsx")

if not os.path.exists("data_kuesioner.xlsx"):
    st.error("File data_kuesioner.xlsx tidak ditemukan di folder project.")
    st.stop()

try:
    df = load_data()
except Exception as e:
    st.error("Terjadi kesalahan saat membaca file Excel.")
    st.write(e)
    st.stop()

# =========================
# SIDEBAR FILTER
# =========================

st.sidebar.header("Filter Data")

questions = [col for col in df.columns if col.startswith("Q")]

selected_questions = st.sidebar.multiselect(
    "Pilih pertanyaan",
    questions,
    default=questions
)

if not selected_questions:
    st.warning("Pilih minimal satu pertanyaan.")
    st.stop()

data = df[selected_questions]

mapping = {
    "SS": 5,
    "S": 4,
    "CS": 3,
    "TS": 2,
    "STS": 1
}

data = data.replace(mapping)

# Tambahan ini supaya tidak error
data = data.apply(pd.to_numeric, errors='coerce')

mean_values = data.mean().reset_index()


# =========================
# HITUNG RATA-RATA
# =========================

mean_values = data.mean().reset_index()
mean_values.columns = ["Pertanyaan", "Rata-rata"]

# =========================
# VISUALISASI
# =========================

fig = px.bar(
    mean_values,
    x="Pertanyaan",
    y="Rata-rata",
    title="Rata-rata Nilai per Pertanyaan",
    text_auto=True
)

fig.update_layout(
    xaxis_title="Pertanyaan",
    yaxis_title="Rata-rata Skor",
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TAMPILKAN DATA MENTAH
# =========================

st.subheader("Data Mentah")
st.dataframe(df)
