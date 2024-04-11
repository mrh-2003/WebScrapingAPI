""" import requests
from bs4 import BeautifulSoup

from models.TheWorldBank import TheWorldBank

from models.OffshoreLeaks import OffshoreLeaks

website = "https://offshoreleaks.icij.org/search?q=juan&c=&j=&d="
response = requests.get(website)
print(response.text)

if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, "lxml")
    table = soup.find("table", class_ = "bg-primary text-white").get_text()
    #rows = table.find_all("tr")
    print(table)
else:
    print("Error: Could not retrieve the website: ", response.status_code) """
""" 

from bs4 import BeautifulSoup
import requests

url = 'https://offshoreleaks.icij.org/search?q=juan&c=&j=&d='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, "lxml")
    table = soup.find("table", class_ = "table table-sm table-striped search__results__table").get_text()
    #rows = table.find_all("tr")
    print(table)
else:
    print('Error:', response.status_code)

 """


""" import requests
import pandas as pd
A
def extract_tables(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status() 

    tables = pd.read_html(response.text)

    return tables

url = "https://offshoreleaks.icij.org/search?q=juan&c=&j=&d="
try:
    extracted_tables = extract_tables(url)
    print(extracted_tables[0])

except Exception as e:
    print(f"Ocurrió un error al extraer las tablas: {e}") """

""" 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL de la página web
url = 'https://sanctionssearch.ofac.treas.gov/'

# Valor a buscar
valor_busqueda = 'juan'

# Configurar el navegador en modo sin cabeza
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

try:
    # Navegar a la página web
    driver.get(url)

    # Encontrar el campo de entrada y enviar el valor de búsqueda
    input_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ctl00_MainContent_txtLastName'))
    )
    input_element.clear()  # Limpiar el campo de entrada
    input_element.send_keys(valor_busqueda)
    
    # Encontrar el botón de búsqueda y hacer clic en él
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ctl00_MainContent_btnSearch'))
    )
    search_button.click()

    # Esperar a que se carguen los resultados (puedes ajustar el tiempo de espera según sea necesario)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'gvSearchResults'))
    )

    # Capturar la información de la tabla y cargarla en un DataFrame de pandas
    tabla = driver.find_element(By.ID, 'gvSearchResults')
    rows = tabla.find_elements(By.TAG_NAME, 'tr')
    
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    # Crear DataFrame de pandas
    df = pd.DataFrame(data[1:], columns=data[0])

    # Imprimir DataFrame
    print(df)

finally:
    # Cerrar el navegador al finalizar
    driver.quit()
 """