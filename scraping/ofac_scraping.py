import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_ofac(search_term):
    url = 'https://sanctionssearch.ofac.treas.gov/'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        input_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'ctl00_MainContent_txtLastName'))
        )
        input_element.clear()  
        input_element.send_keys(search_term)
        search_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'ctl00_MainContent_btnSearch'))
        )
        search_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'gvSearchResults'))
        )
        table = driver.find_element(By.ID, 'gvSearchResults')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            data.append(row_data)
        df = pd.DataFrame(data, columns=['Name', 'Address', 'Type', 'Program', 'List', 'Score'])
        df.fillna("", inplace=True)
        return df.to_dict(orient='records')
    finally:
        driver.quit()
