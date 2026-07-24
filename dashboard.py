import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Dashboard")
st.markdown("Dashboard Analisis Performa Mahasiswa")
st.markdown("""
### 📖 Tentang Dataset

Dashboard ini menyajikan hasil analisis **Student Performance Dataset**, yaitu dataset yang berisi berbagai faktor yang memengaruhi prestasi akademik mahasiswa. 
Data mencakup informasi mengenai karakteristik mahasiswa, kebiasaan belajar, gaya hidup, serta kondisi lingkungan yang kemudian dibandingkan dengan **nilai akhir (Final Score)** yang diperoleh mahasiswa.
Melalui dashboard ini, pengguna dapat mengeksplorasi hubungan antara berbagai faktor seperti **jam belajar, tingkat kehadiran, metode belajar, kualitas internet, kualitas pola makan, pekerjaan paruh waktu, serta tingkat pendapatan keluarga** terhadap performa akademik mahasiswa.
""")

st.markdown("---")

# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():
    df = pd.read_csv("student_performance_finalscore_clean.csv")
    return df

df = load_data()

# Mapping Gender
gender_mapping = {
    0: "Female",
    1: "Male",
    2: "Other"
}

study_mapping = {
    0: "Hybrid",
    1: "Offline",
    2: "Online"
}

family_income_mapping = {
    0: "High",
    1: "Low",
    2: "Middle"
}

diet_quality_mapping = {
    0: "Average",
    1: "Good",
    2: "Poor"
}

internet_quality_mapping = {
    0: "Average",
    1: "Excellent",
    2: "Good",
    3: "Poor"
}

part_time_mapping = {
    0: "No",
    1: "Yes"
}

extracurricular_mapping = {
    0: "No",
    1: "Yes"
}

df["gender"] = df["gender"].replace(gender_mapping)
df["study_method"] = df["study_method"].replace(study_mapping)
df["family_income_level"] = df["family_income_level"].replace(family_income_mapping)
df["diet_quality"] = df["diet_quality"].replace(diet_quality_mapping)
df["internet_quality"] = df["internet_quality"].replace(internet_quality_mapping)
df["part_time_job"] = df["part_time_job"].replace(part_time_mapping)
df["extracurricular"] = df["extracurricular"].replace(extracurricular_mapping)

# ==========================
# SIDEBAR FILTER
# ==========================

st.sidebar.header("Filter Data")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

study_method = st.sidebar.multiselect(
    "Study Method",
    options=df["study_method"].unique(),
    default=df["study_method"].unique()
)

income = st.sidebar.multiselect(
    "Family Income",
    options=df["family_income_level"].unique(),
    default=df["family_income_level"].unique()
)

diet = st.sidebar.multiselect(
    "Diet Quality",
    options=df["diet_quality"].unique(),
    default=df["diet_quality"].unique()
)

internet = st.sidebar.multiselect(
    "Internet Quality",
    options=df["internet_quality"].unique(),
    default=df["internet_quality"].unique()
)

part_time = st.sidebar.multiselect(
    "Part Time Job",
    options=df["part_time_job"].unique(),
    default=df["part_time_job"].unique()
)

extracurricular = st.sidebar.multiselect(
    "Extracurricular",
    options=df["extracurricular"].unique(),
    default=df["extracurricular"].unique()
)

# ==========================
# FILTER DATA
# ==========================

df_selection = df.query(
    "gender == @gender and \
    study_method == @study_method and \
    family_income_level == @income and \
    diet_quality == @diet and \
    internet_quality == @internet and \
    part_time_job == @part_time and \
    extracurricular == @extracurricular"
)

# ==========================
# KPI
# ==========================

st.markdown("## 📊 Key Performance Indicator")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Final Score",
        round(df_selection["final_score"].mean(), 2)
    )

with col2:
    st.metric(
        "Average Study Hours",
        round(df_selection["hours_studied"].mean(), 2)
    )

with col3:
    st.metric(
        "Average Attendance",
        round(df_selection["attendance"].mean(), 2)
    )

with col4:
    st.metric(
        "Average Sleep Hours",
        round(df_selection["sleep_hours"].mean(), 2)
    )

st.metric(
    "Total Students",
    len(df_selection)
)

st.markdown("---")

# ==========================
# DATAFRAME
# ==========================

# st.subheader("Dataset")

