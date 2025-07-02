# AI Stock Trading Agents

This project demonstrates a simple multi-agent system for analyzing stock data and generating trading recommendations using the Google Gemini API, `yfinance` for stock data retrieval, and `pandas` for data manipulation.

## Features

* **Data Retrieval:** Fetches historical stock data using `yfinance`.
* **Bull and Bear Agents:** Two specialized agents (`BullMarketAgent` and `BearMarketAgent`) analyze the stock data from bullish and bearish perspectives, respectively, and generate concise summaries using the Google Gemini API.
* **Manager Agent:** A `ManagerAgent` consolidates the reports from the bull and bear agents, along with recent news (summarized by Gemini), and provides a final buy, hold, or sell recommendation.
* **Google Gemini Integration:** Leverages the Gemini API for natural language understanding and generation, providing insightful summaries and recommendations.

## How it Works

The system operates in the following steps:

1.  **Data Fetching:** The `get_stock_data` function retrieves the past week's daily stock data for a given ticker. Recent news about the stock is also fetched and summarized using the Gemini API.
2.  **Agent Analysis:**
    * The **`BearMarketAgent`** analyzes the stock data for potential bearish indicators (e.g., price drops, high volume on down days).
    * The **`BullMarketAgent`** analyzes the stock data for potential bullish indicators (e.g., price increases, high volume on up days).
    * Both agents use the `get_gemini_summary` function to generate human-readable summaries of their findings from their respective perspectives.
3.  **Manager Decision:** The **`ManagerAgent`** takes the summaries from both the bull and bear agents, along with the news summary, and uses the `get_gemini_manager_summary` function to synthesize this information into a final trading recommendation (buy, hold, or sell) for the next 90 days.

## Setup and Installation

### Prerequisites

* Python 3.7+
* Google Gemini API Key

### Installation

1.  **Clone the repository (or copy the code):**
    ```bash
    git clone https://github.com/zachdwight/stock-trading-agents-yfinance-gemini.git
    cd stock-trading-agents-yfinance-gemini
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    (Create a `requirements.txt` file with the following content if you don't have one):
    ```
    yfinance
    pandas
    google-generativeai
    ```

3.  **Configure your Google Gemini API Key:**

    **IMPORTANT:** For production environments, it is highly recommended to set your API key as an environment variable (e.g., `GOOGLE_API_KEY`).

    ```bash
    export GOOGLE_API_KEY='YOUR_GEMINI_API_KEY'
    ```

    Alternatively, for demonstration purposes, you can temporarily hardcode your API key directly in the `main.py` (or your script's name) file, but **remember to remove it before pushing to a public repository**:

    ```python
    API_KEY = "YOUR_GEMINI_API_KEY" # <--- REPLACE THIS WITH YOUR ACTUAL API KEY
    genai.configure(api_key=API_KEY)
    ```

## Usage

To run the trading agents, simply execute the Python script. You can change the `stock_symbol` variable in the `if __name__ == "__main__":` block to analyze a different stock.

```bash
python trading_agents.py
```

## Sample Output (AAPL)

Note, I did change the yfinance stock query: 
```python
    # 1. Fetch data for the past week
    stock_data = get_stock_data(ticker, period="1mo", interval="1d")
```bash

```bash
--- Running Trading Agents for AAPL ---
Ticker: AAPL news: Apple's recent iPhone sales figures slightly missed analyst expectations, raising concerns about weakening consumer demand in key markets.  This slowdown, coupled with increased production costs, could impact Apple's profitability in the coming quarters.  Supply chain disruptions in China continue to pose a significant risk to Apple's manufacturing and product availability.  The strong US dollar negatively affects international sales, further dampening revenue growth.  However, Apple's services division continues to show strong growth, offering a buffer against declining hardware sales.  Increased investment in artificial intelligence and augmented reality technologies signal long-term growth potential but require significant upfront capital expenditure.  Potential regulatory scrutiny over App Store practices could lead to significant financial penalties and market share losses.  Overall, the mixed signals create uncertainty about Apple's short-term stock performance, though its long-term prospects remain largely positive due to its robust ecosystem and brand loyalty.


--- Past Week's Stock Data (Last 5 entries) ---
                                 Open        High         Low       Close    Volume  Dividends  Stock Splits
Date                                                                                                        
2025-06-26 00:00:00-04:00  201.429993  202.639999  199.460007  201.000000  50799100        0.0           0.0
2025-06-27 00:00:00-04:00  201.889999  203.220001  200.000000  201.080002  73188600        0.0           0.0
2025-06-30 00:00:00-04:00  202.009995  207.389999  199.259995  205.169998  91912800        0.0           0.0
2025-07-01 00:00:00-04:00  206.669998  210.190002  206.139999  207.820007  78673300        0.0           0.0
2025-07-02 00:00:00-04:00  209.080002  213.339996  208.139999  212.059998  30544805        0.0           0.0

Bear Market Agent Report: To: Portfolio Manager

From: [Your Name/Team Name]

Subject: Stock Recommendation: [Stock Name] - Sell

