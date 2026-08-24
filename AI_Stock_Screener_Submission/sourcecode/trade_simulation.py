import pandas as pd
import numpy as np


# Create fake stock prices
prices = [
    100,101,102,103,104,
    105,106,107,108,109,
    110,109,108,107,106,
    105,104,103,102,101,
    100
]


df = pd.DataFrame({
    "ltp": prices
})


print(df)

def calculate_smma(series, period):

    smma = series.copy()

    smma.iloc[:period-1] = np.nan

    smma.iloc[period-1] = series.iloc[:period].mean()

    for i in range(period, len(series)):
        smma.iloc[i] = (
            (smma.iloc[i-1]*(period-1)+series.iloc[i])
            / period
        )

    return smma
  
df["smma5"] = calculate_smma(df["ltp"],5)
df["smma10"] = calculate_smma(df["ltp"],10)


print(df)

df["buy_signal"] = (
    (df["smma5"] > df["smma10"]) &
    (df["smma5"].shift(1) <= df["smma10"].shift(1))
)


df["sell_signal"] = (
    (df["smma5"] < df["smma10"]) &
    (df["smma5"].shift(1) >= df["smma10"].shift(1))
)


print(df)