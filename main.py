from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def create_and_download_data_file():
    # Set up the WebDriver (e.g., Chrome)
    options = webdriver.ChromeOptions()
    download_dir = os.getcwd()  # Set download directory to current working directory
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the web page
        driver.get("https://www.gunviolencearchive.org/")

        # Navigate to the query page
        driver.get("https://www.gunviolencearchive.org/query")

        # Simulate clicking the button to execute the database query
        query_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "edit-actions-execute"))  # Replace with the actual button ID
        )
        query_button.click()

        # Wait for the query results to be returned
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "gva-entry-results-limiter"))  # Replace with the actual result element ID
        )
        
        # Simulate clicking the button to export the CSV
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='button' and text()='Export as CSV']"))
        )
        download_button.click()

        # Simulate clicking the button to download the CSV
        download_button = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='button big' and text()='Download']"))
        )
        download_button.click()

        # Wait for the download to complete
        time.sleep(10)  # Adjust time as needed

        print(f"CSV downloaded to: {download_dir}")

    finally:
        # Close the browser
        driver.quit()
        # Rename the downloaded file
        for filename in os.listdir(download_dir):
            if filename.startswith("export") and filename.endswith(".csv"):
                os.rename(os.path.join(download_dir, filename), os.path.join(download_dir, "gun_violence_data.csv"))
                print("File renamed to gun_violence_data.csv")
                break

if __name__ == "__main__":
    # Check if the file exists, if not, call the function
    if not os.path.exists("gun_violence_data.csv"):
        create_and_download_data_file()
    else:
        print("gun_violence_data.csv already exists.")