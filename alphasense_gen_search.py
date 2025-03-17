import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# Function to set up the Selenium WebDriver and perform the login
def login(driver):
    URL = "https://research.alpha-sense.com/"
    driver.get(URL)

    # Wait for login page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    print("Login page loaded.")

    # Enter username
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys("sasha@katecapllc.com")
    print("Entered username.")

    # Click continue
    continue_button = driver.find_element(By.ID, "next-step")
    continue_button.click()
    print("Clicked continue.")

    # Wait for password field
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("tvz0bur1twz_GRJ_aeu")
    print("Entered password.")

    # Click submit
    submit_button = driver.find_element(
        By.CSS_SELECTOR, "button[data-testid='loginSubmitButton']"
    )
    submit_button.click()
    print("Clicked submit.")

    # Wait for the dashboard to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror"))
    )
    print("Dashboard loaded.")


# Function to perform the search in "Generative Search"
def search_in_generative_search(driver, search_query):
    # Method: Using XPath based on 'aria-label' attribute to click "Generative Search"
    print("Trying Method: XPath based on aria-label to click 'Generative Search'...")
    generative_search_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Generative Search']"))
    )
    generative_search_button.click()
    print("Clicked 'Generative Search'.")

    # Wait for 3 seconds to let the page load
    time.sleep(3)

    # Locate the search input field (textarea)
    search_textarea = driver.find_element(
        By.CSS_SELECTOR, "textarea[aria-invalid='false']"
    )

    # Enter the search term passed as an argument
    search_textarea.send_keys(search_query)  # Enter the search term
    print(f"Entered search query: {search_query}")

    # Simulate pressing Enter to submit the search
    search_textarea.send_keys("\n")  # Simulating Enter key press
    print("Simulated Enter key press to submit the search.")

    # Wait for the results to load (optional)
    time.sleep(5)
    print("Search query submitted successfully.")


# Function to open a new tab and perform the search in that tab
def open_new_tab_and_search(driver, search_query):
    # Open a new tab and switch to it
    driver.execute_script("window.open('');")  # Open a new tab
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
    print("New tab opened and switched.")

    # Navigate directly to the "Generative Search" page in the new tab
    driver.get("https://research.alpha-sense.com/")  # Open the URL in the new tab

    # Wait for the page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror"))
    )
    print("Generative Search page loaded in the new tab.")

    # Perform the search in the new tab
    search_in_generative_search(driver, search_query)
    print("Search performed in the new tab.")


# Main block to handle command-line input
def main(search_query):
    # Initialize Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    try:
        # First login and search in the first tab
        login(driver)
        search_in_generative_search(driver, search_query)

        # Open a new tab and skip login, directly perform search in the second tab
        open_new_tab_and_search(driver, search_query)

    finally:
        # Keep the window open for observation
        time.sleep(30)
        driver.quit()  # Close the browser after the test


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Search in AlphaSense.")
    parser.add_argument(
        "search_query", type=str, help="The search term to enter into AlphaSense."
    )
    args = parser.parse_args()

    # Call the main function to perform the search
    main(args.search_query)
