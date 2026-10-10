"""Streamlit app: find Amazon listings that convert well but get little traffic, and vice versa.

Upload the Seller Central Business Report "Detail Page Sales and Traffic by Child Item".
"""
import numpy as np
import pandas as pd
import streamlit as st

# Column names differ between report versions; map them to one set.
COLUMN_ALIASES = {
    "(Child) ASIN": "asin",
    "Sessions": "sessions",
    "Sessions - Total": "sessions",
    "Page Views": "page_views",
    "Page Views - Total": "page_views",
    "Total Order Items": "orders",
}


def load_report(file) -> pd.DataFrame:
    raw = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
    df = raw.rename(columns=COLUMN_ALIASES)
    missing = {"asin", "sessions", "page_views", "orders"} - set(df.columns)
    if missing:
        raise ValueError(f"report is missing columns for: {', '.join(sorted(missing))}")
    df = df[["asin", "sessions", "page_views", "orders"]].copy()
    for col in ("sessions", "page_views", "orders"):
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
    return df


def score(df: pd.DataFrame, min_sessions: int) -> pd.DataFrame:
    """Conversion rate per page view: high = desirable but under-exposed, low = seen but not bought."""
    df = df[df["sessions"] > min_sessions].copy()
    df["conversion"] = df["orders"] / df["sessions"]
    df["score"] = df["conversion"] / df["page_views"]
    return df.replace([np.inf, -np.inf], np.nan).dropna().sort_values("score", ascending=False)


st.title("Amazon Listing Insights")
st.caption(
    "Upload your Business Report (Detail Page Sales and Traffic by Child Item) to see which "
    "ASINs deserve more advertising and which need a better listing."
)

uploaded = st.file_uploader("Business report", type=["csv", "xlsx"])
if uploaded is None:
    st.info("Waiting for a report…")
    st.stop()

try:
    report = load_report(uploaded)
except ValueError as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

min_sessions = st.number_input("Ignore ASINs with this many sessions or fewer", min_value=0, value=10, step=1)
top_n = st.slider("How many ASINs to show", 1, 100, 10)
ranked = score(report, min_sessions)

left, right = st.columns(2)
with left:
    st.subheader("Desirable, not discoverable")
    st.caption("Buy well when seen, but get little traffic → advertise them.")
    best = ranked.head(top_n)
    st.dataframe(best, hide_index=True)
    st.download_button("Download", best.to_csv(index=False), "desirable_not_discoverable.csv", "text/csv")
with right:
    st.subheader("Discoverable, not desirable")
    st.caption("Get traffic but rarely convert → fix price, images or copy.")
    worst = ranked.tail(top_n).iloc[::-1]
    st.dataframe(worst, hide_index=True)
    st.download_button("Download", worst.to_csv(index=False), "discoverable_not_desirable.csv", "text/csv")
