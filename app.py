import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        text-align: center;
    }
    .positive {
        color: #27ae60;
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

# Load data directly (without importing answer.py)
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name="Kuesioner")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    uploaded_file = st.file_uploader("Upload File Excel", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.success("✓ Data berhasil dimuat!")
    else:
        try:
            df = load_data("data_kuesioner.xlsx")
            if df is not None:
                st.success("✓ Data default berhasil dimuat!")
            else:
                st.error("File data_kuesioner.xlsx tidak ditemukan!")
                st.stop()
        except:
            st.error("File data_kuesioner.xlsx tidak ditemukan!")
            st.stop()
    
    # Filter only Q1-Q17 columns
    pertanyaan_cols = [col for col in df.columns if str(col).startswith('Q') and str(col)[1:].isdigit() and 1 <= int(str(col)[1:]) <= 17]
    df_pertanyaan = df[pertanyaan_cols].copy()
    
    # Display basic info
    st.header("📋 Informasi Data")
    total_responden = len(df_pertanyaan)
    total_pertanyaan = len(pertanyaan_cols)
    total_jawaban = total_responden * total_pertanyaan
    
    st.metric("Total Responden", total_responden)
    st.metric("Total Pertanyaan", total_pertanyaan)
    st.metric("Total Jawaban", total_jawaban)

# Mapping skala ke skor dan kategori
skala_ke_skor = {'SS': 6, 'S': 5, 'CS': 4, 'CTS': 3, 'TS': 2, 'STS': 1}
kategori_mapping = {
    'SS': 'Positif',
    'S': 'Positif',
    'CS': 'Netral',
    'CTS': 'Negatif',
    'TS': 'Negatif',
    'STS': 'Negatif'
}

# Prepare data for analysis
all_answers = df_pertanyaan.values.flatten()
dist_overall = pd.Series(all_answers).value_counts().reindex(['SS', 'S', 'CS', 'CTS', 'TS', 'STS'], fill_value=0)

# Convert to numeric scores
df_skor = df_pertanyaan.replace(skala_ke_skor)
rata_rata_per_q = df_skor.mean().round(2)
rata_rata_keseluruhan = df_skor.values.flatten().mean()

# Category distribution
df_kategori = df_pertanyaan.replace(kategori_mapping)
kategori_counts = pd.Series(df_kategori.values.flatten()).value_counts().reindex(['Positif', 'Netral', 'Negatif'], fill_value=0)
kategori_persen = (kategori_counts / kategori_counts.sum() * 100).round(1)

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Distribusi Keseluruhan", 
    "📊 Per Pertanyaan", 
    "⭐ Rata-rata Skor", 
    "🏷️ Kategori Jawaban", 
    "🎯 Analisis Lanjutan", 
    "ℹ️ Informasi"
])

