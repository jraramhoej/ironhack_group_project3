import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_population():
    # define url
    url = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Portugal_por_popula%C3%A7%C3%A3o"

    # make request
    response = requests.get(url)

    # get content
    content = response.content

    # create soup object
    soup = BeautifulSoup(content, 'html.parser')

    # find table
    table = soup.find("table", class_="wikitable sortable")

    # create DataFrame
    df = pd.read_html(str(table))[0]

    # flatten multi-index
    df.columns = df.columns.map(''.join).str.strip()

    # rename columns
    df.rename(columns={"ConcelhoConcelho": "city", "População Residente2018": "population"}, inplace=True)

    # remove nbsp
    df["population"] = df["population"].str.replace("\s+", "")

    return df[["city", "population"]]