# st.dataframe(df_selection)

# st.markdown("---")

# ==========================
# VISUAL 1
# DISTRIBUSI NILAI
# ==========================

study = (
    df_selection.groupby("study_method")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    study,
    x="study_method",
    y="final_score",
    color="study_method",
    text_auto=".2f",
    title="Average Final Score by Study Method"
)

st.plotly_chart(fig, use_container_width=True)

# Insight Otomatis
best_method = study.loc[study["final_score"].idxmax()]

st.success(
    f"""
### 📌 Insight

Metode belajar **{best_method['study_method']}** memiliki rata-rata nilai tertinggi yaitu **{best_method['final_score']:.2f}**.

Hal ini menunjukkan bahwa metode tersebut memberikan hasil akademik yang lebih baik dibandingkan metode belajar lainnya pada data yang sedang ditampilkan.
"""
)

# ==========================
# VISUAL 2
# ==========================

fig = px.histogram(
    df_selection,
    x="final_score",
    nbins=20,
    title="Distribution of Final Score"
)

st.plotly_chart(fig, use_container_width=True)

average = df_selection["final_score"].mean()
highest = df_selection["final_score"].max()
lowest = df_selection["final_score"].min()

st.info(
    f"""
### 📌 Insight

- Rata-rata nilai mahasiswa adalah **{average:.2f}**.
- Nilai tertinggi yang diperoleh adalah **{highest:.2f}**.
- Nilai terendah adalah **{lowest:.2f}**.

Distribusi ini memberikan gambaran mengenai penyebaran performa akademik mahasiswa pada data yang dipilih.
"""
)

# ==========================
# VISUAL 3
# ==========================

gender_score = (
    df_selection.groupby("gender")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    gender_score,
    x="gender",
    y="final_score",
    color="gender",
    text_auto=".2f",
    title="Average Final Score by Gender"
)

st.plotly_chart(fig, use_container_width=True)

best_gender = gender_score.loc[gender_score["final_score"].idxmax()]

st.info(
    f"""
### 📌 Insight

Mahasiswa dengan kategori **{best_gender['gender']}** memperoleh rata-rata nilai tertinggi yaitu **{best_gender['final_score']:.2f}**.

Namun, hasil ini hanya mencerminkan data yang dipilih melalui filter dan tidak dapat disimpulkan sebagai hubungan sebab-akibat.
"""
)

# ==========================
# VISUAL 4
# ==========================

income = (
    df_selection.groupby("family_income_level")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    income,
    x="family_income_level",
    y="final_score",
    color="family_income_level",
    text_auto=".2f",
    title="Average Final Score by Family Income"
)

st.plotly_chart(fig, use_container_width=True)

highest_income = income.loc[income["final_score"].idxmax()]

st.success(
    f"""
### 📌 Insight

Kategori pendapatan keluarga **{highest_income['family_income_level']}** memiliki rata-rata nilai tertinggi sebesar **{highest_income['final_score']:.2f}**.

Visualisasi ini membantu melihat apakah terdapat kecenderungan hubungan antara kondisi ekonomi keluarga dan prestasi akademik.
"""
)

# ==========================
# VISUAL 5
# CORRELATION
# ==========================

study_hour = (
    df_selection.groupby("hours_studied")["final_score"]
    .mean()
    .reset_index()
)

fig = px.scatter(
    df_selection,
    x="hours_studied",
    y="final_score",
    color="gender",
    title="Relationship Between Study Hours and Final Score",
    trendline="ols"
)

st.plotly_chart(fig, use_container_width=True)

corr = df_selection["hours_studied"].corr(df_selection["final_score"])

st.info(
    f"""
### 📌 Insight

Nilai korelasi antara jam belajar dan nilai akhir adalah **{corr:.2f}**.

Semakin mendekati **1**, hubungan positif antara jam belajar dan nilai semakin kuat. Semakin mendekati **0**, hubungan keduanya semakin lemah.
"""
)

# ==========================
# VISUAL 6
# ==========================

attendance = (
    df_selection.groupby("attendance")["final_score"]
    .mean()
    .reset_index()
)

fig = px.scatter(
    df_selection,
    x="attendance",
    y="final_score",
    color="gender",
    title="Relationship Between Attendance and Final Score",
    trendline="ols"
)

st.plotly_chart(fig,use_container_width=True)

