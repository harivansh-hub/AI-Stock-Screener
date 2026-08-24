
import numpy as np
import pandas as pd


def generate_market_data():

    np.random.seed()

    # 1000 minutes of market data
    n = 1000

    timestamps = pd.date_range(
        start="2026-08-07 09:15:00",
        periods=n,
        freq="min"
    )

    prices = [100.0]
    ltq_values = []

    # Different market regimes
    regime_length = 100

    regimes = [
        "bull",
        "bear",
        "sideways",
        "bull",
        "bear",
        "sideways",
        "bull",
        "bear",
        "bull"
    ]

    for i in range(1, n):

        regime_index = i // regime_length

        if regime_index >= len(regimes):
            regime_index = len(regimes) - 1

        market_type = regimes[regime_index]

        previous_price = prices[-1]

        # ---------------------------------
        # Market behaviour
        # ---------------------------------

        if market_type == "bull":

            drift = 0.12
            volatility = 0.35

        elif market_type == "bear":

            drift = -0.12
            volatility = 0.35

        else:

            drift = 0
            volatility = 0.45


        movement = (
            drift
            + np.random.normal(0, volatility)
        )

        new_price = previous_price + movement

        # Keep price positive
        new_price = max(new_price, 30)

        prices.append(new_price)


        # ---------------------------------
        # LTQ
        # ---------------------------------

        base_ltq = np.random.randint(
            500,
            2500
        )

        # Occasionally create LTQ spikes
        if np.random.random() < 0.15:

            base_ltq *= np.random.randint(
                2,
                5
            )

        ltq_values.append(base_ltq)


    # First LTQ value
    ltq_values.insert(
        0,
        np.random.randint(500, 2500)
    )


    # Determine market type for every row

    market_types = []

    for i in range(n):

        regime_index = i // regime_length

        if regime_index >= len(regimes):
            regime_index = len(regimes) - 1

        market_types.append(
            regimes[regime_index]
        )


    df = pd.DataFrame({

        "timestamp": timestamps,

        "ltp": prices,

        "ltq": ltq_values,

        "market_type": market_types

    })


    return df


# Test generator
if __name__ == "__main__":

    df = generate_market_data()

    print(df.head())

    print("\nMarket distribution:")

    print(
        df["market_type"].value_counts()
    )
