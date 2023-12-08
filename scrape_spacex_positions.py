import concurrent
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Fresh scrape of SpaceX jobs
FORCE_OVERWRITE = False
SCRAPE_QUALIFICATIONS = True

# Set up the WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")

# If file exists spacex_jobs.csv then do not overwrite it
import os

if not os.path.exists("spacex_jobs.csv") or FORCE_OVERWRITE:
    driver = webdriver.Chrome(options=chrome_options)

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

if SCRAPE_QUALIFICATIONS:
    # Load or use the previously created DataFrame
    # If df is not defined then load the CSV file
    try:
        df
    except NameError:
        df = pd.read_csv("spacex_jobs.csv")


    def scrape_job(title, link):
        content_text = None
        try:
            driver = webdriver.Chrome(options=chrome_options)  # Initialize the WebDriver
            wait = WebDriverWait(driver, 10)

            print(f"Processing {title} ...")
            driver.get(link)
            wait.until(EC.presence_of_element_located((By.ID, "content")))
            content = driver.find_element(By.ID, "content")
            content_text = content.text
            lines = content_text.split('\n')

            # Initializing variables
            sections = {
                "RESPONSIBILITIES:": [],
                "BASIC QUALIFICATIONS:": [],
                "PREFERRED SKILLS AND EXPERIENCE:": [],
                "ADDITIONAL REQUIREMENTS:": [],
                "COMPENSATION AND BENEFITS:": [],
                "ITAR REQUIREMENTS:": [],
            }

            current_section = None
            for line in lines:
                # Check if the line is a section header
                if any(section in line for section in sections):
                    current_section = next(section for section in sections if section in line)
                elif current_section:
                    # Add the line to the current section if it's not empty
                    if line.strip():
                        sections[current_section].append(line)

            # Displaying the extracted information
            for section, content in sections.items():
                print(f"{section}\n{' '.join(content)}")
            print()

            driver.quit()
            return title, sections  # Return the extracted data
        except Exception as e:
            print(e)
            driver.quit()
            return title, None  # Indicate failure


    failed_links = []


    assert len(df) > 1, "There should be at least 2+ jobs available"

    # Example usage with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=28) as executor:  # Adjust max_workers based on your resource availability
        futures = {executor.submit(scrape_job, title, link): (title, link) for title, link in
                   zip(df['JOB TITLE'], df['Link'])}

        for future in concurrent.futures.as_completed(futures):
            title, result = future.result()
            if result:
                # Update DataFrame with the result
                df.loc[df['JOB TITLE'] == title, 'RESPONSIBILITIES'] = ' '.join(result["RESPONSIBILITIES:"])
                df.loc[df['JOB TITLE'] == title, 'BASIC QUALIFICATIONS'] = ' '.join(
                    result["BASIC QUALIFICATIONS:"])
                df.loc[df['JOB TITLE'] == title, 'PREFERRED SKILLS AND EXPERIENCE'] = ' '.join(
                    result["PREFERRED SKILLS AND EXPERIENCE:"])
                df.loc[df['JOB TITLE'] == title, 'ADDITIONAL REQUIREMENTS'] = ' '.join(
                    result["ADDITIONAL REQUIREMENTS:"])
                df.loc[df['JOB TITLE'] == title, 'COMPENSATION AND BENEFITS'] = ' '.join(
                    result["COMPENSATION AND BENEFITS:"])
            else:
                print(f"Failed to process {title}")
                failed_links.append((title, result))

    # Save the DataFrame to a CSV file
    df.to_csv("spacex_jobs.csv", index=False)

    # Display the failed links
    print("Failed links:")
    for link in failed_links:
        print(link)
