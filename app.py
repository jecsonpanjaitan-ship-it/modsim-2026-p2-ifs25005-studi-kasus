import os
import pandas as pd
import streamlit as st

file_path = "data_kuesioner.xlsx"

if not os.path.exists(file_path):
    st.error("❌ File data_kuesioner.xlsx tidak ditemukan")
else:
    df = pd.read_excel(file_path)

    if df.empty:
        st.error("❌ File kosong")
    else:
        st.success("✅ Data berhasil dimuat")
        st.dataframe(df.head())
