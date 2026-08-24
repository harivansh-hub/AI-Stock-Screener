import joblib
import pandas as pd

from market_data import generate_market_data
from indicators import add_indicators
from features import create_features


model = joblib.load(
    "stock_model.pkl"
)


df = generate_market_data()

df = add_indicators(df)

df = create_features(df)


# Latest row for every stock

latest = (
    df
    .sort_values("timestamp")
    .groupby("stock")
    .tail(1)
)


features = [

    "smma_gap",
    "price_change",
    "ltq_avg_2",
    "ltq_avg_5",
    "ltq_ratio"

]


latest = latest.dropna(
    subset=features
)


X = latest[features]


probabilities = model.predict_proba(X)[
    :, 1
]


print("\n## ML TRADE ANALYSIS\n")


for i, (_, row) in enumerate(
    latest.iterrows()
):

    probability = probabilities[i]

    decision = (
        "ACCEPT"
        if probability >= 0.60
        else
        "AVOID"
    )

    print(
        f"{row['stock']:10} | "
        f"{row['direction']:10} | "
        f"Entry: {row['ltp']:.2f} | "
        f"Probability: {probability:.2%} | "
        f"{decision}"
    )