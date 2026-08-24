import pandas as pd
import numpy as np


STOCKS = [
    "RELIANCE",
    "TCS",
    "INFY",
    "SBIN",
    "ITC",
    "TATASTEEL",
    "AXISBANK",
    "HDFCBANK"
]


def generate_market_data():

    data = []

    timestamps = pd.date_range(
        "2026-08-07 10:00:00",
        periods=150,
        freq="min"
    )

    for stock in STOCKS:

        price = np.random.uniform(100, 300)

        for timestamp in timestamps:

            price += np.random.normal(0, 1.2)

            price = max(price, 30)

            data.append({

                "timestamp": timestamp,
                "stock": stock,
                "ltp": price,

                "bid_qty": np.random.randint(
                    500000,
                    2000000
                ),

                "ask_qty": np.random.randint(
                    500000,
                    2000000
                ),

                "ltq": np.random.randint(
                    100,
                    2000
                ),

                "etq_5": np.random.randint(
                    50000,
                    500000
                ),

                "etq_20": np.random.randint(
                    200000,
                    1500000
                ),

                "etq_60": np.random.randint(
                    500000,
                    4000000
                )
            })

    return pd.DataFrame(data)


if __name__ == "__main__":

    df = generate_market_data()

    print(df.head())

    print("\nTotal rows:", len(df))

    print("\nStocks:")
    print(df["stock"].unique())