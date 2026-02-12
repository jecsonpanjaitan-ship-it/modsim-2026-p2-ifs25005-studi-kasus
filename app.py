import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from answer import create_analyzer, KuesionerAnalyzer, Visualizer

# Set page configuration
st.set_page_config(
    page_title="Dashboard Kuesioner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive {
        color: #2ecc71;
        font-weight: bold;
    }
    .neutral {
        color: #f39c12;
        font-weight: bold;
    }
    .negative {
        color: #e74c3c;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">📊 Dashboard Visualisasi Kuesioner</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload File Excel", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        file_path = uploaded_file
    else:
        file_path = "data_kuesioner.xlsx"
        st.info("Menggunakan file default: data_kuesioner.xlsx")
    
    # Create analyzer and visualizer
    try:
        analyzer, visualizer = create_analyzer(file_path)
        st.success("✓ Data berhasil dimuat!")
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()
    
    # Display basic info
    st.header("📋 Informasi Data")
    stats = analyzer.get_descriptive_statistics()
    
    st.metric("Total Responden", stats['total_respondents'])
    st.metric("Total Pertanyaan", stats['total_questions'])
    st.metric("Rata-rata Keseluruhan", f"{stats['overall_average']:.2f}")
    
    # Reliability analysis
    st.header("🔍 Analisis Keandalan")
    reliability = analyzer.get_reliability_analysis()
    st.metric("Cronbach's Alpha", reliability['cronbach_alpha'])
    st.caption(reliability['interpretation'])

# Main content
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Distribusi Keseluruhan", 
    "📊 Per Pertanyaan", 
    "⭐ Rata-rata Skor", 
    "🏷️ Kategori Jawaban", 
    "🎯 Analisis Lanjutan", 
    "🧮 Statistik Deskriptif", 
    "ℹ️ Informasi"
])

