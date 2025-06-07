from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd
import time


# Setup WebDriver 
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#Accept Alert
def accept_alert(driver):
    try:
        time.sleep(5)
        alert = driver.switch_to.alert
        alert.accept()
    except Exception:
        pass


# Navigate to Tender Page
def navigate_to_new_tenders(driver ,timeout=10):
    driver.get('https://etender.cpwd.gov.in/')
    accept_alert(driver)

    WebDriverWait(driver ,timeout).until( # wait untill element clicable
                    EC.element_to_be_clickable(
                (By.ID, "a_TenderswithinOneday3")))
    
    elem = driver.find_element(By.ID, "a_TenderswithinOneday3")
    ActionChains(driver).move_to_element(elem).click().perform()
    


#Set Dropdown Records
def set_record_limit(driver, limit="20"):


    time.sleep(5)
    dropdown = Select(driver.find_element(By.NAME, "awardedDataTable_length"))
    dropdown.select_by_visible_text(limit)
    time.sleep(5)


#Extract Tender Data
def extract_tender_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('td')
       
        if not cols and len(cols) != 9 :
            continue

        tender_id = cols[0].text.strip()
        if not tender_id.isdigit():
            continue

        data.append({
                "ref_no": cols[1].text.strip(),
                "title": BeautifulSoup(str(cols[2]), 'html.parser').text.strip(),
                "tender_value": cols[4].text.strip().replace("₹", "").strip(),
                "emd": cols[5].text.strip(),
                "bid_submission_end_date": cols[6].text.strip(),
                "bid_open_date": cols[7].text.strip(),
        })

    return data


# Save Data
def save_data(data, filename="tenders.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


#Main Scraper
def scrape_tender_details():
    driver = get_driver()
    try:
        navigate_to_new_tenders(driver)
        set_record_limit(driver)
        html = driver.page_source
        data = extract_tender_data(html)
        save_data(data)
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_tender_details()
