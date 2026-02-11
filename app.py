import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Dashboard Kuesioner",
    layout="wide"
)

# =====================
# LOAD DATA (SINKRON answer.py)
# =====================
df = pd.read_excel("data_kuesioner.xlsx")

questions = [f"Q{i}" for i in range(1, 18)]
data = df[questions]

skala_order = ["SS", "S", "CS", "CTS", "TS", "STS"]
skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}

# =====================
# SIDEBAR
# =====================
st.sidebar.markdown("## 📊 ANALISIS KUESIONER")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filter Pertanyaan")
st.sidebar.multiselect(
    "Pilih pertanyaan",
    questions,
    default=questions
)

# =====================
# HEADER
# =====================
st.markdown(
    """
    <h2>📈 Dashboard Analisis Kuesioner</h2>
    <p style='color:gray;'>Sinkron 1–1 dengan answer.py</p>
    """,
    unsafe_allow_html=True
)

# =====================
# Q1 – BAR DISTRIBUSI TOTAL
# =====================
st.subheader("📊 Distribusi Jawaban Keseluruhan")

vc = (
    data.stack()
    .value_counts()
    .reindex(skala_order, fill_value=0)
    .reset_index()
)
vc.columns = ["Jawaban", "Jumlah"]

fig_bar = px.bar(
    vc,
    x="Jawaban",
    y="Jumlah",
    text="Jumlah"
)
st.plotly_chart(fig_bar, use_container_width=True)

# =====================
# PIE CHART
# =====================
st.subheader("🥧 Proporsi Jawaban")

fig_pie = px.pie(
    vc,
    names="Jawaban",
    values="Jumlah"
)
st.plotly_chart(fig_pie, use_container_width=True)

# =====================
# STACKED BAR PER PERTANYAAN
# =====================
st.subheader("📚 Distribusi Jawaban per Pertanyaan")

stacked = (
    data.apply(lambda x: x.value_counts())
    .T
    .reindex(columns=skala_order, fill_value=0)
    .reset_index()
)

fig_stack = px.bar(
    stacked,
    x="index",
    y=skala_order,
    barmode="stack",
    labels={"index": "Pertanyaan"}
)
st.plotly_chart(fig_stack, use_container_width=True)

# =====================
# RATA-RATA SKOR PER PERTANYAAN
# =====================
st.subheader("⭐ Rata-rata Skor per Pertanyaan")

mean_q = data.replace(skor).mean().reset_index()
mean_q.columns = ["Pertanyaan", "Rata-rata Skor"]

fig_mean = px.bar(
    mean_q,
    x="Pertanyaan",
    y="Rata-rata Skor",
    text="Rata-rata Skor"
)
st.plotly_chart(fig_mean, use_container_width=True)

# =====================
# POSITIF / NETRAL / NEGATIF (Q13)
# =====================
st.subheader("😊 Distribusi Jawaban Positif, Netral, Negatif")

pos = data.isin(["SS", "S"]).sum().sum()
neu = data.isin(["CS"]).sum().sum()
neg = data.isin(["CTS", "TS", "STS"]).sum().sum()

kat_df = pd.DataFrame({
    "Kategori": ["Positif", "Netral", "Negatif"],
    "Jumlah": [pos, neu, neg]
})

fig_kat = px.bar(
    kat_df,
    x="Kategori",
    y="Jumlah",
    text="Jumlah"
)
st.plotly_chart(fig_kat, use_container_width=True)

# =====================
# BONUS – RADAR CHART (FIXED & STABLE)
# =====================
st.subheader("Radar Chart Profil Kepuasan")

# pastikan tidak ada NaN
radar_df = mean_q.dropna()

fig_radar = px.line_polar(
    radar_df,
    r="Rata-rata Skor",
    theta="Pertanyaan",
    line_close=True
)

fig_radar.update_traces(fill="toself")
fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[1, 6]
        )
    )
)

st.plotly_chart(fig_radar, use_container_width=True)