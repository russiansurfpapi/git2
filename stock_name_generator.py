import openai
import argparse
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env.local file
load_dotenv(".env.local")

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY1")

# Check if the API key is set correctly
if not api_key:
    sys.exit(
        "Error: OpenAI API key is missing or not set correctly. Please update the API key in the .env.local file."
    )

# Set OpenAI API key
openai.api_key = api_key

client = OpenAI(api_key=api_key)

# Command-line argument parser
parser = argparse.ArgumentParser(
    description="Find stock ticker for a given company name."
)
parser.add_argument("company_name", type=str, help="Name of the company")
args = parser.parse_args()


# Function to retrieve stock ticker symbol
def get_stock_ticker(company_name):
    prompt = (
        f"Provide the stock ticker symbol for the publicly traded company named '{company_name}'. "
        f"Respond only with the stock ticker symbol and nothing else."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial assistant that provides stock ticker symbols.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Extract the stock ticker from the response
        ticker_symbol = response.choices[0].message.content.strip()
        return ticker_symbol

    except Exception as e:
        print(f"Error retrieving stock ticker for {company_name}: {e}")
        return None


# Get the stock ticker for the provided company name
stock_ticker = get_stock_ticker(args.company_name)

# Print the result
if stock_ticker:
    print(f"Stock ticker for '{args.company_name}': {stock_ticker}")
else:
    print(f"Could not retrieve stock ticker for '{args.company_name}'.")
