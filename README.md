# Student Performance Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis faktor-faktor
yang paling memengaruhi nilai akhir mahasiswa — mulai dari kebiasaan belajar,
kondisi psikologis, hingga latar belakang sosial-ekonomi.

---

## Deskripsi

Dashboard ini membaca data performa mahasiswa (CSV), lalu menyajikan:

- **Insight utama** — faktor dengan korelasi positif dan negatif terkuat terhadap nilai akhir.
- **Ranking faktor penentu** — perbandingan korelasi semua variabel numerik terhadap nilai akhir.
- **Pendalaman faktor positif** — hubungan jam belajar & sesi bimbingan dengan nilai.
- **Pendalaman faktor negatif** — dampak kecemasan ujian & stres terhadap nilai.
- **Sebaran nilai** — distribusi nilai akhir dan persentase mahasiswa berisiko.
- **Cek kesetaraan** — apakah gender, ekonomi keluarga, akses internet, dan ekstrakurikuler
  memengaruhi nilai secara signifikan.
- **Faktor gaya hidup sekunder** — pola makan dan pekerjaan paruh waktu.
- **Kesimpulan & rekomendasi** — ringkasan actionable di akhir halaman.

Seluruh chart bisa difilter secara interaktif lewat sidebar (gender, metode belajar,
pendapatan keluarga, kualitas pola makan, kualitas internet, pekerjaan paruh waktu,
dan keikutsertaan ekstrakurikuler).

---

## Struktur File

```
.
├── dashboard.py       # Kode utama dashboard
├── student_performance_finalscore_clean.csv  # Dataset
└── README.md
└── Requirements.txt
```

## Persyaratan

- Python 3.9+
- Library berikut:

```bash
pip install -r requirements.txt
```
---

## Format Dataset

File CSV (`student_performance_finalscore_clean.csv`) harus memiliki kolom berikut:

**Kolom kategorikal (berkode angka)**

| Kolom                   | 0        | 1        | 2        | 3       |
|-------------------------|----------|----------|----------|---------|
| `gender`                | Female   | Male     | Other    | –       |
| `study_method`          | Hybrid   | Offline  | Online   | –       |
| `family_income_level`   | High     | Low      | Middle   | –       |
| `diet_quality`          | Average  | Good     | Poor     | –       |
| `internet_quality`      | Average  | Excellent| Good     | Poor    |
| `part_time_job`         | No       | Yes      | –        | –       |
| `extracurricular`       | No       | Yes      | –        | –       |

**Kolom numerik**

`hours_studied`, `tutoring_sessions_per_week`, `previous_gpa`, `attendance`,
`sleep_hours`, `age`, `screen_time`, `stress_level`, `exam_anxiety_score`,
`final_score`
---

## Cara Menjalankan

1. Pastikan `student_performance_finalscore_clean.csv` berada di folder yang sama
   dengan `dashboard.py`.
2. Install dependencies (lihat bagian **requirements.txt**).
3. Jalankan:

```bash
streamlit run dashboard.py
```

4. Dashboard akan terbuka otomatis di browser (biasanya `http://localhost:8501`).

## Catatan

Dashboard ini dibuat untuk keperluan eksplorasi data performa mahasiswa dan dapat
disesuaikan untuk konteks analisis serupa.
Insight yang ditampilkan bersifat deskriptif (korelasi), bukan kausal — interpretasikan.