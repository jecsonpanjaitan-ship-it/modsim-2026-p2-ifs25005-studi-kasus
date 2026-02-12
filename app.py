import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Judul Dashboard
st.set_page_config(page_title="Dashboard Kuesioner", layout="wide")
st.title("📊 Dashboard Visualisasi Kuesioner")

# Mapping skala ke skor dan kategori
scale_to_score = {
    "SS": 6,
    "S": 5,
    "CS": 4,
    "CTS": 3,
    "TS": 2,
    "STS": 1
}

scale_to_category = {
    "SS": "Positif",
    "S": "Positif",
    "CS": "Netral",
    "CTS": "Negatif",
    "TS": "Negatif",
    "STS": "Negatif"
}

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("data_kuesioner.xlsx")
    return df

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("File 'data_kuesioner.xlsx' tidak ditemukan. Pastikan file berada di folder yang sama.")
    st.stop()

# Validasi: pastikan semua nilai valid
valid_scales = set(scale_to_score.keys())
all_values = df_raw.values.flatten()
if not set(all_values).issubset(valid_scales):
    invalid = set(all_values) - valid_scales
    st.warning(f"Nilai tidak valid ditemukan: {invalid}. Harap perbaiki data.")
    st.stop()

# Ubah ke skor numerik dan kategori
df_score = df_raw.replace(scale_to_score)
df_category = df_raw.replace(scale_to_category)

# Gabung semua jawaban menjadi satu series untuk analisis keseluruhan
all_answers = df_raw.melt(value_name="Jawaban")["Jawaban"]
all_categories = all_answers.map(scale_to_category)

# === 1. Bar Chart: Distribusi Jawaban Keseluruhan ===
st.subheader("1. Distribusi Jawaban Keseluruhan (Frekuensi)")
answer_counts = all_answers.value_counts().reindex(["SS", "S", "CS", "CTS", "TS", "STS"], fill_value=0)
fig1 = px.bar(
    x=answer_counts.index,
    y=answer_counts.values,
    labels={"x": "Skala", "y": "Frekuensi"},
    color=answer_counts.index,
    color_discrete_map={
        "SS": "#1f77b4",
        "S": "#6baed6",
        "CS": "#d9d9d9",
        "CTS": "#fd8d3c",
        "TS": "#f16913",
        "STS": "#d94801"
    }
)
st.plotly_chart(fig1, use_container_width=True)

# === 2. Pie Chart: Proporsi Jawaban Keseluruhan ===
st.subheader("2. Proporsi Jawaban Keseluruhan")
fig2 = px.pie(
    names=answer_counts.index,
    values=answer_counts.values,
    color=answer_counts.index,
    color_discrete_map={
        "SS": "#1f77b4",
        "S": "#6baed6",
        "CS": "#d9d9d9",
        "CTS": "#fd8d3c",
        "TS": "#f16913",
        "STS": "#d94801"
    }
)
st.plotly_chart(fig2, use_container_width=True)

# === 3. Stacked Bar: Distribusi Jawaban per Pertanyaan ===
st.subheader("3. Distribusi Jawaban per Pertanyaan")
question_dist = df_raw.apply(lambda col: col.value_counts()).fillna(0)
question_dist = question_dist.reindex(["SS", "S", "CS", "CTS", "TS", "STS"], fill_value=0)
question_dist = question_dist.T  # Transpose agar pertanyaan jadi index

fig3 = px.bar(
    question_dist,
    x=question_dist.index,
    y=["SS", "S", "CS", "CTS", "TS", "STS"],
    labels={"value": "Frekuensi", "x": "Pertanyaan"},
    color_discrete_map={
        "SS": "#1f77b4",
        "S": "#6baed6",
        "CS": "#d9d9d9",
        "CTS": "#fd8d3c",
        "TS": "#f16913",
        "STS": "#d94801"
    }
)
fig3.update_layout(barmode='stack')
st.plotly_chart(fig3, use_container_width=True)

# === 4. Bar Chart: Rata-rata Skor per Pertanyaan ===
st.subheader("4. Rata-rata Skor per Pertanyaan")
mean_scores = df_score.mean()
fig4 = px.bar(
    x=mean_scores.index,
    y=mean_scores.values,
    labels={"x": "Pertanyaan", "y": "Rata-rata Skor"},
    color=mean_scores.values,
    color_continuous_scale="Blues"
)
fig4.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig4, use_container_width=True)

# === 5. Bar Chart: Distribusi Kategori (Positif, Netral, Negatif) ===
st.subheader("5. Distribusi Kategori Jawaban")
category_counts = all_categories.value_counts().reindex(["Positif", "Netral", "Negatif"], fill_value=0)
fig5 = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    labels={"x": "Kategori", "y": "Jumlah"},
    color=category_counts.index,
    color_discrete_map={"Positif": "#2ca02c", "Netral": "#d9d9d9", "Negatif": "#d62728"}
)
st.plotly_chart(fig5, use_container_width=True)

# === BONUS: Heatmap Korelasi Skor Antar Pertanyaan ===
st.subheader("🎯 Bonus: Heatmap Korelasi Skor Antar Pertanyaan")
corr_matrix = df_score.corr()
fig_bonus = px.imshow(
    corr_matrix,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu_r",
    labels=dict(color="Korelasi")
)
st.plotly_chart(fig_bonus, use_container_width=True)

# === Info Tambahan ===
st.sidebar.header("ℹ️ Informasi")
st.sidebar.write("""
- **SS**: Sangat Setuju (6)  
- **S**: Setuju (5)  
- **CS**: Cukup Setuju (4)  
- **CTS**: Cenderung Tidak Setuju (3)  
- **TS**: Tidak Setuju (2)  
- **STS**: Sangat Tidak Setuju (1)  

Kategori:
- **Positif**: SS, S  
- **Netral**: CS  
- **Negatif**: CTS, TS, STS
""")