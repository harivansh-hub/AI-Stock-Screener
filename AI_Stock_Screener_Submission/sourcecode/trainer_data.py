import pandas as pd

from backtest import run_backtest


ALL_TRADES = []

NUMBER_OF_SIMULATIONS = 500


for simulation in range(NUMBER_OF_SIMULATIONS):

    trades = run_backtest()

    if not trades.empty:
        ALL_TRADES.append(trades)


# Combine everything
if ALL_TRADES:

    training_data = pd.concat(
        ALL_TRADES,
        ignore_index=True
    )

else:

    training_data = pd.DataFrame()


# Remove rows where ML features are missing
training_data = training_data.dropna()


# Save dataset
training_data.to_csv(
    "training_data.csv",
    index=False
)


print("\n================================")
print("TRAINING DATA CREATED")
print("================================")

print(f"Simulations: {NUMBER_OF_SIMULATIONS}")

print(f"Total trades: {len(training_data)}")

print(
    f"Profitable trades: "
    f"{training_data['profitable'].sum()}"
)

print(
    f"Losing trades: "
    f"{(training_data['profitable'] == 0).sum()}"
)

print("\nSaved as:")
print("training_data.csv")