**Summary:** Despite a recent upward swing, the provided data reveals a bearish trend for [Stock Name] over the past month.  Prices have fluctuated wildly, showing volatility, and the closing price is still lower than the initial highs observed within the period.  Increased volume during periods of decline signals selling pressure exceeding buying interest.

**Recommendation:** Sell [Stock Name] within the next 90 days.  The recent price increase may represent a temporary "dead-cat bounce," a short-lived rally in a downtrend, rather than a sustained recovery.  Continued volatility and the overall downward trajectory suggest further price depreciation is likely over the next three months.  This decision minimizes potential losses.

Bull Market Agent Report: To: Manager
From: [Your Name]
Date: July 2, 2025
Subject: Stock Recommendation - Next 90 Days

**Summary:** The stock exhibits strong bullish momentum. Over the past three weeks, it has demonstrated a consistent upward trend, overcoming temporary dips with increasing volume. The recent close at 212.06 represents a significant gain from the recent low of 195.07 and a robust close above the opening price of the week. This suggests strong buying pressure and a positive outlook.


**Recommendation:** Buy.  Given the current trajectory and positive market indicators within this short timeframe, I recommend initiating a buy position. The stock's recent performance and overall trend strongly suggest further gains within the next 90 days.  We should monitor the stock closely for any indications of a significant pullback, but at present the risk-reward ratio favors a bullish strategy.


Manager Agent is evaluating reports:
  - Bear Report: To: Portfolio Manager

From: [Your Name/Team Name]

Subject: Stock Recommendation: [Stock Name] - Sell

**Summary:** Despite a recent upward swing, the provided data reveals a bearish trend for [Stock Name] over the past month.  Prices have fluctuated wildly, showing volatility, and the closing price is still lower than the initial highs observed within the period.  Increased volume during periods of decline signals selling pressure exceeding buying interest.

**Recommendation:** Sell [Stock Name] within the next 90 days.  The recent price increase may represent a temporary "dead-cat bounce," a short-lived rally in a downtrend, rather than a sustained recovery.  Continued volatility and the overall downward trajectory suggest further price depreciation is likely over the next three months.  This decision minimizes potential losses.

  - Bull Report: To: Manager
From: [Your Name]
Date: July 2, 2025
Subject: Stock Recommendation - Next 90 Days

**Summary:** The stock exhibits strong bullish momentum. Over the past three weeks, it has demonstrated a consistent upward trend, overcoming temporary dips with increasing volume. The recent close at 212.06 represents a significant gain from the recent low of 195.07 and a robust close above the opening price of the week. This suggests strong buying pressure and a positive outlook.


**Recommendation:** Buy.  Given the current trajectory and positive market indicators within this short timeframe, I recommend initiating a buy position. The stock's recent performance and overall trend strongly suggest further gains within the next 90 days.  We should monitor the stock closely for any indications of a significant pullback, but at present the risk-reward ratio favors a bullish strategy.


Manager Agent's Final Decision: ## AAPL Stock Recommendation: Hold (Next 90 Days)

The conflicting analyst reports and recent news regarding AAPL present a complex picture, making a definitive buy or sell recommendation challenging within the next 90-day timeframe.  Therefore, a **hold** strategy is recommended.

**Reasons for not buying:**

* **Mixed Signals:** While one analyst highlights a short-term bullish trend, the other points to underlying bearish indicators and the possibility of a "dead-cat bounce". The recent news supports this cautious view.  Missed sales expectations, production cost increases, supply chain issues, currency headwinds, and regulatory risks all contribute to a less optimistic outlook than the purely bullish assessment suggests.
* **Short-Term Uncertainty:** The news clearly indicates significant uncertainty regarding AAPL's performance in the short-term. While the services division is strong, the weaknesses in hardware sales could outweigh this positive factor in the next 90 days.  Focusing on the immediate future, the risks outweigh the potential rewards for a buy recommendation.

**Reasons for not selling:**

* **Long-Term Potential:**  The news also points to significant long-term potential in AI and AR investments, as well as the continued strength of the services segment.  A sell decision at this point risks missing out on any potential rebound driven by these positive factors should the short-term headwinds abate.
* **Potential for a "Dead-Cat Bounce" Reversal:** The bearish analysis mentions the possibility that the recent upward swing is a temporary rally, meaning that a sell decision now might be premature.  It's possible that the positive momentum could continue, leading to gains.


**Hold Strategy Justification:**

The "hold" recommendation allows us to observe the market's reaction to the recent news and the unfolding of these competing short-term and long-term factors.  Monitoring the stock closely over the next 90 days, paying particular attention to:

* **Consumer demand:** Any further signs of weakening or strengthening in key markets.
* **Supply chain disruptions:** Resolution or worsening of these issues.
* **Regulatory outcomes:**  The impact of any potential penalties.
* **The performance of the services division:**  Whether its continued growth can offset challenges in the hardware sector.

Will provide a more informed buy or sell decision based on this ongoing assessment.  Regular review of these factors, alongside more detailed technical and fundamental analysis, is crucial before a future recommendation can be made.

--- End of Trading Agent Run ---
```
