# 🏆 Komdigi x DQLab Hackathon Solutions

Repositori ini mendokumentasikan solusi lengkap saya dalam **Hackathon Komdigi x DQLab**, sebuah kompetisi coding intensif 24 jam yang menguji kemampuan pemecahan masalah, pengolahan data, dan kerja tim di bawah tekanan waktu. Saya berhasil menyelesaikan ketiga masalah yang diberikan dengan fokus pada akurasi, efisiensi, dan kolaborasi tim.

---

## 📋 Overview

Hackathon ini merupakan tantangan coding yang diselenggarakan oleh DQLab untuk peserta terpilih dari program Digital Talent Kominfo. Dalam periode 24 jam pada 18 November 2025, saya dan tim menghadapi tiga masalah kompleks yang mencakup:

- **Masalah 1**: Parsing dan pemetaan data transaksi dari berbagai format tanggal
- **Masalah 2**: Kategorisasi otomatis transaksi keuangan menggunakan teknik text matching
- **Masalah 3**: Simulasi bisnis multi-tahun untuk analisis investasi properti kos-kosan

**Individual Contribution**: Saya berkontribusi pada semua tiga masalah dengan kolaborasi tim untuk Masalah 1 dan 2, serta mengerjakan Masalah 3 secara mandiri. Hasil akhir menunjukkan output yang akurat, kode yang efisien, dan kemampuan beradaptasi dengan requirement yang berubah.

---

## 🎯 Hackathon Background

**Event Format**:
- Durasi: 24 jam non-stop
- Tanggal: 18 November 2025
- Sistem: Email-based (permintaan soal, submit kode, cek skor via tugastest@ujikompetensi.com)
- Setiap anggota tim mendapat tugas berbeda yang harus diselesaikan

**Judging Criteria**:
- **Correctness (Kebenaran)**: Output sesuai dengan ekspektasi yang ditentukan
- **Speed of Execution (Kecepatan Eksekusi)**: Waktu eksekusi program dan waktu pengiriman solusi
- **Originality (Orisinalitas)**: Solusi asli tanpa plagiarisme
- **Team Integration (Integrasi Tim)**: Skor individu berkontribusi ke skor tim dengan pengali performa kolektif

---

## 💡 Challenges and Solutions

### 🔹 Masalah 1: Parsing dan Pemetaan Tanggal Transaksi

**Tujuan**: Mengekstrak dan menormalisasi tanggal dari data transaksi keuangan yang memiliki format beragam (bahasa Indonesia dan Inggris, dengan atau tanpa singkatan).

**Pendekatan**:
- Membangun dictionary komprehensif untuk mapping nama bulan Indonesia dan Inggris
- Menggunakan regex pattern matching untuk mengenali berbagai format tanggal:
  - Format: "2024, 17 desember"
  - Format: "17 desember 2024"
  - Format: "7 aug '24"
- Normalisasi tahun 2-digit menjadi 4-digit
- Output standar: DD-MM-YYYY

**File Utama**:
- `parse_and_map.py`: Script untuk ekstraksi dan konversi tanggal
- `transaksi-raw-partial.xlsx`: Data input mentah
- `transaksi-output.xlsx`: Hasil parsing yang sudah dinormalisasi

**Hasil**: Berhasil memproses seluruh data transaksi dengan akurasi 100%, menghasilkan format tanggal yang konsisten untuk analisis lebih lanjut.

---

### 🔹 Masalah 2: Kategorisasi Otomatis Transaksi Keuangan

**Tujuan**: Mengklasifikasikan transaksi keuangan secara otomatis berdasarkan deskripsi, dengan mencocokkan ke kategori master akun (Pendapatan, Pengeluaran, Tarif Baru).

**Pendekatan**:
- Implementasi **n-gram matching** (unigram, bigram, trigram) untuk text similarity
- Text preprocessing: normalisasi, tokenisasi, stopword removal
- Mapping custom untuk istilah-istilah umum (contoh: "bulanan" → "bulan", "wi fi" → "wifi")
- Scoring system untuk menemukan kategori terbaik berdasarkan kecocokan token
- Post-processing untuk menentukan tanda nominal (positif/negatif) berdasarkan kategori

**File Utama**:
- `find_categories.py`: Script kategorisasi dengan n-gram matching
- `master_akun.xlsx`: Data referensi kategori dan akun
- `transaksi.xlsx`: Data transaksi input
- `transaksi dengan kategori.xlsx`: Output dengan kategori dan akun teridentifikasi

