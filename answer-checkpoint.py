import pandas as pd

df = pd.read_excel("data_kuesioner.xlsx")

questions = [f"Q{i}" for i in range(1, 18)]
data = df[questions]

N = len(df)
TOTAL = data.size

skala_order = ["SS", "S", "CS", "CTS", "TS", "STS"]

def pct(j, t):
    return f"{(j / t * 100):.1f}"

target = input().strip().lower()

# q1
if target == "q1":
    vc = data.stack().value_counts().reindex(skala_order, fill_value=0)
    mx = vc.max()
    skala = [s for s in skala_order if vc[s] == mx][0]
    print(f"{skala}|{mx}|{pct(mx, TOTAL)}")

# q2
elif target == "q2":
    vc = data.stack().value_counts().reindex(skala_order, fill_value=0)
    mn = vc.min()
    skala = [s for s in skala_order if vc[s] == mn][0]
    print(f"{skala}|{mn}|{pct(mn, TOTAL)}")

# q3
elif target == "q3":
    cnt = {q: (data[q] == "SS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    print(f"{q}|{mx}|{pct(mx, N)}")

# q4
elif target == "q4":
    cnt = {q: (data[q] == "S").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    print(f"{q}|{mx}|{pct(mx, N)}")

# q5
elif target == "q5":
    cnt = {q: (data[q] == "CS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    print(f"{q}|{mx}|{pct(mx, N)}")

# q6
elif target == "q6":
    cnt = {q: (data[q] == "CTS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    print(f"{q}|{mx}|{pct(mx, N)}")

# q7
elif target == "q7":
    cnt = {q: (data[q] == "TS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    print(f"{q}|{mx}|{pct(mx, N)}")

# q8
elif target == "q8":
    cnt = {q: (data[q] == "TS").sum() for q in questions}
    mx = max(cnt.values())
    q = min(q for q in questions if cnt[q] == mx)
    print(f"{q}|{mx}|{pct(mx, N)}")


# q9
elif target == "q9":
    out = []
    for q in questions:
        j = (data[q] == "STS").sum()
        if j > 0:
            out.append(f"{q}:{pct(j, N)}")
    print("|".join(out))

# q10
elif target == "q10":
    skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}
    mean_all = data.replace(skor).stack().mean()
    print(f"{mean_all:.2f}")

# q11
elif target == "q11":
    skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}
    mean = {q: data[q].replace(skor).mean() for q in questions}
    mx = max(mean.values())
    q = min(q for q in questions if mean[q] == mx)
    print(f"{q}:{mx:.2f}")

# q12
elif target == "q12":
    skor = {"SS":6, "S":5, "CS":4, "CTS":3, "TS":2, "STS":1}
    mean = {q: data[q].replace(skor).mean() for q in questions}
    mn = min(mean.values())
    q = min(q for q in questions if mean[q] == mn)
    print(f"{q}:{mn:.2f}")

# q13
elif target == "q13":
    pos = data.isin(["SS", "S"]).sum().sum()
    neu = data.isin(["CS"]).sum().sum()
    neg = data.isin(["CTS", "TS", "STS"]).sum().sum()
    tot = pos + neu + neg

    print(
        f"positif={pos}:{pct(pos, tot)}|"
        f"netral={neu}:{pct(neu, tot)}|"
        f"negatif={neg}:{pct(neg, tot)}"
    )
