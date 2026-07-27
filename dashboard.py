import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# DESIGN TOKENS
# ==========================================================

NAVY = "#0B3D42"      # headers / dark text
TEAL = "#0F8B8D"      # positive driver / primary
CORAL = "#E85D4C"     # negative driver / risk
AMBER = "#F2A541"     # secondary / modest effect
SLATE = "#94A3A0"     # neutral / low-impact factors
BG_CARD = "#F6F9F8"
BORDER = "#E1E8E6"

CHART_FONT = "Inter, sans-serif"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  {{
    font-family: 'Inter', sans-serif;
}}
h1, h2, h3 {{
    font-family: 'Sora', sans-serif !important;
    color: {NAVY};
}}
.hero-box {{
    background: linear-gradient(135deg, {NAVY} 0%, #135e63 100%);
    padding: 28px 32px;
    border-radius: 14px;
    color: #EAF6F5;
    margin-bottom: 22px;
}}
.hero-box h2 {{
    color: #ffffff !important;
    margin-top: 0;
    font-size: 1.4rem;
}}
.hero-box p {{
    font-size: 1.02rem;
    line-height: 1.55;
    margin-bottom: 0;
    color: #DCEEEC;
}}
.section-eyebrow {{
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 0.75rem;
    font-weight: 600;
    color: {TEAL};
    margin-bottom: -6px;
}}
.insight-box {{
    background: {BG_CARD};
    border-left: 4px solid var(--accent, {TEAL});
    border-radius: 6px;
    padding: 14px 18px;
    margin: 6px 0 22px 0;
    font-size: 0.95rem;
    line-height: 1.55;
    color: #24312F;
}}
.insight-box b {{ color: {NAVY}; }}
div[data-testid="stMetric"] {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 12px 6px 8px 14px;
}}
hr {{ border-color: {BORDER}; }}
</style>
""", unsafe_allow_html=True)


def section_header(eyebrow, title):
    st.markdown(f'<div class="section-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f"### {title}")


def insight_box(html, accent=TEAL):
    st.markdown(
        f'<div class="insight-box" style="--accent:{accent}">{html}</div>',
        unsafe_allow_html=True
    )


def style_fig(fig, height=420):
    fig.update_layout(
        font=dict(family=CHART_FONT, color=NAVY, size=13),
        title=dict(font=dict(size=16, family="Sora, sans-serif", color=NAVY)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=60, b=40, l=10, r=10),
        height=height,
        showlegend=fig.layout.showlegend if fig.layout.showlegend is not None else False,
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEF2F1", zeroline=False)
    return fig


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("student_performance_finalscore_clean.csv")
    return df

df = load_data()

gender_mapping = {0: "Female", 1: "Male", 2: "Other"}
study_mapping = {0: "Hybrid", 1: "Offline", 2: "Online"}
family_income_mapping = {0: "High", 1: "Low", 2: "Middle"}
diet_quality_mapping = {0: "Average", 1: "Good", 2: "Poor"}
internet_quality_mapping = {0: "Average", 1: "Excellent", 2: "Good", 3: "Poor"}
part_time_mapping = {0: "No", 1: "Yes"}
extracurricular_mapping = {0: "No", 1: "Yes"}

df["gender"] = df["gender"].map(gender_mapping)
df["study_method"] = df["study_method"].map(study_mapping)
df["family_income_level"] = df["family_income_level"].map(family_income_mapping)
df["diet_quality"] = df["diet_quality"].map(diet_quality_mapping)
df["internet_quality"] = df["internet_quality"].map(internet_quality_mapping)
df["part_time_job"] = df["part_time_job"].map(part_time_mapping)
df["extracurricular"] = df["extracurricular"].map(extracurricular_mapping)

# Friendly labels for the numeric "driver" variables
DRIVER_LABELS = {
    "hours_studied": "Jam Belajar",
    "tutoring_sessions_per_week": "Sesi Bimbingan/Minggu",
    "previous_gpa": "IPK Sebelumnya",
    "attendance": "Tingkat Kehadiran",
    "sleep_hours": "Jam Tidur",
    "age": "Usia",
    "screen_time": "Waktu Layar",
    "stress_level": "Tingkat Stres",
    "exam_anxiety_score": "Kecemasan Ujian",
}

# ==========================================================
# SIDEBAR FILTER
# ==========================================================

st.sidebar.header("🔍 Filter Data")

gender = st.sidebar.multiselect("Gender", options=df["gender"].unique(), default=df["gender"].unique())
study_method = st.sidebar.multiselect("Study Method", options=df["study_method"].unique(), default=df["study_method"].unique())
income = st.sidebar.multiselect("Family Income", options=df["family_income_level"].unique(), default=df["family_income_level"].unique())
diet = st.sidebar.multiselect("Diet Quality", options=df["diet_quality"].unique(), default=df["diet_quality"].unique())
internet = st.sidebar.multiselect("Internet Quality", options=df["internet_quality"].unique(), default=df["internet_quality"].unique())
part_time = st.sidebar.multiselect("Part Time Job", options=df["part_time_job"].unique(), default=df["part_time_job"].unique())
extracurricular = st.sidebar.multiselect("Extracurricular", options=df["extracurricular"].unique(), default=df["extracurricular"].unique())

df_selection = df.query(
    "gender == @gender and \
    study_method == @study_method and \
    family_income_level == @income and \
    diet_quality == @diet and \
    internet_quality == @internet and \
    part_time_job == @part_time and \
    extracurricular == @extracurricular"
)

st.title("🎓 Student Performance Dashboard")
st.caption("Analisis faktor-faktor di balik nilai akhir mahasiswa")

if df_selection.empty or len(df_selection) < 10:
    st.warning("⚠️ Kombinasi filter ini menghasilkan data yang terlalu sedikit untuk dianalisis. Silakan ubah filter di sidebar.")
    st.stop()

# ==========================================================
# COMPUTE CORE STATS (used across the page)
# ==========================================================

numeric_drivers = list(DRIVER_LABELS.keys())
corr_series = df_selection[numeric_drivers + ["final_score"]].corr()["final_score"].drop("final_score")
corr_series = corr_series.sort_values(ascending=False)

top_positive = corr_series.index[0]
top_negative = corr_series.index[-1]

at_risk_threshold = 60
at_risk_pct = (df_selection["final_score"] < at_risk_threshold).mean() * 100

# Equity check range (categorical, low-impact factors)
equity_factors = {
    "Gender": "gender",
    "Pendapatan Keluarga": "family_income_level",
    "Kualitas Internet": "internet_quality",
    "Ekstrakurikuler": "extracurricular",
}
equity_ranges = {}
for label, col in equity_factors.items():
    g = df_selection.groupby(col)["final_score"].mean()
    equity_ranges[label] = g.max() - g.min()

# ==========================================================
# HERO — headline thesis of the dashboard
# ==========================================================

st.markdown(f"""
<div class="hero-box">
<h2>📌 Insight Utama</h2>
<p>
Nilai akhir mahasiswa paling kuat berkaitan dengan <b>{DRIVER_LABELS[top_positive]}</b>
(korelasi {corr_series[top_positive]:+.2f}) dan paling kuat menurun seiring naiknya
<b>{DRIVER_LABELS[top_negative]}</b> (korelasi {corr_series[top_negative]:+.2f}).
Sebaliknya, faktor latar belakang seperti gender, pendapatan keluarga, kualitas internet,
dan keikutsertaan ekstrakurikuler hanya menyumbang perbedaan rata-rata kurang dari 1 poin —
menunjukkan bahwa performa akademik lebih ditentukan oleh <b>kebiasaan belajar dan kondisi
psikologis</b> mahasiswa, bukan oleh latar belakang atau akses mereka.
</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# KPI ROW
# ==========================================================

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Rata-rata Nilai Akhir", f"{df_selection['final_score'].mean():.1f}")
k2.metric("Rata-rata Jam Belajar", f"{df_selection['hours_studied'].mean():.1f} jam")
k3.metric("Rata-rata Kehadiran", f"{df_selection['attendance'].mean():.0f}%")
k4.metric(f"Berisiko (<{at_risk_threshold})", f"{at_risk_pct:.1f}%")
k5.metric("Total Mahasiswa", f"{len(df_selection):,}")

