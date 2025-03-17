import argparse
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.local")

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY1")

if not openai_api_key:
    sys.exit("❌ Error: OpenAI API key is missing. Please update .env.local.")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=openai_api_key)


# Function to escape special characters for JavaScript
def escape_js_string(js_string):
    # Escape both single and double quotes
    return js_string.replace("'", "\\'").replace('"', '\\"')


# Function to generate complete questions using OpenAI
def generate_complete_questions(bullets):
    prompt = f"""
    Take the following bullet points and turn them into clear, complete questions:

    {bullets}

    **Please separate each search query with the number 888* when returning your response. DO NOT USE NEWLINES.**
    """

    try:
        # Making the API call using chat completions with openai_client
        response = openai_client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 for better responses
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates research questions based on input bullet points.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,  # Moderately creative and reliable results
            max_tokens=200,  # Sufficient for detailed responses
        )

        # Print the raw response from OpenAI
        print("API Response:", response.choices[0].message.content)

        # Extract and process the response to split by "888*" and remove excess whitespace
        response_text = response.choices[0].message.content
        questions = [
            question.strip()
            for question in response_text.split("888*")
            if question.strip()
        ]
        return questions

    except Exception as e:
        print(f"❌ Error generating complete questions: {e}")
        return []


# Function to generate the JavaScript code for related search queries
def generate_js_code(questions_list):
    if not questions_list:
        return "Error: No related questions generated."

    # Format the questions as JavaScript array and escape any special characters
    questions_js_array = [
        f'"{escape_js_string(question)}"' for question in questions_list
    ]
    questions_js = ", ".join(questions_js_array)

    # Return the full JavaScript code as a string
    js_code = f"""
(async function() {{
    const questions = [{questions_js}];

    function insertTextAndSubmit(question) {{
        const inputBox = document.querySelector("textarea.query-box-input");
        if (inputBox) {{
            inputBox.value = question;
            inputBox.dispatchEvent(new Event("input", {{ bubbles: true }}));

            setTimeout(() => {{
                const enterEvent = new KeyboardEvent("keydown", {{
                    key: "Enter",
                    code: "Enter",
                    which: 13,
                    keyCode: 13,
                    bubbles: true,
                }});
                inputBox.dispatchEvent(enterEvent);
                console.log(`Submitted: ${{
                    question
                }}`);
            }}, 1000);  // Slight delay before submitting
        }} else {{
            console.error("Input box not found!");
        }}
    }}

    for (let i = 0; i < questions.length; i++) {{
        setTimeout(() => insertTextAndSubmit(questions[i]), i * 30000); // 30 seconds apart
    }}
}})();
    """

    return js_code


# Main block to handle command-line input
if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate JavaScript for search queries based on input bullet points."
    )
    parser.add_argument(
        "bullets", type=str, help="The bullet points to turn into complete questions."
    )
    args = parser.parse_args()

    # Generate the complete questions
    complete_questions = generate_complete_questions(args.bullets)

    if complete_questions:
        # Generate and print the JavaScript code
        js_code = generate_js_code(complete_questions)
        print("Generated JavaScript Code:")
        print(js_code)
    else:
        print("No questions were generated.")
