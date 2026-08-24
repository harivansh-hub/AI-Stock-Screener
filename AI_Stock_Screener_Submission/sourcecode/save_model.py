import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("training_data.csv")

df = pd.get_dummies(
    df,
    columns=["market_type", "direction"],
    dtype=int
)

features = [
    "smma_gap",
    "ltq_ratio",
    "ltq_avg_2",
    "ltq_avg_5",
    "price_change",
    "market_type_bull",
    "market_type_bear",
    "market_type_sideways",
    "direction_BUY",
    "direction_SELL"
]

df = df.dropna(subset=features)

X = df[features]
y = df["profitable"]

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

model.fit(X, y)

joblib.dump(
    model,
    "stock_model.pkl"
)

print("Model saved successfully!")