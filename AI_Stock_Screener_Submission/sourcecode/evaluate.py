import pandas as pd

from sklearn.model_selection import train_test_split
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


# 80% training / 20% unseen testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Train model ONLY on training data
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# Predict unseen test data
probabilities = model.predict_proba(X_test)[:, 1]


test_results = df.loc[X_test.index].copy()

test_results["profit_probability"] = probabilities


# ML accepts probability >= 60%
accepted = test_results[
    test_results["profit_probability"] >= 0.60
]


# SMMA baseline
smma_win_rate = (
    y_test.sum() / len(y_test)
) * 100


# ML filtered result
if len(accepted) > 0:

    ml_win_rate = (
        accepted["profitable"].sum()
        / len(accepted)
    ) * 100

else:

    ml_win_rate = 0


print("\n========== UNSEEN TEST ==========")

print(
    f"SMMA Only       : "
    f"{smma_win_rate:.2f}% profitable"
)

print(
    f"ML Filter       : "
    f"{ml_win_rate:.2f}% profitable"
)

print(
    f"\nTest Trades     : {len(test_results)}"
)

print(
    f"ML Accepted     : {len(accepted)}"
)

print(
    f"ML Profitable   : "
    f"{accepted['profitable'].sum()}"
)

print("=================================")