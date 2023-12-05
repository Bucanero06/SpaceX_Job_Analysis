import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Fresh scrape of SpaceX jobs
FORCE_OVERWRITE = False
ANALYZE_DATA = True

# Set up the WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")

driver = webdriver.Chrome(options=chrome_options)

# If file exists spacex_jobs.csv then do not overwrite it
import os

if not os.path.exists("spacex_jobs.csv") or FORCE_OVERWRITE:

    # Navigate to the SpaceX careers page
    driver.get("https://www.spacex.com/careers/jobs/")

    # Wait for the dynamic content to load
    wait = WebDriverWait(driver, 10)

    # Wait for the job listings table to be present
    job_listings_table = wait.until(EC.presence_of_element_located((By.ID, "joblisttable")))

    # Find all row elements within the table
    rows = job_listings_table.find_elements(By.TAG_NAME, "tr")

    # Initialize lists to hold columns and data
    columns = []
    data = []

    # Process the header row separately
    header = rows[0].find_elements(By.TAG_NAME, "th")
    columns = [th.text for th in header]  # Adjust if header cells have different structure
    columns.append('Link')  # Add a column for the link

    # Iterate over the remaining rows
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]

        # Extract href from the first cell
        first_cell_link = cells[0].find_element(By.TAG_NAME, "a").get_attribute('href')
        row_data.append(first_cell_link)

        data.append(row_data)
        # print(data[-1])

    # Close the browser session
    driver.quit()

    # Create a DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Display or process the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv("spacex_jobs.csv", index=False)

if ANALYZE_DATA:
    # Load or use the previously created DataFrame
    # If df is not defined then load the CSV file
    try:
        df
    except NameError:
        df = pd.read_csv("spacex_jobs.csv")


    # ... previous code to collect job titles and links ...

    # Function to extract basic qualifications
    def extract_basic_qualifications(driver, url):
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "content")))

        try:
            # XPath to find the <ul> list following the <p> containing "BASIC QUALIFICATIONS"
            xpath = "//p[strong[contains(text(), 'BASIC QUALIFICATIONS')]]/following-sibling::ul[1]"
            qualifications_element = driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            try:
                xpath = "//div[strong[contains(text(), 'BASIC QUALIFICATIONS')]]/following-sibling::ul[1]"
                qualifications_element = driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                try:
                    xpath = "//div[b[contains(text(), 'Basic Qualifications')]]/following-sibling::ul[1]"
                    qualifications_element = driver.find_element(By.XPATH, xpath)
                except NoSuchElementException:
                    try:
                        xpath = "//p[b[contains(text(), 'Basic Qualifications')]]/following-sibling::ul[1]"
                        qualifications_element = driver.find_element(By.XPATH, xpath)
                    except NoSuchElementException as e:
                        try:
                            # XPath to find the <ul> list following the <p> containing "BASIC QUALIFICATIONS"
                            xpath = "//p[b[contains(text(), 'BASIC QUALIFICATIONS')]]/following-sibling::ul[1]"
                            qualifications_element = driver.find_element(By.XPATH, xpath)
                            return [li.find_element(By.TAG_NAME, "p").text for li in
                                    qualifications_element.find_elements(By.TAG_NAME, "li")]
                        except NoSuchElementException:
                            return None

        return [li.text for li in qualifications_element.find_elements(By.TAG_NAME, "li")]


    # Initialize a dictionary to store job data
    job_details = {}
    failed_links = []

    for title, link in zip(df['JOB TITLE'], df['Link']):
        try:
            print(f"Processing {title} ...")
            print(f"Link: {link}")
            qualifications = extract_basic_qualifications(driver, link)
            if qualifications is None:
                failed_links.append(link)
                continue
            # job_details[title] = {
            #     "link": link,
            #     "qualifications": qualifications
            # }
            print(f"Qualifications: {qualifications}\n")

            # Add the qualifications to the DataFrame
            df.loc[df['Link'] == link, 'Qualifications'] = '\n'.join(qualifications)
        except Exception as e:
            print(e)
            failed_links.append(link)
    # Close the browser session
    driver.quit()

    # Save the DataFrame to a CSV file
    df.to_csv("spacex_jobs.csv", index=False)

    # Display the failed links
    print("Failed links:")
    for link in failed_links:
        print(link)
