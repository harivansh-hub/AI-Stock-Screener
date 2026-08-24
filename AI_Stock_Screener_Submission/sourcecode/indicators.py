import pandas as pd


def calculate_smma(series, period):

    smma = []

    for i, price in enumerate(series):

        if i == 0:

            smma.append(price)

        else:

            previous = smma[-1]

            value = (
                previous * (period - 1)
                + price
            ) / period

            smma.append(value)

    return smma


def add_indicators(df):

    df = df.copy()

    df = df.sort_values(
        ["stock", "timestamp"]
    )

    df["smma20"] = (
        df.groupby("stock")["ltp"]
        .transform(
            lambda x:
            calculate_smma(x, 20)
        )
    )

    df["smma120"] = (
        df.groupby("stock")["ltp"]
        .transform(
            lambda x:
            calculate_smma(x, 120)
        )
    )

    df["smma20_previous"] = (
        df.groupby("stock")["smma20"]
        .shift(1)
    )

    df["smma120_previous"] = (
        df.groupby("stock")["smma120"]
        .shift(1)
    )

    df["buy_signal"] = (
        (df["smma20"] > df["smma120"])
        &
        (
            df["smma20_previous"]
            <=
            df["smma120_previous"]
        )
    )

    df["sell_signal"] = (
        (df["smma20"] < df["smma120"])
        &
        (
            df["smma20_previous"]
            >=
            df["smma120_previous"]
        )
    )

    return df


if __name__ == "__main__":

    from market_data import generate_market_data

    df = generate_market_data()

    df = add_indicators(df)

    print(
        df[
            [
                "timestamp",
                "stock",
                "ltp",
                "smma20",
                "smma120",
                "buy_signal",
                "sell_signal"
            ]
        ].tail(20).to_string(index=False)
    )