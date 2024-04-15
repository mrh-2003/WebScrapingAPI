#Información general

El presente proyecto es una REST API desarrollada en Python usando el framework FastAPI. Este proyecto hace uso de web scraping para extraer información de entidades en listas de alto riesgo. Las fuentes de información usadas son:

v	Offshore Leaks Database: https://offshoreleaks.icij.org o

§	Atributos: Entity, Jurisdiction, Linked To, Data From

v	The World Bank:  https://projects.worldbank.org/en/projects operations/procurement/debarred-firms

§	Atributos: Firm Name, Address, Country, From Date (Ineligibility Period), To Date (Ineligibility Period), Grounds

v	OFAC: https://sanctionssearch.ofac.treas.gov/

§	Atributos: Name, Address, Type, Program(s), List, Score

#Pasos para ejecutar el proyecto:

Clonar el repositorio en Git Hub y de forma local crear un entorno virtual

python -m venv venv

Después activar el entorno virtual

venv\Scripts\activate

Se debe instalar todas las dependencias necesarias

pip install -r requirements.txt

Se debe crear las variables de entorno en un archivo .env, las variables usadas son

SECRET\_KEY = "jhr8743rg8yerh34985r3y4y8rg83h48r3h89j32i4hny3gd6534tr73frh3498urhy83hg8fr743r3gryfhhg"

ALGORITHM = "HS256"

ACCESS\_TOKEN\_EXPIRE\_MINUTES = 30

API\_KEY = "z9duUaFUiEUYSHs97CU38fcZO7ipOPvm"

Estos datos deben ser privados, sin embargo, lo comparto para facilidad de uso.

Después se debe ejecutar el api con el siguiente comando

uvicorn main:app --reload

Cuando ya este ejecutado se debe entrar al dominio que te brinda la api y adicionarle /docs para poder ingresar a la documentación de swagger. El dominio por defecto es

http://127.0.0.1:8000/docs

Dentro se debe autenticar en la aplicación para poder hacer uso de la REST API

Username: mrh2003

Password: secret

O si prefiere cree sus propias credenciales y después inicie sesión.

Dentro tendrá acceso a los endpoints que traen información de las 3 fuentes mencionadas anteriormente.  También se adjuntara la colección de postman para que se realicen las pruebas por ese medio.
