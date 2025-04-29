from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time

# List of tender websites
urls = [
    "https://tntenders.gov.in/nicgep/app",
    "https://eprocure.gov.in/epublish/app",
    "https://etenders.gov.in/eprocure/app?page=FrontEndTendersOpen",
    "https://etenders.kerala.gov.in/nicgep/app"
]

# Function to fetch tender details from URL
def fetch_tender_details(driver, url):
    tender_data = []
    try:
        driver.get(url)

        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'list_table')]"))
        )
        
        tender_rows = table.find_elements(By.XPATH, ".//tbody/tr")
        
        for row in tender_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            tender_details = [col.text.strip() for col in cols]

            if tender_details and any(tender_details):  
                tender_data.append(tender_details)

    except Exception as e:
        print(f"Error while fetching {url}: {e}")

    return tender_data

def clean_and_save(all_tenders):
    
    flat_list = [item for sublist in all_tenders for item in sublist]
    raw_text = " ".join(flat_list)

    # Clean text
    raw_text = raw_text.replace('Latest Tenders updates every 15 mins.', '')
    raw_text = raw_text.replace('More...', '')

    # Extracting tender lines
    lines = raw_text.split('\n')
    tender_lines = [line for line in lines if re.search(r'^\d+\.', line.strip())]

    data = []
    for line in tender_lines:
        line = re.sub(r'^\d+\.\s*', '', line).strip()

        date_match = list(re.finditer(r'\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2} (?:AM|PM)', line))

        if len(date_match) >= 2:
            first_date = date_match[0]
            second_date = date_match[1]

            title_ref_part = line[:first_date.start()].strip()

            title_ref_split = title_ref_part.rsplit(' ', 1)
            if len(title_ref_split) == 2:
                title, ref_no = title_ref_split
            else:
                title = title_ref_split[0]
                ref_no = ''

            closing_date = line[first_date.start():first_date.end()]
            bid_opening_date = line[second_date.start():second_date.end()]

            data.append([title.strip(), ref_no.strip(), closing_date.strip(), bid_opening_date.strip()])

    # DataFrame
    df = pd.DataFrame(data, columns=['Tender Title', 'Reference No', 'Closing Date', 'Bid Opening Date'])

    # Saving to CSV append mode
    df.to_csv('tenders.csv', mode='a', index=False, header=False)
    print("Tenders saved to tenders.csv")

def main_scraper():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    all_tenders = []
    for url in urls:
        print(f"\nFetching tenders from {url}\n" + "-"*60)
        tenders = fetch_tender_details(driver, url)

        for tender in tenders:
            all_tenders.append(tender)
            print(tender)
        print("="*60)

    driver.quit()

    if all_tenders:
        clean_and_save(all_tenders)
    else:
        print("No tenders fetched this time.")

if __name__ == "__main__":
    while True:
        print("\nStarting tender fetch cycle...")
        main_scraper()
        print("Waiting 15 minutes before next fetch...")
        time.sleep(15 * 60)
