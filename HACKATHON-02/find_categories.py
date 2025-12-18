import pandas as pd
import re

STOPWORDS = {"kos", "kamar", "area", "pendapatan", "dan", "untuk", "dari",
             "karena", "penghuni", "ke", "kecil", "per", "layanan", "sakit",
             "januari", "februari", "maret", "april", "mei", "juni", "juni",
             "juli", "agustus", "september", "oktober", "november", "desember",
             "terlambat", "atau"}

NORMALIZE_MAP = {
    "bulanan": "bulan",
    "harian": "hari",
    "mingguan": "minggu",
    "tahunan": "tahun",
    "keterlambatan": "terlambat",
    "renov": "renovasi",
    "wi fi": "wifi",
    "internet": "wifi",
    "pembelian": "beli",
    "pengeluaran": "beli",
    "penyesuaian": "perubahan",
    "pam": "air",
    "tagihan": "biaya",
    "perawatan": "pemeliharaan",
    "tarif": "biaya",
    "harga": "biaya",
    "pembuatan":"pembangunan",
    "pembangunan": "bangun",
    "kenaikan": "perubahan",
    "harga kamar": "biaya sewa",
    "kost": "kos",
    'pdam':"air"
}

def normalize_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    for key, value in NORMALIZE_MAP.items():
        text = re.sub(r'\b' + key + r'\b', value, text)
    return text

def remove_duplicates(tokens):
    seen = set()
    unique_tokens = []
    for t in tokens:
        if t not in seen:
            unique_tokens.append(t)
            seen.add(t)
    return unique_tokens

def tokenize(text):
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = remove_duplicates(tokens) 
    return tokens

def remove_duplicates(tokens):
    seen = set()
    unique_tokens = []
    for t in tokens:
        if t not in seen:
            unique_tokens.append(t)
            seen.add(t)
    return unique_tokens

def generate_ngrams(tokens, n):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def get_all_ngrams_from_tokens(tokens):
    ngrams = set()
    for n in [1, 2, 3]:
        if len(tokens) >= n:
            ngrams.update(generate_ngrams(tokens, n))
    return ngrams

def process_ngram_matching(
    master_file="master_akun.xlsx",
    master_sheet="Data",
    trx_file="transaksi.xlsx",
    trx_sheet="Data",
    output_file="transaksi_dengan_kategori.xlsx",
    output_sheet="Data"
):
    df_master = pd.read_excel(master_file, sheet_name=master_sheet)
    df_trx = pd.read_excel(trx_file, sheet_name=trx_sheet)

    master_ngram_list = []
    master_tokens_list = []
    master_norm_list = []

    for desc in df_master["Deskripsi"]:
        norm = normalize_text(desc)
        tokens_master = tokenize(norm)
        ngrams_master = get_all_ngrams_from_tokens(tokens_master)

        master_norm_list.append(norm)
        master_tokens_list.append(tokens_master)
        master_ngram_list.append(ngrams_master)

    kategori_list = []
    akun_list = []

    for text in df_trx["Deskripsi Transaksi"]:
        norm_trx = normalize_text(text)
        tokens_trx = tokenize(norm_trx)

        trx_ngrams = get_all_ngrams_from_tokens(tokens_trx)

        best_score = 0
        best_idx = None

        for i, master_ngrams in enumerate(master_ngram_list):
            score = len(trx_ngrams.intersection(master_ngrams))
            if score > best_score:
                best_score = score
                best_idx = i

        if best_score > 0:
            kategori = df_master.loc[best_idx, "Kategori"]
            akun = df_master.loc[best_idx, "Deskripsi"]
        else:
            kategori = "Tidak Dikenali"
            akun = ""

        kategori_list.append(kategori)
        akun_list.append(akun)


    df_trx["Akun"] = akun_list
    df_trx["Kategori"] = kategori_list

    nominal_final = []
    tarif_baru = []

    for i, row in df_trx.iterrows():
        nilai = row["Nominal"]
        kategori = row["Kategori"]

        if kategori == "Pendapatan":
            nominal_final.append(abs(nilai))
            tarif_baru.append(0)
        elif kategori == "Pengeluaran":
            nominal_final.append(-abs(nilai))
            tarif_baru.append(0)
        elif kategori == "Tarif Baru":
            nominal_final.append(0)
            tarif_baru.append(abs(nilai))
        else:
            nominal_final.append(nilai)
            tarif_baru.append(0)

    df_trx["Nominal"] = nominal_final
    df_trx["Tarif Baru"] = tarif_baru

    df_output = df_trx[[
        "No",
        "Deskripsi Transaksi",
        "Akun",
        "Kategori",
        "Nominal",
        "Tarif Baru",
    ]]

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df_output.to_excel(writer, sheet_name=output_sheet, index=False)

    return df_output

process_ngram_matching(
    master_file="master_akun.xlsx",
    master_sheet="Data",
    trx_file="transaksi.xlsx",
    trx_sheet="Data",
    output_file="transaksi_dengan_kategori.xlsx",
    output_sheet="Data"
)