import argparse
import time
from semantic_search import generate_related_searches  # Import your existing function


# Function to escape special characters for JavaScript
def escape_js_string(js_string):
    return js_string.replace("'", "\\'").replace('"', '\\"')


# Function to generate the JavaScript code
def generate_js_code(search_term):
    # Generate the related searches using your existing function
    related_searches = generate_related_searches(search_term)

    if not related_searches:
        return "Error: No related searches generated."

    # Format the searches as JavaScript array and escape any special characters
    questions_js_array = [
        f'"{escape_js_string(search)}"' for search in related_searches
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


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate JavaScript for search queries."
    )
    parser.add_argument(
        "search_term",
        type=str,
        help="The search term to generate related search queries.",
    )
    args = parser.parse_args()

    # Generate and print the JavaScript code
    js_code = generate_js_code(args.search_term)
    print("Generated JavaScript Code:")
    print(js_code)
