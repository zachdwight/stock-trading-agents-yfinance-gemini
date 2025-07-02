import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


# --- Google Gemini API Integration ---
import google.generativeai as genai

# Configure the API key
# IMPORTANT: Replace 'YOUR_GEMINI_API_KEY' with your actual API key,
# or even better, set it as an environment variable (e.g., GOOGLE_API_KEY)
# and load it like this:
# API_KEY = os.getenv("GOOGLE_API_KEY")
# if not API_KEY:
#    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set your Gemini API key.")

# For demonstration, you can temporarily put your key here, but REMOVE IT FOR PRODUCTION.
API_KEY = "XXXXXX" # <--- REPLACE THIS WITH YOUR ACTUAL API KEY



genai.configure(api_key=API_KEY)

# Function to call Google Gemini API
def get_gemini_summary(portfolio_data_string: str, sentiment: str) -> str:

    try:

        model = genai.GenerativeModel('gemini-1.5-flash')

        # Craft the prompt for the LLM
        prompt = (
            f"Analyze the following stock data and provide a concise summary like a {sentiment} trader "
            "of its overall health and provide a recommendation to buy, hold, or sell the stock to your manager."
            "Provide this recommendation in context of the next 90 days. \n\n"
            f"Current view:\n{portfolio_data_string}\n\n"
            "Justification/Summary:"
        )

      
        response = model.generate_content(prompt)

        # Check if the response has text content
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            print(f"      Warning: Gemini API returned an empty or malformed response. Debug info: {response}")
            return "Could not generate summary from Gemini API (empty response)."

    except Exception as e:
        print(f"      Error calling Google Gemini API: {type(e).__name__} - {e}")
        return "Could not get summary from Google Gemini API due to an error."

def get_gemini_manager_summary(bull: str, bear: str, news: str) -> str:

    try:

        model = genai.GenerativeModel('gemini-1.5-flash')

        # Craft the prompt for the LLM
        prompt = (
            "Analyze the following stock outlooks from your workers.  You are their manager. "
            "Provide a final buy, hold, or sell recommendation based on their reports."
            "Provide this recommendation in context of the next 90 days. \n\n"
            f"Bullish Opinion:\n{bull}\n\n"
            f"Bearish Opinion:\n{bear}\n\n"
            f"Recent News:\n{news}\n\n"
            
        )


        response = model.generate_content(prompt)

        # Check if the response has text content
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            print(f"      Warning: Gemini API returned an empty or malformed response. Debug info: {response}")
            return "Could not generate summary from Gemini API (empty response)."

    except Exception as e:
        print(f"      Error calling Google Gemini API: {type(e).__name__} - {e}")
        return "Could not get summary from Google Gemini API due to an error."

def get_gemini_news_summary(stock: str) -> str:
    try:

        model = genai.GenerativeModel('gemini-1.5-flash')

        # Craft the prompt for the LLM
        prompt = (
            f"Please provide 8 sentence summary of stock {stock} news that may impact economic outlook of company and stock price."
        )

        response = model.generate_content(prompt)

        # Check if the response has text content
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return f"Ticker: {stock} news: " + response.candidates[0].content.parts[0].text
        else:
            print(f"      Warning: Gemini API returned an empty or malformed response. Debug info: {response}")
            return "Could not generate summary from Gemini API (empty response)."

    except Exception as e:
        print(f"      Error calling Google Gemini API: {type(e).__name__} - {e}")
        return "Could not get summary from Google Gemini API due to an error."