with tab1:
    st.header("Distribusi Jawaban Keseluruhan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar Chart
        fig_bar = go.Figure(data=[
            go.Bar(
                x=dist_overall.index,
                y=dist_overall.values,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
                text=dist_overall.values,
                textposition='auto',
            )
        ])
        fig_bar.update_layout(
            title='Distribusi Jawaban Kuesioner (Keseluruhan)',
            xaxis_title='Skala Jawaban',
            yaxis_title='Jumlah Responden',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Pie Chart
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=dist_overall.index,
                values=dist_overall.values,
                hole=0.4,
                marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
                textinfo='label+percent',
                hoverinfo='label+value+percent'
            )
        ])
        fig_pie.update_layout(
            title='Proporsi Jawaban Kuesioner (Keseluruhan)',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Display raw data
    st.subheader("Tabel Distribusi Jawaban")
    st.dataframe(dist_overall.to_frame(name='Jumlah').style.background_gradient(cmap='Blues'))

with tab2:
    st.header("Distribusi Jawaban per Pertanyaan")
    
    # Stacked Bar Chart
    distribution_per_q = pd.DataFrame()
    for col in df_pertanyaan.columns:
        counts = df_pertanyaan[col].value_counts().reindex(['SS', 'S', 'CS', 'CTS', 'TS', 'STS'], fill_value=0)
        distribution_per_q[col] = counts
    
    fig_stacked = go.Figure()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, skala in enumerate(['SS', 'S', 'CS', 'CTS', 'TS', 'STS']):
        fig_stacked.add_trace(go.Bar(
            name=skala,
            x=distribution_per_q.columns,
            y=distribution_per_q.loc[skala],
            marker_color=colors[i],
            text=distribution_per_q.loc[skala],
            textposition='inside'
        ))
    
    fig_stacked.update_layout(
        title='Distribusi Jawaban per Pertanyaan (Q1-Q17)',
        xaxis_title='Pertanyaan',
        yaxis_title='Jumlah Responden',
        barmode='stack',
        template='plotly_white',
        height=500,
        legend_title='Skala Jawaban'
    )
    st.plotly_chart(fig_stacked, use_container_width=True)
    
    st.subheader("Tabel Distribusi per Pertanyaan")
    st.dataframe(distribution_per_q.style.background_gradient(cmap='Blues'))

with tab3:
    st.header("Rata-rata Skor per Pertanyaan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar Chart for average scores
        colors_avg = []
        for score in rata_rata_per_q.values:
            if score >= 5:
                colors_avg.append('#27ae60')  # Green
            elif score >= 4:
                colors_avg.append('#f39c12')  # Orange
            else:
                colors_avg.append('#e74c3c')  # Red
        
        fig_avg = go.Figure(data=[
            go.Bar(
                x=rata_rata_per_q.index,
                y=rata_rata_per_q.values,
                marker_color=colors_avg,
                text=rata_rata_per_q.values,
                textposition='auto',
            )
        ])
        fig_avg.add_hline(y=4, line_dash="dash", line_color="red", 
                         annotation_text="Threshold Netral (4)", annotation_position="bottom right")
        fig_avg.update_layout(
            title='Rata-rata Skor per Pertanyaan',
            xaxis_title='Pertanyaan',
            yaxis_title='Rata-rata Skor',
            template='plotly_white',
            height=400,
            yaxis_range=[0, 6.5]
        )
        st.plotly_chart(fig_avg, use_container_width=True)
    
    with col2:
        # Trend Line
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=rata_rata_per_q.index,
            y=rata_rata_per_q.values,
            mode='lines+markers',
            line=dict(color='#3498db', width=3),
            marker=dict(size=10, symbol='circle'),
            name='Rata-rata Skor'
        ))
        fig_trend.add_hline(y=4, line_dash="dash", line_color="orange", 
                           annotation_text="Threshold Netral")
        fig_trend.update_layout(
            title='Trend Rata-rata Skor per Pertanyaan',
            xaxis_title='Pertanyaan',
            yaxis_title='Rata-rata Skor',
            template='plotly_white',
            height=400,
            yaxis_range=[0, 6.5]
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Statistics summary
    st.subheader("Statistik Rata-rata Skor")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rata-rata Tertinggi", f"{rata_rata_per_q.max():.2f}", f"{rata_rata_per_q.idxmax()}")
    col2.metric("Rata-rata Terendah", f"{rata_rata_per_q.min():.2f}", f"{rata_rata_per_q.idxmin()}")
    col3.metric("Rata-rata Keseluruhan", f"{rata_rata_keseluruhan:.2f}")
    col4.metric("Standar Deviasi", f"{df_skor.values.flatten().std():.2f}")

with tab4:
    st.header("Distribusi Kategori Jawaban")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category distribution bar chart
        fig_cat = go.Figure(data=[
            go.Bar(
                x=kategori_counts.index,
                y=kategori_counts.values,
                marker_color=['#27ae60', '#f39c12', '#e74c3c'],
                text=[f"{count} ({persen}%)" for count, persen in zip(kategori_counts.values, kategori_persen.values)],
                textposition='auto',
            )
        ])
        fig_cat.update_layout(
            title='Distribusi Kategori Jawaban',
            xaxis_title='Kategori',
            yaxis_title='Jumlah Responden',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Category stacked bar per question
        cat_per_q = pd.DataFrame()
        for col in df_pertanyaan.columns:
            counts = df_pertanyaan[col].replace(kategori_mapping).value_counts().reindex(['Positif', 'Netral', 'Negatif'], fill_value=0)
            cat_per_q[col] = counts
        
        fig_cat_stacked = go.Figure()
        for i, cat in enumerate(['Positif', 'Netral', 'Negatif']):
            color = '#27ae60' if cat == 'Positif' else '#f39c12' if cat == 'Netral' else '#e74c3c'
            fig_cat_stacked.add_trace(go.Bar(
                name=cat,
                x=cat_per_q.columns,
                y=cat_per_q.loc[cat],
                marker_color=color,
                text=cat_per_q.loc[cat],
                textposition='inside'
            ))
        
        fig_cat_stacked.update_layout(
            title='Distribusi Kategori per Pertanyaan',
            xaxis_title='Pertanyaan',
            yaxis_title='Jumlah Responden',
            barmode='stack',
            template='plotly_white',
            height=400,
            legend_title='Kategori'
        )
        st.plotly_chart(fig_cat_stacked, use_container_width=True)
    
    # Category percentages display
    st.subheader("Persentase Kategori")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric-card"><span class="positive">✅ Positif:</span><br>{kategori_counts["Positif"]} ({kategori_persen["Positif"]}%)</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card"><span class="neutral">⚠️ Netral:</span><br>{kategori_counts["Netral"]} ({kategori_persen["Netral"]}%)</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card"><span class="negative">❌ Negatif:</span><br>{kategori_counts["Negatif"]} ({kategori_persen["Negatif"]}%)</div>', unsafe_allow_html=True)

with tab5:
    st.header("Analisis Lanjutan (Bonus)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar Chart
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=rata_rata_per_q.values.tolist() + [rata_rata_per_q.values[0]],
            theta=rata_rata_per_q.index.tolist() + [rata_rata_per_q.index[0]],
            fill='toself',
            marker=dict(size=8),
            line=dict(color='#27ae60', width=3)
        ))
        fig_radar.update_layout(
            title='Radar Chart: Performa Rata-rata per Pertanyaan',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 6],
                    tickmode='linear',
                    tick0=0,
                    dtick=1
                )
            ),
            template='plotly_white',
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Box Plot
        fig_box = go.Figure()
        for col in df_skor.columns:
            fig_box.add_trace(go.Box(
                y=df_skor[col],
                name=col,
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                marker=dict(size=4),
                line=dict(width=2)
            ))
        fig_box.update_layout(
            title='Box Plot: Distribusi Skor per Pertanyaan',
            xaxis_title='Pertanyaan',
            yaxis_title='Skor',
            template='plotly_white',
            height=450,
            yaxis_range=[0, 7]
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Heatmap
    st.subheader("Heatmap: Pola Jawaban")
    heatmap_data = pd.DataFrame()
    for col in df_pertanyaan.columns:
        counts = df_pertanyaan[col].value_counts().reindex(['SS', 'S', 'CS', 'CTS', 'TS', 'STS'], fill_value=0)
        heatmap_data[col] = counts
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdYlGn_r',
        text=heatmap_data.values,
        texttemplate='%{text}',
        textfont={'size': 10}
    ))
    fig_heatmap.update_layout(
        title='Heatmap: Distribusi Jawaban per Pertanyaan',
        xaxis_title='Pertanyaan',
        yaxis_title='Skala Jawaban',
        template='plotly_white',
        height=500
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab6:
    st.header("Informasi Dashboard")
    
    st.markdown("""
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
    
    ### 📈 Ringkasan Data
    
    Berdasarkan data yang dimuat:
    """)
    
    st.metric("Total Responden", len(df_pertanyaan))
    st.metric("Total Pertanyaan", len(pertanyaan_cols))
    st.metric("Rata-rata Keseluruhan", f"{rata_rata_keseluruhan:.2f}")
    st.metric("Persentase Positif", f"{kategori_persen['Positif']}%")
    st.metric("Persentase Netral", f"{kategori_persen['Netral']}%")
    st.metric("Persentase Negatif", f"{kategori_persen['Negatif']}%")
    
    st.markdown("---")
    st.subheader("📋 Contoh Data (5 baris pertama)")
    st.dataframe(df_pertanyaan.head())

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Dashboard Kuesioner Analytics &copy; 2026 | Powered by Streamlit & Plotly</p>
    </div>
""", unsafe_allow_html=True)