st.markdown("---")

# ==========================================================
# SECTION 1 — DRIVER RANKING (hero chart)
# ==========================================================

section_header("Faktor Penentu", "Apa yang Paling Memengaruhi Nilai Akhir?")

corr_df = corr_series.reset_index()
corr_df.columns = ["variable", "correlation"]
corr_df["label"] = corr_df["variable"].map(DRIVER_LABELS)
corr_df["arah"] = corr_df["correlation"].apply(lambda x: "Meningkatkan Nilai" if x > 0 else "Menurunkan Nilai")

fig = px.bar(
    corr_df.sort_values("correlation"),
    x="correlation",
    y="label",
    orientation="h",
    color="arah",
    color_discrete_map={"Meningkatkan Nilai": TEAL, "Menurunkan Nilai": CORAL},
    text=corr_df.sort_values("correlation")["correlation"].map(lambda x: f"{x:+.2f}"),
    title="Korelasi Setiap Faktor terhadap Nilai Akhir",
    labels={"correlation": "Koefisien Korelasi", "label": ""},
)
fig.update_traces(textposition="outside")
fig = style_fig(fig, height=430)
fig.update_layout(showlegend=True, legend_title="")
st.plotly_chart(fig, use_container_width=True)

insight_box(f"""
<b>{DRIVER_LABELS[top_positive]}</b> dan <b>sesi bimbingan belajar</b> adalah dua pendorong nilai
terkuat — semakin banyak keduanya, semakin tinggi nilai akhir. Di sisi lain,
<b>{DRIVER_LABELS[top_negative]}</b> dan tingkat stres berkorelasi negatif: semakin tinggi
kecemasan/stres mahasiswa, semakin rendah kecenderungan nilainya. Grafik ini menjadi acuan
untuk dua bagian berikutnya, yang membedah faktor-faktor dengan pengaruh terbesar ini lebih dalam.
""", accent=TEAL)