# --- 1. Data Retrieval Function ---
def get_stock_data(ticker, period="1wk", interval="1d"):
    """
    Fetches historical stock data for a given ticker.
    period: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    interval: "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
    Note: Yahoo Finance does not support minute-level data for periods longer than 7 days.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# --- 2. Agent Classes ---

class StockAgent:
    def __init__(self, name):
        self.name = name

    def analyze(self, stock_data):
        raise NotImplementedError("Subclasses must implement this method")

class BearMarketAgent(StockAgent):
    def __init__(self):
        super().__init__("Bear Market Agent")

    def analyze(self, stock_data):
        if stock_data.empty:
            return "No data to analyze."

        # Simple bear market indicators
        last_close = stock_data['Close'].iloc[-1]
        first_close = stock_data['Close'].iloc[0]
        max_high = stock_data['High'].max()
        min_low = stock_data['Low'].min()

        bearish_reasons = []
        bearish_reasons.append(stock_data)

        if last_close < first_close:
            bearish_reasons.append(f"Stock closed lower than the beginning of the week ({last_close:.2f} vs {first_close:.2f}).")
        if (max_high - last_close) / last_close > 0.05: # Significant drop from weekly high
            bearish_reasons.append(f"Significant drop from weekly high ({max_high:.2f}) to current close ({last_close:.2f}).")
        if stock_data['Volume'].iloc[-1] > stock_data['Volume'].mean() * 1.5 and last_close < stock_data['Close'].iloc[-2]:
            bearish_reasons.append("High volume on a down day, indicating strong selling pressure.")
        return get_gemini_summary(bearish_reasons,"bearish")


class BullMarketAgent(StockAgent):
    def __init__(self):
        super().__init__("Bull Market Agent")

    def analyze(self, stock_data):
        if stock_data.empty:
            return "No data to analyze."

        # Simple bull market indicators
        last_close = stock_data['Close'].iloc[-1]
        first_close = stock_data['Close'].iloc[0]
        min_low = stock_data['Low'].min()
        max_high = stock_data['High'].max()

        bullish_reasons = []
        bullish_reasons.append(stock_data)

        if last_close > first_close:
            bullish_reasons.append(f"Stock closed higher than the beginning of the week ({last_close:.2f} vs {first_close:.2f}).")
        if (last_close - min_low) / min_low > 0.05: # Significant rise from weekly low
            bullish_reasons.append(f"Significant rise from weekly low ({min_low:.2f}) to current close ({last_close:.2f}).")
        if stock_data['Volume'].iloc[-1] > stock_data['Volume'].mean() * 1.5 and last_close > stock_data['Close'].iloc[-2]:
            bullish_reasons.append("High volume on an up day, indicating strong buying interest.")
        return get_gemini_summary(bullish_reasons,"bullish")

class ManagerAgent(StockAgent):
    def __init__(self):
        super().__init__("Manager Agent")

    def decide(self, bear_report, bull_report, news_report):
        print(f"\n{self.name} is evaluating reports:")
        print(f"  - Bear Report: {bear_report}")
        print(f"  - Bull Report: {bull_report}")

        decision = "HOLD" # Default to hold

        decision = get_gemini_manager_summary(bull_report, bear_report, news_report)

        return decision

# --- 3. Orchestration ---

def run_trading_agents(ticker):
    print(f"--- Running Trading Agents for {ticker} ---")

    # 1. Fetch data for the past week (this is very small window so adjust for 'better' view of stock
    stock_data = get_stock_data(ticker, period="1wk", interval="1d")
    stock_news = get_gemini_news_summary(ticker)
    print(stock_news)
    if stock_data is None or stock_data.empty:
        print(f"Could not retrieve data for {ticker}. Exiting.")
        return

    print("\n--- Past Week's Stock Data (Last 5 entries) ---")
    print(stock_data.tail())

    # 2. Initialize agents
    bear_agent = BearMarketAgent()
    bull_agent = BullMarketAgent()
    manager_agent = ManagerAgent()

    # 3. Agents analyze data
    bear_report = bear_agent.analyze(stock_data)
    bull_report = bull_agent.analyze(stock_data)

    print(f"\n{bear_agent.name} Report: {bear_report}")
    print(f"{bull_agent.name} Report: {bull_report}")

    # 4. Manager makes a decision
    final_decision = manager_agent.decide(bear_report, bull_report, stock_news)

    print(f"\n{manager_agent.name}'s Final Decision: {final_decision}")
    print("--- End of Trading Agent Run ---")

# --- Example Usage ---
if __name__ == "__main__":
    # You can change the ticker symbol here
    stock_symbol = "CNC" 
    # stock_symbol = "AAPL" # Apple
    # stock_symbol = "GOOGL" # Google

    run_trading_agents(stock_symbol)
