import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# Function to set up the Selenium WebDriver and perform the search
def search_in_alphasense(search_query):
    # URL to navigate
    URL = "https://research.alpha-sense.com/"

    # Initialize Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    try:
        print("Opening URL...")
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
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

        # Method 1: Using XPath based on 'aria-label' attribute to click "Generative Search"
        print("Trying Method 1: XPath based on aria-label...")
        generative_search_button_1 = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@aria-label='Generative Search']")
            )
        )
        generative_search_button_1.click()
        print("Clicked 'Generative Search' using Method 1.")

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

        # Open a new tab and switch to it for Tesla search
        driver.execute_script("window.open('');")  # Open a new tab
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

        # Navigate to AlphaSense in the new tab
        driver.get(URL)
        print("Navigated to AlphaSense URL in the new tab.")

        # Wait for the new tab to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        print("Login page loaded in new tab.")

        # Enter username in the new tab
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys("sasha@katecapllc.com")
        print("Entered username in new tab.")

        # Click continue in the new tab
        continue_button = driver.find_element(By.ID, "next-step")
        continue_button.click()
        print("Clicked continue in new tab.")

        # Wait for password field
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("tvz0bur1twz_GRJ_aeu")
        print("Entered password in new tab.")

        # Click submit in the new tab
        submit_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-testid='loginSubmitButton']"
        )
        submit_button.click()
        print("Clicked submit in new tab.")

        # Wait for the dashboard to load in the second tab
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror"))
        )
        print("Dashboard loaded in new tab.")

        # Perform the search for "Tesla" in the new tab
        search_textarea = driver.find_element(
            By.CSS_SELECTOR, "textarea[aria-invalid='false']"
        )
        tesla_query = "Tesla"
        search_textarea.send_keys(tesla_query)  # Enter "Tesla"
        print(f"Entered search query for Tesla: {tesla_query}")

        # Simulate pressing Enter to submit the search
        search_textarea.send_keys(Keys.RETURN)  # Simulating Enter key press
        print("Simulated Enter key press to submit the Tesla search.")

        # Wait for the search results to load (optional)
        time.sleep(5)
        print("Tesla search query submitted successfully.")

    finally:
        # Keep the window open for observation
        time.sleep(30)
        driver.quit()  # Close the browser after the test


# Main block to handle command-line input
if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Search in AlphaSense.")
    parser.add_argument(
        "search_query", type=str, help="The search term to enter into AlphaSense."
    )
    args = parser.parse_args()

    # Call the function to perform the search
    search_in_alphasense(args.search_query)
