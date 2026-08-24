import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from market_data import generate_market_data
from indicators import add_indicators
from features import create_features


# -------------------------
# DATA
# -------------------------

df = generate_market_data()

df = add_indicators(df)

df = create_features(df)


# -------------------------
# CREATE PROFITABLE LABEL
# -------------------------

df["future_price"] = (
    df.groupby("stock")["ltp"]
    .shift(-5)
)

df["profitable"] = (
    df["future_price"]
    >
    df["ltp"]
).astype(int)


# Remove incomplete rows

df = df.dropna()


# -------------------------
# FEATURES
# -------------------------

feature_columns = [

    "smma_gap",
    "price_change",
    "ltq_avg_2",
    "ltq_avg_5",
    "ltq_ratio"

]


X = df[feature_columns]

y = df["profitable"]


# -------------------------
# TRAIN / TEST
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nDATASET")

print(
    "Total trades:",
    len(df)
)

print(
    y.value_counts()
)


print("\nTRAIN / TEST")

print(
    "Training samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)


# -------------------------
# RANDOM FOREST
# -------------------------

model = RandomForestClassifier(

    n_estimators=200,

    random_state=42,

    class_weight="balanced",

    max_depth=8
)


model.fit(
    X_train,
    y_train
)


# -------------------------
# EVALUATION
# -------------------------

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\nMODEL RESULTS")

print(
    f"Accuracy: {accuracy:.2%}"
)


print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "LOSS",
            "PROFIT"
        ]
    )
)


# -------------------------
# FEATURE IMPORTANCE
# -------------------------

print(
    "\nFEATURE IMPORTANCE"
)


importance = pd.Series(

    model.feature_importances_,

    index=feature_columns

).sort_values(
    ascending=False
)


print(importance)


# -------------------------
# SAVE MODEL
# -------------------------

import joblib

joblib.dump(
    model,
    "stock_model.pkl"
)


print(
    "\nModel saved as stock_model.pkl"
)