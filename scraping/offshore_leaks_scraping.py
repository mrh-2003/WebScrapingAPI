import requests
import pandas as pd

def scrape_offshore_leaks(name):
    url = f"https://offshoreleaks.icij.org/search?q={name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        table = pd.read_html(response.text)[0]
        table.fillna("", inplace=True)
        return table.to_dict(orient='records')

    except Exception as e:
        raise e