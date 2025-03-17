import os
import sys
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv(".env.local")

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY1")

if not openai_api_key:
    sys.exit("❌ Error: OpenAI API key is missing. Please update .env.local.")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=openai_api_key)


print("running")


def generate_related_searches(search_term):
    prompt = f"""
    As a research analyst, generate 10 highly relevant and distinct search queries that explore different aspects of the following topic: "{search_term}". 
    The queries should consider multiple angles, including but not limited to:
    - The business model
    - The product or service release cycle
    - The company’s leadership and management structure
    - Competitors and market landscape
    - Financial outlook and funding sources
    - Technological innovation and technical stack
    - Industry trends, including marketing strategies and consumer behavior
    Each query should expand the scope of the original term, exploring different dimensions of the topic.
    **Please separate each search query with the number 888*  when returning your response. DO NOT USE NEWLINES
    """

    try:
        # Making the API call using chat completions with openai_client
        response = openai_client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 for better responses
            messages=[
                {
                    "role": "system",
                    "content": "You are an investment and research analyst.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,  # Moderately creative and reliable results
            max_tokens=200,  # Sufficient for detailed responses
        )

        print(response.choices[0].message.content)
        print("no strip")
        result = response.choices[0].message.content.strip()
        print("yes strip")
        print(result)

        response_text = response.choices[0].message.content
        search_queries = [
            query.strip() for query in response_text.split("888*") if query.strip()
        ]
        print(search_queries)
        # split_items = response_text.split("888*")  # Step 2: Split by "888*"
        # print("\nSplit Items:\n", split_items)
        return search_queries
        # # # Split the response content by '888*'
        # # generated_searches = response_content.split("888*")
        # print(
        #     "      BANANAS               BANANAS               BANANAS               BANANAS               BANANAS               BANANAS               BANANAS               BANANAS               BANANAS               BANANAS               BANANAS         "
        # )

        # # print("Generated Related Searches:")
        # # for search in generated_searches:
        # #     print(f"- {search.strip()}")

        # return "bananas"

    except Exception as e:
        print(f"❌ Error generating related searches: {e}")
        return []


if __name__ == "__main__":
    search_term = "blue orbit vs virgin galactic"  # Example input
    related_searches = generate_related_searches(search_term)
    print(related_searches)  # This will print the related search queries
