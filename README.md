# Dynamic-Lookback---Momentum-Trading-Strategy-BTC
I coded and backtested the dynamic lookback formula (STRATEGY.py) to measure momentum on BTC, from this article (The article applied this on SPY) : https://seekingalpha.com/article/4043600-testing-a-dynamic-lookback-period-in-a-simple-momentum-trading-model , I chose as arbitrary lookback 720 hours or 30 days (On the article is 100-day arbitrary lookback to start and apply the dynamic lookback formula) , I used hourly data.
This is the part of the article that describes this formula:
a dynamic lookback is used which is based on the 100-day volatility of SPY, which we'll call σ (σ is the standard deviation of the last 100 days of daily returns; 100 days was chosen arbitrarily). A volatility factor "VF" is then calculated by dividing the current σ by the 100-day simple average of σ. The lookback period is then VF times 252. If the current σ is 75% of the 100-day SMA of σ, then the lookback would be 75% * 252, or 189 days.
Dynamic Lookback Formula: 
![8f447ba0-3547-4992-8884-fe8f581c1095](https://github.com/user-attachments/assets/6301c9a1-0854-4ea0-8de0-78722e9a8fc6)
Results from 2020-07-02 until 2025-06-02 (1456% Compounded Returns or 15x, -53 Drawdown....) 
![DYNAMIC LOOKBACK BT NO FEES NO SLIPPAGE HOURLY BT ](https://github.com/user-attachments/assets/ff0c5bce-069c-4bf4-ae4c-b2a5ba463f59)


