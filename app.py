import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI News Dashboard", layout="wide")

st.title("📰 AI News Scraper Dashboard")

# Load data
df = pd.read_csv("output.csv")

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔍 Filters")

# Search box
search = st.sidebar.text_input("Search News")

# Category filter (if exists)
if "category" in df.columns:
    categories = ["All"] + list(df["category"].dropna().unique())
    selected_category = st.sidebar.selectbox("Category", categories)
else:
    selected_category = "All"

# ---------------- Filtering Logic ----------------
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df.astype(str).apply(
            lambda row: row.str.contains(search, case=False).any(), axis=1
        )
    ]

if selected_category != "All" and "category" in df.columns:
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

# ---------------- Metrics ----------------
col1, col2 = st.columns(2)

col1.metric("Total Records", len(df))
col2.metric("Filtered Records", len(filtered_df))

st.divider()

# ---------------- Data Display ----------------
st.subheader("📊 News Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- Download Button ----------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "news_data.csv",
    "text/csv"
)