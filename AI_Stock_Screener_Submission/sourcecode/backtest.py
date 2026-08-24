import pandas as pd

pd.set_option("display.max_columns", None)

from data_generator import generate_market_data
from indicators import add_indicators
from features import create_features


def run_backtest():

    # ===================================
    # 1. Generate market data
    # ===================================

    df = generate_market_data()

    # Add stock identifier
    # Required because features.py groups data by stock
    if "stock" not in df.columns:
        df["stock"] = "DEMO"


    # ===================================
    # 2. Calculate indicators and signals
    # ===================================

    # This creates:
    # smma20
    # smma120
    # smma20_previous
    # smma120_previous
    # buy_signal
    # sell_signal

    df = add_indicators(df)


    # ===================================
    # 3. Create ML / trading features
    # ===================================

    df = create_features(df)


    # ===================================
    # Optional debugging
    # ===================================

    print("\nDATA COLUMNS:")
    print(df.columns.tolist())

    print("\nFIRST 5 ROWS:")
    print(df.head())


    # ===================================
    # 4. Trade simulation
    # ===================================

    trades = []

    position = None
    entry_price = None
    entry_time = None

    # Store features from entry moment
    entry_features = None


    for i in range(len(df)):

        row = df.iloc[i]


        # ===================================
        # OPEN SELL
        # ===================================

        if row["sell_signal"] and position is None:

            position = "SELL"

            entry_price = row["ltp"]

            entry_time = row["timestamp"]

            entry_features = {

                "smma_gap": row["smma_gap"],

                "ltq_ratio": row["ltq_ratio"],

                "ltq_avg_2": row["ltq_avg_2"],

                "ltq_avg_5": row["ltq_avg_5"],

                "market_type": row["market_type"],

                "price_change": row["price_change"],

                "direction": "SELL"
            }


        # ===================================
        # OPEN BUY
        # ===================================

        elif row["buy_signal"] and position is None:

            position = "BUY"

            entry_price = row["ltp"]

            entry_time = row["timestamp"]

            entry_features = {

                "smma_gap": row["smma_gap"],

                "ltq_ratio": row["ltq_ratio"],

                "ltq_avg_2": row["ltq_avg_2"],

                "ltq_avg_5": row["ltq_avg_5"],

                "market_type": row["market_type"],

                "price_change": row["price_change"],

                "direction": "BUY"
            }


        # ===================================
        # CLOSE SELL
        # ===================================

        elif row["buy_signal"] and position == "SELL":

            exit_price = row["ltp"]

            pnl = entry_price - exit_price


            trade = {

                "type": "SELL",

                "entry_time": entry_time,

                "entry_price": entry_price,

                "exit_time": row["timestamp"],

                "exit_price": exit_price,

                "pnl": pnl,

                "profitable": int(pnl > 0)
            }


            # Add entry-time features
            trade.update(entry_features)

            trades.append(trade)


            position = None

            entry_features = None


        # ===================================
        # CLOSE BUY
        # ===================================

        elif row["sell_signal"] and position == "BUY":

            exit_price = row["ltp"]

            pnl = exit_price - entry_price


            trade = {

                "type": "BUY",

                "entry_time": entry_time,

                "entry_price": entry_price,

                "exit_time": row["timestamp"],

                "exit_price": exit_price,

                "pnl": pnl,

                "profitable": int(pnl > 0)
            }


            # Add entry-time features
            trade.update(entry_features)

            trades.append(trade)


            position = None

            entry_features = None


    # ===================================
    # 5. Create trades dataframe
    # ===================================

    trades_df = pd.DataFrame(trades)

    return trades_df


# =======================================
# Run directly
# =======================================

if __name__ == "__main__":

    trades_df = run_backtest()

    print("\nTRADE RESULTS:\n")


    if trades_df.empty:

        print("No completed trades.")

    else:

        for _, trade in trades_df.iterrows():

            print(

                f"{trade['type']:4} | "

                f"Entry: {trade['entry_price']:.2f} | "

                f"Exit: {trade['exit_price']:.2f} | "

                f"P/L: {trade['pnl']:.2f} | "

                f"SMMA Gap: {trade['smma_gap']:.3f} | "

                f"LTQ Ratio: {trade['ltq_ratio']:.2f} | "

                f"LTQ2: {trade['ltq_avg_2']:.0f} | "

                f"LTQ5: {trade['ltq_avg_5']:.0f} | "

                f"Market: {trade['market_type']} | "

                f"Result: "
                f"{'PROFIT' if trade['profitable'] == 1 else 'LOSS'}"

            )