corr_att = df_selection["attendance"].corr(df_selection["final_score"])

st.success(
    f"""
### 📌 Insight

Hubungan antara tingkat kehadiran dan nilai akhir memiliki nilai korelasi **{corr_att:.2f}**.

Semakin tinggi tingkat kehadiran mahasiswa, umumnya semakin baik pula nilai akhir yang diperoleh jika korelasinya bernilai positif.
"""
)

# ==========================
# VISUAL 7
# ==========================

internet_score = (
    df_selection.groupby("internet_quality")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    internet_score,
    x="internet_quality",
    y="final_score",
    color="internet_quality",
    text_auto=".2f",
    title="Average Final Score by Internet Quality"
)

st.plotly_chart(fig,use_container_width=True)

# ==========================
# INSIGHT
# ==========================

highest = internet_score.loc[internet_score["final_score"].idxmax()]
lowest = internet_score.loc[internet_score["final_score"].idxmin()]

st.success(f"""
### 📌 Insight

Kategori **{highest['internet_quality']}** memiliki rata-rata nilai akhir tertinggi yaitu **{highest['final_score']:.2f}**, sedangkan kategori **{lowest['internet_quality']}** memiliki rata-rata nilai terendah yaitu **{lowest['final_score']:.2f}**.

Grafik ini menunjukkan bahwa kualitas akses internet dapat berkaitan dengan performa akademik mahasiswa. Akses internet yang lebih baik berpotensi mendukung proses belajar melalui kemudahan memperoleh materi, mengikuti pembelajaran daring, dan mengakses berbagai sumber belajar.
""")

diet = (
    df_selection.groupby("diet_quality")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    diet,
    x="diet_quality",
    y="final_score",
    color="diet_quality",
    text_auto=".2f",
    title="Average Final Score by Diet Quality"
)

st.plotly_chart(fig,use_container_width=True)

best_diet = diet.loc[diet["final_score"].idxmax()]
lowest_diet = diet.loc[diet["final_score"].idxmin()]

st.info(f"""
### 📌 Insight

Kategori **{best_diet['diet_quality']}** memiliki rata-rata nilai akhir tertinggi sebesar **{best_diet['final_score']:.2f}**.

Sementara itu, kategori **{lowest_diet['diet_quality']}** memiliki rata-rata nilai akhir terendah sebesar **{lowest_diet['final_score']:.2f}**.

Hasil ini menunjukkan bahwa kualitas pola makan dapat berkaitan dengan performa akademik mahasiswa. Namun, hubungan ini bersifat deskriptif dan tidak menunjukkan sebab-akibat.
""")

job = (
    df_selection.groupby("part_time_job")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    job,
    x="part_time_job",
    y="final_score",
    color="part_time_job",
    text_auto=".2f",
    title="Average Final Score by Part Time Job"
)

st.plotly_chart(fig,use_container_width=True)

best_job = job.loc[job["final_score"].idxmax()]

st.success(f"""
### 📌 Insight

Mahasiswa dengan status **{best_job['part_time_job']}** memiliki rata-rata nilai akhir tertinggi sebesar **{best_job['final_score']:.2f}**.

Visualisasi ini menunjukkan adanya perbedaan rata-rata nilai antara mahasiswa yang memiliki pekerjaan paruh waktu dan yang tidak. Perbedaan tersebut dapat menjadi bahan analisis lebih lanjut mengenai pengaruh aktivitas di luar akademik terhadap hasil belajar.
""")

extra = (
    df_selection.groupby("extracurricular")["final_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    extra,
    x="extracurricular",
    y="final_score",
    color="extracurricular",
    text_auto=".2f",
    title="Average Final Score by Extracurricular"
)

st.plotly_chart(fig,use_container_width=True)

best_extra = extra.loc[extra["final_score"].idxmax()]

st.info(f"""
### 📌 Insight

Mahasiswa yang termasuk dalam kategori **{best_extra['extracurricular']}** memperoleh rata-rata nilai akhir tertinggi sebesar **{best_extra['final_score']:.2f}**.

Visualisasi ini membantu melihat apakah keikutsertaan dalam kegiatan ekstrakurikuler berkaitan dengan pencapaian akademik mahasiswa. Hasil ini merupakan gambaran dari data yang ditampilkan dan bukan merupakan hubungan sebab-akibat.
""")