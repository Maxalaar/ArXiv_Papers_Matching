from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# Config
# =========================
st.set_page_config(
    page_title="ArXiv Papers Explorer",
    layout="wide"
)

# =========================
# Load data
# =========================
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["published_date"] = pd.to_datetime(df["published_date"])
    return df


data_path = Path(
    "/home/malaarabiou/Programming_Projects/Pycharm_Projects/ArXiv_Papers_Matching/results/xrl/data.csv"
)
df = load_data(data_path)

# =========================
# Header
# =========================
st.title("📚 ArXiv Papers Explorer")
st.caption(f"{len(df)} articles indexés")

# =========================
# Sidebar – Filters
# =========================
st.sidebar.header("🎛️ Filtres")

years = st.sidebar.slider(
    "Année de publication",
    int(df.year.min()),
    int(df.year.max()),
    (int(df.year.min()), int(df.year.max()))
)

categories = st.sidebar.multiselect(
    "Catégories principales",
    sorted(df.primary_category.unique())
)

search = st.sidebar.text_input("🔍 Recherche texte (titre / résumé / auteurs)")

# =========================
# Filtering
# =========================
filtered = df[df.year.between(*years)]

if categories:
    filtered = filtered[filtered.primary_category.isin(categories)]

if search:
    mask = filtered[["title", "summary", "authors"]].apply(
        lambda row: row.str.contains(search, case=False).any(),
        axis=1
    )
    filtered = filtered[mask]

# =========================
# Stats
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📄 Articles", len(filtered))
col2.metric(
    "📅 Années couvertes",
    f"{filtered.year.min()} – {filtered.year.max()}"
)
col3.metric(
    "🏷️ Catégories",
    filtered.primary_category.nunique()
)

# =========================
# Timeline
# =========================
st.subheader("📈 Évolution temporelle")

timeline = (
    filtered
    .groupby("year")
    .size()
    .reset_index(name="count")
)

fig_timeline = px.bar(
    timeline,
    x="year",
    y="count",
    labels={
        "year": "Année",
        "count": "Nombre d'articles"
    }
)

st.plotly_chart(fig_timeline, width="stretch")

# =========================
# Category distribution
# =========================
st.subheader("🏷️ Répartition par catégorie")

cat_dist = (
    filtered
    .primary_category
    .value_counts()
    .rename_axis("primary_category")
    .reset_index(name="count")
)

fig_cat = px.pie(
    cat_dist,
    names="primary_category",
    values="count",
    title="Distribution des catégories"
)

st.plotly_chart(fig_cat, width="stretch")

# =========================
# Table
# =========================
st.subheader("📄 Articles")

table = (
    filtered[
        [
            "title",
            "authors",
            "year",
            "primary_category",
            "published_date",
            "url"
        ]
    ]
    .sort_values("published_date", ascending=False)
)

st.dataframe(
    table,
    width="stretch",
    height=500
)

# =========================
# Article viewer
# =========================
st.subheader("🔍 Détails de l'article")

selected_title = st.selectbox(
    "Sélectionner un article",
    table["title"]
)

article = df[df.title == selected_title].iloc[0]

st.markdown(f"### {article.title}")
st.markdown(f"**Auteurs :** {article.authors}")
st.markdown(f"**Catégorie :** `{article.primary_category}`")
st.markdown(f"**Publié le :** {article.published_date.date()}")
st.markdown(f"[📄 Accéder à l'article]({article.url})")

with st.expander("📝 Résumé"):
    st.write(article.summary)
