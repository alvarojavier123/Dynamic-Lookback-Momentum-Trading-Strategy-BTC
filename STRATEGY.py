import pandas as pd
pd.set_option("display.max_rows", None)
import numpy as np
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
init()


df = pd.read_csv("aggTrades_aggregated_1h.csv", parse_dates=['timestamp'])
df = df.dropna()
df = df.drop("buy_volume", axis=1)
df = df.drop("sell_volume", axis=1)
df = df.drop("volume_diff", axis=1)
df = df.drop("total_volume", axis=1)
df = df.drop("aggressor", axis=1)
df.set_index('timestamp', inplace=True)

vol_window = 720    # 720 HOURS ARBITRARY LOOKBACK TO START
base_lookback = 720   


# Compute hourly returns
df['return'] = df['price'].pct_change()

# Compute rolling volatility (σ) over 2400 hours
df['volatility'] = df['return'].rolling(window=vol_window).std()

# Compute rolling average volatility (SMA of σ)
df['avg_volatility'] = df['volatility'].rolling(window=vol_window).mean()

# Compute volatility factor VF = σ / avg(σ)
df['VF'] = df['volatility'] / df['avg_volatility']

# Compute dynamic lookback: VF * base_lookback, capped at max_lookback
df['dyn_lookback'] = (df['VF'] * base_lookback)

df['signal'] = 0

for i in range(0,len(df)):
    print(i)
    date = df.index[i]
    print("Date = ", date)

    price_now = df['price'].iloc[i]
    std = df['volatility'].iloc[i]
    mean = df['avg_volatility'].iloc[i]
    VF = df['VF'].iloc[i]
    dynamic_lookback = df['dyn_lookback'].iloc[i]


    if not np.isnan(dynamic_lookback):
        print("Dynamic Lookback = ", dynamic_lookback)
        print("Price Now = ", price_now)
        price_then = df['price'].iloc[i - int(dynamic_lookback)]
        print("Price Then = ", price_then)
        print("Date At Lookback Period = ", df.iloc[i - int(dynamic_lookback)].name)
        direction = price_now - price_then
        print("Direction = ", direction)
        if direction > 0 :
            df.at[date, 'signal'] = 1

        if direction < 0 :
            df.at[date, 'signal'] = -1


df['strategy_return'] = df['signal'].shift(1) * df['return']
df['cum_return'] = (1 + df['strategy_return']).cumprod()

df.dropna(subset=['strategy_return'], inplace=True)

# Cumulative return
cum_returns = (1 + df['strategy_return']).cumprod()

# Metrics
sharpe = df['strategy_return'].mean() / df['strategy_return'].std() * np.sqrt(365*24)
rolling_max = cum_returns.cummax()
drawdown = cum_returns / rolling_max - 1
max_dd = drawdown.min()


print(Fore.CYAN + f"Sharpe Ratio: {sharpe:.2f}")
print(f"Cumulative Return (final): {cum_returns.iloc[-1] - 1:.2%} ({cum_returns.iloc[-1]:.2f}x)")
print(f"Max Drawdown: {max_dd:.2%}" + Style.RESET_ALL)

# Plot
plt.figure(figsize=(15, 6))
cum_returns.plot(title='Cumulative Return Without TP/SL')
plt.xlabel('Time')
plt.ylabel('Cumulative Return')
plt.grid(True)
plt.tight_layout()
plt.show()

