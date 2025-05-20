from tiingo import TiingoClient
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# Set up Tiingo API key
config = {
    'session': True,
    'api_key': "272e1e82e3f41dcfd3a096fbd5939a024a02ff98"  # Replace with your own API key
}
client = TiingoClient(config)

# Download daily GLD (Gold ETF) data
symbol = "GLD"
df = client.get_dataframe(
    symbol,
    frequency='daily',
    startDate='2024-05-01',
    endDate='2024-05-17'
)

df = df.dropna()

# Calculate indicators
df["EMA9"] = EMAIndicator(close=df["close"], window=9).ema_indicator()
df["EMA21"] = EMAIndicator(close=df["close"], window=21).ema_indicator()
df["RSI"] = RSIIndicator(close=df["close"], window=14).rsi()

# Generate buy/sell signals
df["Signal"] = 0
df.loc[(df["EMA9"] > df["EMA21"]) & (df["RSI"] > 50), "Signal"] = 1
df.loc[(df["EMA9"] < df["EMA21"]) & (df["RSI"] < 50), "Signal"] = -1

# Initialize backtest variables
balance = 100
position = None
entry_price = 0
risk_per_trade = 10
reward_ratio = 2
equity_curve = []

# Backtest loop
for i in range(1, len(df)):
    signal = df["Signal"].iloc[i]
    price = df["close"].iloc[i]

    if position is None:
        if signal == 1:
            position = "long"
            entry_price = price
            stop_loss = entry_price - (risk_per_trade / (balance / 100))
            take_profit = entry_price + reward_ratio * (entry_price - stop_loss)
        elif signal == -1:
            position = "short"
            entry_price = price
            stop_loss = entry_price + (risk_per_trade / (balance / 100))
            take_profit = entry_price - reward_ratio * (stop_loss - entry_price)
    else:
        if position == "long":
            if price <= stop_loss:
                balance -= risk_per_trade
                # print(f"Exit LONG at {price:.2f}, Stop Loss hit. Balance: R{balance:.2f}")
                position = None
            elif price >= take_profit:
                balance += risk_per_trade * reward_ratio
                # print(f"Exit LONG at {price:.2f}, Take Profit hit. Balance: R{balance:.2f}")
                position = None
        elif position == "short":
            if price >= stop_loss:
                balance -= risk_per_trade
                # print(f"Exit SHORT at {price:.2f}, Stop Loss hit. Balance: R{balance:.2f}")
                position = None
            elif price <= take_profit:
                balance += risk_per_trade * reward_ratio
                # print(f"Exit SHORT at {price:.2f}, Take Profit hit. Balance: R{balance:.2f}")
                position = None

    equity_curve.append(balance)

# Plotting equity curve with dates
plt.figure(figsize=(10, 5))
plt.plot(df.index[1:], equity_curve, label="Equity Curve", color='gold')
plt.title("Backtest: GLD EMA + RSI Strategy")
plt.xlabel("Date")
plt.ylabel("Balance (R)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Final Balance: R{balance:.2f}")