**Hasil**: Mencapai tingkat akurasi identifikasi kategori yang sangat baik, dengan hanya sebagian kecil transaksi yang masuk ke kategori "Tidak Dikenali". Sistem ini menunjukkan kemampuan NLP dasar yang efektif untuk aplikasi bisnis.

---

### 🔹 Masalah 3: Simulasi Investasi Properti Kos-Kosan

**Tujuan**: Membuat simulator bisnis yang memodelkan pertumbuhan investasi properti kos-kosan selama periode multi-tahun, dengan mempertimbangkan berbagai aturan bisnis dinamis seperti perubahan harga sewa, biaya pembangunan, dan threshold pembangunan.

**Pendekatan**:
- Simulasi month-by-month untuk setiap investor
- Implementasi sistem event-driven untuk menangani perubahan aturan berdasarkan periode
- Logika threshold kompleks (persentase atau nilai absolut) untuk menentukan kapan membangun kamar baru
- Perhitungan otomatis:
  - Peningkatan biaya pembangunan tahunan
  - Pendapatan sewa bulanan
  - Saldo dan total kamar pada setiap periode
- Support untuk event khusus per investor (contoh: stop building, perubahan harga sewa)

**File Utama**:
- `simulation.py`: Engine simulasi utama (200+ baris kode)
- `modal.xlsx`: Data modal awal dan parameter investor
- `informasi-tambahan.xlsx`: Rules dan event timeline
- `simulasi.xlsx`: Output detail per investor dan summary harta

**Hasil**: Menghasilkan timeline lengkap transaksi bulanan untuk setiap investor selama periode simulasi, dengan akurasi penghitungan finansial 100% dan kemampuan mengakomodasi skenario bisnis yang kompleks.

---

## 🛠️ Tech Stack

**Bahasa & Framework**:
- Python 3.x
- Pandas (manipulasi data dan Excel I/O)
- OpenPyXL (engine untuk writing Excel)
- Regex (pattern matching untuk parsing)

**Metodologi**:
- Text processing dan normalisasi
- N-gram based text similarity
- Event-driven simulation
- Data transformation dan validation

**Tools Pengembangan**:
- VS Code
- Git untuk version control
- Virtual environment (envtask3)

---

## 🎖️ Outcomes and Achievements

✅ **Menyelesaikan 3 dari 3 masalah** dalam batas waktu yang ditentukan

✅ **Akurasi Output**: Semua hasil sesuai ekspektasi dan lolos validasi

✅ **Kode yang Efisien**: Optimasi untuk kecepatan eksekusi dan penggunaan memori

✅ **Kolaborasi Tim**: Koordinasi efektif dalam pembagian tugas dan integrasi solusi

✅ **Adaptabilitas**: Mampu menangani requirement yang berkembang dan edge cases

**Skills Demonstrated**:
- Data wrangling dan cleaning
- Text processing dan pattern recognition
- Business logic implementation
- Algorithm optimization
- Team collaboration under pressure
- Problem decomposition

---

## 📚 What I Learned

1. **Manajemen Waktu**: Dalam hackathon 24 jam, prioritas dan time-boxing sangat krusial. Saya belajar untuk fokus pada MVP (Minimum Viable Product) dulu, baru optimasi.

2. **Kerja Tim**: Komunikasi yang jelas dan pembagian tugas yang tegas memungkinkan kami menyelesaikan lebih banyak dalam waktu singkat.

3. **Problem Solving**: Memecah masalah kompleks menjadi sub-masalah kecil membuat solusi lebih manageable dan testable.

4. **Kode yang Maintainable**: Meskipun under pressure, menulis kode yang clean dan commented sangat membantu saat debugging dan iterasi.

5. **Real-world Application**: Ketiga masalah ini mencerminkan tantangan nyata di dunia bisnis (parsing data mentah, kategorisasi otomatis, simulasi investasi), memberikan perspektif praktis yang valuable.

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas openpyxl
```

### Masalah 1
```bash
cd HACKATHON-01
python parse_and_map.py
# Output: transaksi-output.xlsx
```

### Masalah 2
```bash
cd HACKATHON-02
python find_categories.py
# Output: transaksi_dengan_kategori.xlsx
```

### Masalah 3
```bash
cd HACKATHON-03
python simulation.py
# Output: simulasi.xlsx
```

**Catatan**: Pastikan file Excel input (data mentah) berada di direktori yang sama dengan script Python.

---

## 📫 Contact

Interested in discussing this project or exploring collaboration opportunities? Feel free to reach out, I’d be happy to connect.

---
