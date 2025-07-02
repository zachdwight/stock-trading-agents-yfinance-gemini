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
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
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
python your_script_name.py
