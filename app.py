import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analisis Kuesioner", layout="wide")

st.title("📊 Analisis Data Kuesioner")

# ===============================
# Load data
# ===============================
try:
    df = pd.read_excel("data_kuesioner.xlsx")
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

questions = [f"Q{i}" for i in range(1, 18)]
data = df[questions]

N = len(df)
TOTAL = data.size

skala_order = ["SS", "S", "CS", "CTS", "TS", "STS"]

def pct(j, t):
    return f"{(j / t * 100):.1f}%"

# ===============================
# Pilih pertanyaan
# ===============================
target = st.selectbox(
    "Pilih Analisis",
    [f"q{i}" for i in range(1, 14)]
)

st.divider()

# ===============================
# Proses sesuai pilihan
# ===============================
if target == "q1":
    vc = data.stack().value_counts().reindex(skala_order, fill_value=0)
    mx = vc.max()
    skala = [s for s in skala_order if vc[s] == mx][0]
    st.success(f"{skala} | {mx} | {pct(mx, TOTAL)}")

elif target == "q2":
    vc = data.stack().value_counts().reindex(skala_order, fill_value=0)
    mn = vc.min()
    skala = [s for s in skala_order if vc[s] == mn][0]
    st.success(f"{skala} | {mn} | {pct(mn, TOTAL)}")

elif target == "q3":
    cnt = {q: (data[q] == "SS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    st.success(f"{q} | {mx} | {pct(mx, N)}")

elif target == "q4":
    cnt = {q: (data[q] == "S").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    st.success(f"{q} | {mx} | {pct(mx, N)}")

elif target == "q5":
    cnt = {q: (data[q] == "CS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    st.success(f"{q} | {mx} | {pct(mx, N)}")

elif target == "q6":
    cnt = {q: (data[q] == "CTS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    st.success(f"{q} | {mx} | {pct(mx, N)}")

elif target == "q7":
    cnt = {q: (data[q] == "TS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    st.success(f"{q} | {mx} | {pct(mx, N)}")

elif target == "q8":
    cnt = {q: (data[q] == "STS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    st.success(f"{q} | {mx} | {pct(mx, N)}")

elif target == "q9":
    out = []
    for q in questions:
        j = (data[q] == "STS").sum()
        if j > 0:
            out.append(f"{q}: {pct(j, N)}")
    st.info(" | ".join(out) if out else "Tidak ada nilai STS")

elif target == "q10":
    skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}
    mean_all = data.replace(skor).stack().mean()
    st.success(f"Rata-rata keseluruhan: {mean_all:.2f}")

elif target == "q11":
    skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}
    mean = {q: data[q].replace(skor).mean() for q in questions}
    mx = max(mean.values())
    q = min(q for q in questions if mean[q] == mx)
    st.success(f"{q} : {mx:.2f}")

elif target == "q12":
    skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}
    mean = {q: data[q].replace(skor).mean() for q in questions}
    mn = min(mean.values())
    q = min(q for q in questions if mean[q] == mn)
    st.success(f"{q} : {mn:.2f}")

elif target == "q13":
    pos = data.isin(["SS", "S"]).sum().sum()
    neu = data.isin(["CS"]).sum().sum()
    neg = data.isin(["CTS", "TS", "STS"]).sum().sum()
    tot = pos + neu + neg

    st.write(
        f"**Positif** = {pos} ({pct(pos, tot)})  \n"
        f"**Netral** = {neu} ({pct(neu, tot)})  \n"
        f"**Negatif** = {neg} ({pct(neg, tot)})"
    )
