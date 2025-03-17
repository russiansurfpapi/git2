import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys from .env.local
load_dotenv(".env.local")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY1")
FMP_API_KEY = os.getenv("FMP_API_KEY")

if not OPENAI_API_KEY:
    sys.exit("❌ Error: OpenAI API key is missing. Please update .env.local.")

if not FMP_API_KEY:
    sys.exit("❌ Error: FMP API key is missing. Please update .env.local.")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# API Endpoints
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3/earning_call_transcript"


def get_stock_ticker(company_name):
    """Retrieve the stock ticker symbol using OpenAI."""
    prompt = (
        f"Provide the stock ticker symbol for the publicly traded company named '{company_name}'. "
        f"Respond only with the stock ticker symbol and nothing else."
    )

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial assistant that provides stock ticker symbols.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=10,
        )

        ticker_symbol = response.choices[0].message.content.strip().upper()
        return ticker_symbol

    except Exception as e:
        print(f"❌ Error retrieving stock ticker for {company_name}: {e}")
        return None


def get_latest_earnings_call(ticker):
    """Fetches the most recent earnings call transcript."""
    file_path = f"./{ticker}_latest_earnings.txt"

    print(f"📥 Fetching the most recent earnings call for {ticker}...")

    response = requests.get(f"{FMP_BASE_URL}/{ticker}?apikey={FMP_API_KEY}")

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            with open(file_path, "w", encoding="utf-8") as f:
                for entry in data:
                    f.write(f"Date: {entry.get('date', 'Unknown')}\n\n")
                    f.write(
                        f"Transcript:\n{entry.get('content', 'No transcript available')}\n"
                    )
                    f.write("=" * 80 + "\n")  # Separator for readability
            print(f"✅ Saved: {file_path}")
        else:
            print(f"❌ No transcript available.")
    else:
        print(f"❌ API Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 batch_fmp_earnings.py <company1, company2, company3,...>")
        sys.exit(1)

    company_list = sys.argv[1].split(",")

    for company_name in company_list:
        company_name = company_name.strip()

        print(f"🔍 Retrieving stock ticker for '{company_name}'...")
        ticker = get_stock_ticker(company_name)

        if not ticker:
            print(
                f"❌ Could not determine the stock ticker for '{company_name}'. Skipping..."
            )
            continue

        print(f"✅ Found ticker: {ticker}")

        try:
            get_latest_earnings_call(ticker)
        except Exception as e:
            print(f"❌ Error fetching earnings for {ticker}: {e}")
