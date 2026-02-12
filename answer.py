import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

def main():
    # Baca data dari file Excel
    df = pd.read_excel("data_kuesioner.xlsx", sheet_name="Kuesioner")
    
    # Filter hanya kolom pertanyaan Q1-Q17
    pertanyaan_cols = [col for col in df.columns if str(col).startswith('Q') and str(col)[1:].isdigit() and 1 <= int(str(col)[1:]) <= 17]
    df_pertanyaan = df[pertanyaan_cols].copy()
    
    # Mapping skala ke skor
    skala_ke_skor = {'SS': 6, 'S': 5, 'CS': 4, 'CTS': 3, 'TS': 2, 'STS': 1}
    
    # Mapping untuk kategori
    kategori_mapping = {
        'SS': 'positif',
        'S': 'positif',
        'CS': 'netral',
        'CTS': 'negatif',
        'TS': 'negatif',
        'STS': 'negatif'
    }
    
    # Hitung total jawaban keseluruhan
    total_jawaban = df_pertanyaan.shape[0] * len(pertanyaan_cols)
    
    # q1: Skala paling banyak dipilih
    all_answers = df_pertanyaan.values.flatten()
    dist_overall = pd.Series(all_answers).value_counts()
    skala_terbanyak = dist_overall.idxmax()
    jumlah_terbanyak = dist_overall.max()
    persen_terbanyak = (jumlah_terbanyak / total_jawaban) * 100
    
    # q2: Skala paling sedikit dipilih
    skala_tersedikit = dist_overall.idxmin()
    jumlah_tersedikit = dist_overall.min()
    persen_tersedikit = (jumlah_tersedikit / total_jawaban) * 100
    
    # q3-q8: Pertanyaan dengan skala tertentu paling banyak
    def get_max_question_for_scale(scale):
        counts_per_q = df_pertanyaan.apply(lambda col: (col == scale).sum())
        max_q = counts_per_q.idxmax()
        max_count = counts_per_q.max()
        persen = (max_count / df_pertanyaan.shape[0]) * 100
        return max_q, max_count, persen
    
    # q9: Pertanyaan dengan STS
    sts_counts = df_pertanyaan.apply(lambda col: (col == 'STS').sum())
    sts_persen = (sts_counts / df_pertanyaan.shape[0]) * 100
    sts_questions = [(q, sts_persen[q]) for q in sts_counts.index if sts_counts[q] > 0]
    
    # q10: Skor rata-rata keseluruhan
    df_skor = df_pertanyaan.replace(skala_ke_skor)
    rata_rata_keseluruhan = df_skor.values.flatten().mean()
    
    # q11: Pertanyaan dengan rata-rata skor tertinggi
    rata_rata_per_q = df_skor.mean()
    q_tertinggi = rata_rata_per_q.idxmax()
    nilai_tertinggi = rata_rata_per_q.max()
    
    # q12: Pertanyaan dengan rata-rata skor terendah
    q_terendah = rata_rata_per_q.idxmin()
    nilai_terendah = rata_rata_per_q.min()
    
    # q13: Distribusi kategori
    df_kategori = df_pertanyaan.replace(kategori_mapping)
    kategori_counts = pd.Series(df_kategori.values.flatten()).value_counts()
    kategori_persen = (kategori_counts / total_jawaban) * 100
    
    # Baca input pertanyaan (tanpa prompt untuk kompatibilitas Delcom)
    target_question = input().strip()
    
    if target_question == "q1":
        print(f"{skala_terbanyak}|{jumlah_terbanyak}|{persen_terbanyak:.1f}")
    
    elif target_question == "q2":
        print(f"{skala_tersedikit}|{jumlah_tersedikit}|{persen_tersedikit:.1f}")
    
    elif target_question == "q3":
        q, count, persen = get_max_question_for_scale('SS')
        print(f"{q}|{count}|{persen:.1f}")
    
    elif target_question == "q4":
        q, count, persen = get_max_question_for_scale('S')
        print(f"{q}|{count}|{persen:.1f}")
    
    elif target_question == "q5":
        q, count, persen = get_max_question_for_scale('CS')
        print(f"{q}|{count}|{persen:.1f}")
    
    elif target_question == "q6":
        q, count, persen = get_max_question_for_scale('CTS')
        print(f"{q}|{count}|{persen:.1f}")
    
    elif target_question == "q7":
        q, count, persen = get_max_question_for_scale('TS')
        print(f"{q}|{count}|{persen:.1f}")
    
    elif target_question == "q8":
        q, count, persen = get_max_question_for_scale('TS')
        print(f"{q}|{count}|{persen:.1f}")
    
    elif target_question == "q9":
        if sts_questions:
            result = "|".join([f"{q}:{p:.1f}" for q, p in sts_questions])
            print(result)
        else:
            print("")
    
    elif target_question == "q10":
        print(f"{rata_rata_keseluruhan:.2f}")
    
    elif target_question == "q11":
        print(f"{q_tertinggi}:{nilai_tertinggi:.2f}")
    
    elif target_question == "q12":
        print(f"{q_terendah}:{nilai_terendah:.2f}")
    
    elif target_question == "q13":
        pos = kategori_counts.get('positif', 0)
        net = kategori_counts.get('netral', 0)
        neg = kategori_counts.get('negatif', 0)
        pos_p = kategori_persen.get('positif', 0.0)
        net_p = kategori_persen.get('netral', 0.0)
        neg_p = kategori_persen.get('negatif', 0.0)
        print(f"positif={int(pos)}:{pos_p:.1f}|netral={int(net)}:{net_p:.1f}|negatif={int(neg)}:{neg_p:.1f}")

if __name__ == "__main__":
    main()