st.markdown("---")

# ==========================================================
# SECTION 2 — DEEP DIVE: POSITIVE DRIVERS
# ==========================================================

section_header("Pendalaman", "Dua Faktor yang Paling Mendorong Nilai Naik")

c1, c2 = st.columns(2)

with c1:
    fig = px.scatter(
        df_selection,
        x="hours_studied",
        y="final_score",
        color="gender",  # Warna berdasarkan gender
        trendline="ols",
        opacity=0.6,
        title="Jam Belajar vs Nilai Akhir",
        labels={
            "hours_studied": "Jam Belajar/Minggu",
            "final_score": "Nilai Akhir",
            "gender": "Gender"
        },
        color_discrete_map={
            "Male": "#3B82F6",      # Biru
            "Female": "#EC4899",    # Pink
            "Other": "#10B981"      # Hijau
        }
    )

    fig.update_traces(marker=dict(size=6))

    st.plotly_chart(
        style_fig(fig, height=380),
        use_container_width=True
    )

with c2:
    tutor = df_selection.groupby("tutoring_sessions_per_week")["final_score"].mean().reset_index()
    fig = px.bar(
        tutor, x="tutoring_sessions_per_week", y="final_score",
        text_auto=".1f",
        color_discrete_sequence=[TEAL],
        title="Sesi Bimbingan/Minggu vs Rata-rata Nilai",
        labels={"tutoring_sessions_per_week": "Sesi Bimbingan/Minggu", "final_score": "Rata-rata Nilai"},
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(style_fig(fig, height=380), use_container_width=True)

hours_corr = corr_series["hours_studied"]
tutor_gain = tutor["final_score"].iloc[-1] - tutor["final_score"].iloc[0]
insight_box(f"""
Korelasi jam belajar terhadap nilai akhir sebesar <b>{hours_corr:+.2f}</b> — salah satu hubungan
terkuat di dataset ini. Pola serupa terlihat pada bimbingan belajar: mahasiswa dengan sesi bimbingan
terbanyak rata-rata unggul sekitar <b>{tutor_gain:+.1f} poin</b> dibanding yang tanpa bimbingan sama sekali.
Keduanya adalah faktor yang <b>dapat dikendalikan</b> mahasiswa maupun institusi — menjadikannya
titik intervensi paling realistis untuk meningkatkan performa akademik.
""", accent=TEAL)

st.markdown("---")

# ==========================================================
# SECTION 3 — DEEP DIVE: NEGATIVE / WELLBEING DRIVER
# ==========================================================

section_header("Pendalaman", "Kecemasan Ujian: Faktor Penurun Nilai Terbesar")

fig = px.scatter(
    df_selection, x="exam_anxiety_score", y="final_score",
    trendline="ols", opacity=0.35,
    color_discrete_sequence=[CORAL],
    title="Skor Kecemasan Ujian vs Nilai Akhir",
    labels={"exam_anxiety_score": "Skor Kecemasan Ujian", "final_score": "Nilai Akhir"},
)
fig.update_traces(marker=dict(size=5))
st.plotly_chart(style_fig(fig, height=380), use_container_width=True)

anxiety_corr = corr_series["exam_anxiety_score"]
stress_corr = corr_series["stress_level"]
insight_box(f"""
Kecemasan ujian berkorelasi <b>{anxiety_corr:+.2f}</b> terhadap nilai akhir — hubungan negatif
terkuat di antara semua faktor yang diukur. Tingkat stres harian menunjukkan pola yang sejalan
(korelasi {stress_corr:+.2f}). Ini menunjukkan bahwa <b>kondisi psikologis mahasiswa saat menjelang
dan selama ujian</b> berdampak nyata terhadap hasil belajar, sehingga dukungan manajemen stres dan
kecemasan patut dipertimbangkan sebagai bagian dari strategi peningkatan performa akademik —
sejajar pentingnya dengan jam belajar.
""", accent=CORAL)

st.markdown("---")

# ==========================================================
# SECTION 4 — DISTRIBUTION / AT-RISK
# ==========================================================

section_header("Sebaran Nilai", "Berapa Banyak Mahasiswa yang Berisiko?")

fig = px.histogram(
    df_selection, x="final_score", nbins=30,
    color_discrete_sequence=[TEAL],
    title="Distribusi Nilai Akhir Mahasiswa",
    labels={"final_score": "Nilai Akhir"},
)
fig.add_vline(x=at_risk_threshold, line_dash="dash", line_color=CORAL,
              annotation_text=f"Batas Risiko ({at_risk_threshold})", annotation_position="top")
st.plotly_chart(style_fig(fig, height=380), use_container_width=True)

insight_box(f"""
Rata-rata nilai akhir mahasiswa pada data terpilih adalah <b>{df_selection['final_score'].mean():.1f}</b>,
dengan rentang dari <b>{df_selection['final_score'].min():.1f}</b> hingga
<b>{df_selection['final_score'].max():.1f}</b>. Sekitar <b>{at_risk_pct:.1f}%</b> mahasiswa berada
di bawah ambang {at_risk_threshold}, kelompok inilah yang paling membutuhkan intervensi berupa
tambahan jam bimbingan atau dukungan manajemen stres, sesuai dua faktor utama pada bagian sebelumnya.
""", accent=TEAL)

st.markdown("---")

# ==========================================================
# SECTION 5 — EQUITY CHECK (low-impact background factors)
# ==========================================================

section_header("Cek Kesetaraan", "Apakah Latar Belakang Mahasiswa Berpengaruh?")

equity_long = []
for label, col in equity_factors.items():
    g = df_selection.groupby(col)["final_score"].mean().reset_index()
    g.columns = ["kategori", "rata_rata_nilai"]
    g["faktor"] = label
    equity_long.append(g)
equity_df = pd.concat(equity_long, ignore_index=True)

overall_avg = df_selection["final_score"].mean()

fig = px.bar(
    equity_df, x="kategori", y="rata_rata_nilai",
    facet_col="faktor", facet_col_wrap=4,
    color_discrete_sequence=[SLATE],
    text_auto=".1f",
    title="Rata-rata Nilai Akhir berdasarkan Latar Belakang",
    labels={"rata_rata_nilai": "Rata-rata Nilai", "kategori": ""},
)
fig.update_yaxes(matches=None, range=[0, 100])
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1], font=dict(size=12, color=NAVY)))
fig.add_hline(y=overall_avg, line_dash="dot", line_color=AMBER)
fig.update_traces(textposition="outside")
st.plotly_chart(style_fig(fig, height=380), use_container_width=True)

