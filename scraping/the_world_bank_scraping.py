from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_the_world_bank():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms')
        page.wait_for_timeout(3000) 
        content = page.content()
        tables = pd.read_html(content)     
        browser.close()
        return tables[1].to_dict(orient='records')
dataframe = scrape_the_world_bank()
print(dataframe)
