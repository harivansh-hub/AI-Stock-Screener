import streamlit as st
import pandas as pd
import joblib

from market_data import generate_market_data
from indicators import add_indicators
from features import create_features


# -------------------------
# PAGE
# -------------------------

st.set_page_config(

    page_title="AI Stock Screener",

    page_icon="📊",

    layout="wide"
)


st.title("📊 AI Stock Screener")

st.caption(
    "SMMA Crossover + Random Forest"
)


# -------------------------
# MODEL
# -------------------------

model = joblib.load(
    "stock_model.pkl"
)


# -------------------------
# MARKET DATA
# -------------------------

df = generate_market_data()

df = add_indicators(df)

df = create_features(df)


# -------------------------
# LATEST STOCK DATA
# -------------------------

latest = (

    df
    .sort_values("timestamp")
    .groupby("stock")
    .tail(1)
    .copy()

)


# -------------------------
# REMOVE MISSING VALUES
# -------------------------

feature_columns = [

    "smma_gap",
    "price_change",
    "ltq_avg_2",
    "ltq_avg_5",
    "ltq_ratio"

]


latest = latest.dropna(
    subset=feature_columns
)


# -------------------------
# ML
# -------------------------

X = latest[
    feature_columns
]


probabilities = model.predict_proba(
    X
)[:, 1]


latest["probability"] = (
    probabilities
)


latest["decision"] = latest[
    "probability"
].apply(

    lambda x:
    "ACCEPT"
    if x >= 0.60
    else
    "AVOID"

)


# -------------------------
# DISPLAY DATA
# -------------------------

display_df = latest[

    [

        "stock",

        "ltp",

        "smma20",

        "smma120",

        "smma_gap",

        "ltq",

        "ltq_avg_2",

        "ltq_avg_5",

        "ltq_ratio",

        "direction",

        "probability",

        "decision"

    ]

].copy()


display_df["probability"] = (

    display_df["probability"]
    .map(
        lambda x:
        f"{x:.2%}"
    )

)


display_df.columns = [

    "Stock",

    "LTP",

    "SMMA20",

    "SMMA120",

    "SMMA Gap",

    "LTQ",

    "LTQ Avg 2",

    "LTQ Avg 5",

    "LTQ Ratio",

    "Signal",

    "Profit Probability",

    "Decision"

]


# -------------------------
# SUMMARY
# -------------------------

accepted = (

    latest["decision"]
    == "ACCEPT"

).sum()


st.subheader(

    f"Stocks: {len(latest)} | "
    f"ML Accepted: {accepted}"

)


# -------------------------
# TABLE
# -------------------------

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True

)


# -------------------------
# REFRESH
# -------------------------

if st.button("🔄 Refresh"):

    st.rerun()