widest_factor = max(equity_ranges, key=equity_ranges.get)
insight_box(f"""
Garis putus-putus menandai rata-rata nilai keseluruhan ({overall_avg:.1f}). Keempat faktor latar
belakang ini semuanya bertumpu sangat dekat dengan garis tersebut — selisih terbesar hanya pada
<b>{widest_factor}</b> ({equity_ranges[widest_factor]:.2f} poin). Artinya gender, kondisi ekonomi
keluarga, kualitas akses internet, dan keikutsertaan ekstrakurikuler <b>bukan pembeda utama</b>
performa akademik pada data ini — berbeda dari jam belajar dan kondisi psikologis yang dampaknya
jauh lebih besar.
""", accent=AMBER)

st.markdown("---")

# ==========================================================
# SECTION 6 — SECONDARY LIFESTYLE FACTORS
# ==========================================================

section_header("Faktor Sekunder", "Gaya Hidup yang Masih Berdampak Sedang")

c1, c2 = st.columns(2)

with c1:
    diet_g = df_selection.groupby("diet_quality")["final_score"].mean().reset_index()
    fig = px.bar(
        diet_g, x="diet_quality", y="final_score",
        color="diet_quality", text_auto=".1f",
        color_discrete_map={"Good": TEAL, "Average": AMBER, "Poor": CORAL},
        title="Kualitas Pola Makan vs Rata-rata Nilai",
        labels={"diet_quality": "Kualitas Pola Makan", "final_score": "Rata-rata Nilai"},
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(style_fig(fig, height=360), use_container_width=True)

with c2:
    job_g = df_selection.groupby("part_time_job")["final_score"].mean().reset_index()
    fig = px.bar(
        job_g, x="part_time_job", y="final_score",
        color="part_time_job", text_auto=".1f",
        color_discrete_map={"No": TEAL, "Yes": AMBER},
        title="Pekerjaan Paruh Waktu vs Rata-rata Nilai",
        labels={"part_time_job": "Pekerjaan Paruh Waktu", "final_score": "Rata-rata Nilai"},
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(style_fig(fig, height=360), use_container_width=True)

diet_range = diet_g["final_score"].max() - diet_g["final_score"].min()
job_range = job_g["final_score"].max() - job_g["final_score"].min()
insight_box(f"""
Pola makan menunjukkan selisih <b>{diet_range:.1f} poin</b> antara kategori terbaik dan terburuk,
sementara mahasiswa dengan pekerjaan paruh waktu rata-rata <b>{job_range:.1f} poin</b> lebih rendah
dibanding yang tidak bekerja. Keduanya bukan faktor utama seperti jam belajar atau kecemasan ujian,
namun cukup untuk dipertimbangkan sebagai dukungan pelengkap — misalnya edukasi gizi atau
keringanan beban akademik bagi mahasiswa yang bekerja.
""", accent=AMBER)

# ==========================================================
# CLOSING SUMMARY
# ==========================================================

st.markdown("---")
section_header("Kesimpulan", "Ringkasan & Rekomendasi")
st.markdown(f"""
- 📈 **Tingkatkan akses bimbingan belajar** — sesi bimbingan menunjukkan hubungan positif yang
  konsisten dengan nilai akhir dan merupakan intervensi yang paling mudah ditambah.
- 🧘 **Perhatikan kesehatan psikologis mahasiswa** — kecemasan ujian dan stres adalah dua
  faktor penurun nilai terbesar; dukungan konseling dapat berdampak signifikan.
- 🎯 **Fokuskan bantuan pada {at_risk_pct:.0f}% mahasiswa berisiko** (nilai di bawah {at_risk_threshold})
  ketimbang menyasar berdasarkan latar belakang, karena gender, ekonomi keluarga, dan akses internet
  terbukti bukan pembeda utama performa akademik.
- 🍽️ **Faktor gaya hidup** seperti pola makan dan pekerjaan paruh waktu berperan sebagai
  pendukung tambahan, bukan penentu utama.
""")

with st.expander("📄 Lihat data mentah (sesuai filter)"):
    st.dataframe(df_selection, use_container_width=True)