import pandas as pd


def create_features(df):

    df = df.copy()

    df["smma_gap"] = (
        df["smma20"]
        -
        df["smma120"]
    )

    df["price_change"] = (
        df.groupby("stock")["ltp"]
        .pct_change()
    )

    df["ltq_avg_2"] = (
        df.groupby("stock")["ltq"]
        .transform(
            lambda x:
            x.rolling(2).mean()
        )
    )

    df["ltq_avg_5"] = (
        df.groupby("stock")["ltq"]
        .transform(
            lambda x:
            x.rolling(5).mean()
        )
    )

    df["ltq_ratio"] = (
        df["ltq_avg_2"]
        /
        df["ltq_avg_5"]
    )

    df["market_type"] = "sideways"

    df.loc[
        df["smma_gap"] > 1,
        "market_type"
    ] = "bull"

    df.loc[
        df["smma_gap"] < -1,
        "market_type"
    ] = "bear"

    df["direction"] = "NONE"

    df.loc[
        df["buy_signal"],
        "direction"
    ] = "BUY"

    df.loc[
        df["sell_signal"],
        "direction"
    ] = "SELL"

    return df