with tab1:
    st.header("Distribusi Jawaban Keseluruhan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(visualizer.create_overall_bar_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(visualizer.create_overall_pie_chart(), use_container_width=True)
    
    # Display raw data
    with st.expander("Lihat Data Mentah"):
        st.write("Distribusi Jawaban:")
        st.dataframe(analyzer.get_overall_distribution().to_frame().rename(columns={0: 'Jumlah'}))

with tab2:
    st.header("Distribusi Jawaban per Pertanyaan")
    
    st.plotly_chart(visualizer.create_stacked_bar_chart(), use_container_width=True)
    
    # Display distribution table
    with st.expander("Lihat Tabel Distribusi"):
        distribution_df = analyzer.get_distribution_per_question()
        st.dataframe(distribution_df.style.background_gradient(cmap='Blues'))

with tab3:
    st.header("Analisis Rata-rata Skor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(visualizer.create_average_scores_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(visualizer.create_trend_line(), use_container_width=True)
    
    # Display statistics
    avg_scores = analyzer.get_average_scores_per_question()
    st.subheader("Statistik Rata-rata Skor")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rata-rata Tertinggi", f"{avg_scores.max():.2f}", 
                f"Pertanyaan: {avg_scores.idxmax()}")
    col2.metric("Rata-rata Terendah", f"{avg_scores.min():.2f}", 
                f"Pertanyaan: {avg_scores.idxmin()}")
    col3.metric("Rata-rata Keseluruhan", f"{avg_scores.mean():.2f}")
    col4.metric("Standar Deviasi", f"{avg_scores.std():.2f}")

with tab4:
    st.header("Distribusi Kategori Jawaban")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(visualizer.create_category_distribution_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(visualizer.create_category_stacked_chart(), use_container_width=True)
    
    # Display category percentages
    st.subheader("Persentase Kategori")
    category_dist = analyzer.get_category_distribution()
    total = category_dist.sum()
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric-card"><span class="positive">✅ Positif:</span><br>{category_dist["Positif"]} ({category_dist["Positif"]/total*100:.1f}%)</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card"><span class="neutral">⚠️ Netral:</span><br>{category_dist["Netral"]} ({category_dist["Netral"]/total*100:.1f}%)</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card"><span class="negative">❌ Negatif:</span><br>{category_dist["Negatif"]} ({category_dist["Negatif"]/total*100:.1f}%)</div>', unsafe_allow_html=True)

with tab5:
    st.header("Analisis Lanjutan (Bonus)")
    
    st.subheader("Radar Chart - Performa Pertanyaan")
    st.plotly_chart(visualizer.create_radar_chart(), use_container_width=True)
    
    st.subheader("Box Plot - Distribusi Skor")
    st.plotly_chart(visualizer.create_box_plot(), use_container_width=True)
    
    st.subheader("Heatmap - Pola Jawaban")
    st.plotly_chart(visualizer.create_heatmap(), use_container_width=True)

with tab6:
    st.header("Statistik Deskriptif Lengkap")
    
    stats = analyzer.get_descriptive_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Ringkasan Data")
        st.metric("Total Responden", stats['total_respondents'])
        st.metric("Total Pertanyaan", stats['total_questions'])
        st.metric("Total Jawaban", len(analyzer.df) * len(analyzer.df.columns))
    
    with col2:
        st.subheader("📈 Statistik Skor")
        st.metric("Rata-rata Keseluruhan", f"{stats['overall_average']:.2f}")
        st.metric("Standar Deviasi", f"{stats['overall_std']:.2f}")
        st.metric("Skor Minimum", stats['min_score'])
        st.metric("Skor Maksimum", stats['max_score'])
    
    with col3:
        st.subheader("🔍 Keandalan")
        reliability = analyzer.get_reliability_analysis()
        st.metric("Cronbach's Alpha", reliability['cronbach_alpha'])
        st.caption(reliability['interpretation'])
        st.metric("Jumlah Item", reliability['item_count'])
    
    st.markdown("---")
    
    st.subheader("📋 Rata-rata Skor per Pertanyaan")
    avg_scores_df = analyzer.get_average_scores_per_question().to_frame().rename(columns={0: 'Rata-rata Skor'})
    avg_scores_df['Kategori'] = avg_scores_df['Rata-rata Skor'].apply(
        lambda x: 'Sangat Baik' if x >= 5 else ('Baik' if x >= 4 else 'Perlu Perbaikan')
    )
    st.dataframe(avg_scores_df.style.format({'Rata-rata Skor': '{:.2f}'}).background_gradient(cmap='RdYlGn', subset=['Rata-rata Skor']))
    
    st.subheader("📊 Distribusi Kategori")
    category_df = analyzer.get_category_distribution().to_frame().rename(columns={0: 'Jumlah'})
    category_df['Persentase'] = (category_df['Jumlah'] / category_df['Jumlah'].sum() * 100).round(2)
    st.dataframe(category_df.style.format({'Persentase': '{:.2f}%'}))

with tab7:
    st.header("Informasi Dashboard")
    
    st.markdown("""
    ### 📖 Tentang Dashboard
    
    Dashboard ini menyediakan visualisasi komprehensif untuk data kuesioner dengan berbagai jenis grafik dan analisis statistik.
    
    ### 🎯 Fitur Utama
    
    1. **Distribusi Keseluruhan**
       - Bar Chart: Menampilkan distribusi frekuensi semua jawaban
       - Pie Chart: Menampilkan proporsi persentase jawaban
    
    2. **Analisis per Pertanyaan**
       - Stacked Bar Chart: Distribusi jawaban untuk setiap pertanyaan
       - Tabel distribusi lengkap
    
    3. **Rata-rata Skor**
       - Bar Chart: Rata-rata skor per pertanyaan dengan threshold
       - Trend Line: Pola tren skor dengan moving average
    
    4. **Kategori Jawaban**
       - Bar Chart: Distribusi kategori (Positif, Netral, Negatif)
       - Stacked Bar: Distribusi kategori per pertanyaan
    
    5. **Analisis Lanjutan (Bonus)**
       - Radar Chart: Visualisasi performa multi-dimensi
       - Box Plot: Distribusi dan outlier skor
       - Heatmap: Pola jawaban secara visual
    
    ### 📊 Skala Penilaian
    
    | Skala | Nilai | Kategori |
    |-------|-------|----------|
    | SS (Sangat Setuju) | 6 | Positif |
    | S (Setuju) | 5 | Positif |
    | CS (Cukup Setuju) | 4 | Netral |
    | CTS (Cukup Tidak Setuju) | 3 | Negatif |
    | TS (Tidak Setuju) | 2 | Negatif |
    | STS (Sangat Tidak Setuju) | 1 | Negatif |
    
    ### 🔍 Interpretasi Kategori
    
    - **Positif (Skor 5-6)**: Respon yang mendukung/menguntungkan
    - **Netral (Skor 4)**: Respon yang cenderung netral
    - **Negatif (Skor 1-3)**: Respon yang tidak mendukung/kurang menguntungkan
    
    ### 📈 Analisis Keandalan
    
    Cronbach's Alpha digunakan untuk mengukur reliabilitas/keandalan instrumen:
    - ≥ 0.9: Excellent
    - ≥ 0.8: Good
    - ≥ 0.7: Acceptable
    - ≥ 0.6: Questionable
    - ≥ 0.5: Poor
    - < 0.5: Unacceptable
    
    ### 🛠️ Teknologi yang Digunakan
    
    - **Streamlit**: Framework untuk aplikasi web
    - **Plotly**: Library visualisasi interaktif
    - **Pandas**: Manipulasi dan analisis data
    - **NumPy**: Komputasi numerik
    
    ### 👨‍💻 Pengembang
    
    Dashboard ini dikembangkan untuk analisis kuesioner yang komprehensif dan interaktif.
    """)
    
    # Display data sample
    st.markdown("---")
    st.subheader("📋 Contoh Data")
    st.write("5 baris pertama dari dataset:")
    st.dataframe(analyzer.df.head())

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Dashboard Kuesioner Analytics &copy; 2026 | Powered by Streamlit & Plotly</p>
    </div>
""", unsafe_allow_html=True)