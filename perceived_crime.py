from bs4 import BeautifulSoup
import requests
import time
import random


def get_perceived_crime(list_of_cities):

    results = []

    for name in list_of_cities:

        try:
            # use randomly different times for each request
            time.sleep(random.random())

            try:
                # define url
                url = 'https://www.numbeo.com/crime/in/' + name.replace(" ", "-")

                # make request
                response = requests.get(url)

                # create soup object
                soup = BeautifulSoup(response.content, 'html.parser')

                # find all tables
                tables = soup.find_all('table', attrs={'class': 'table_indices'})

                # choose first table
                table = tables[0]
            except:
                # define url
                url = 'https://www.numbeo.com/crime/in/' + name.replace(" ", "-") + "-Portugal"

                # make request
                response = requests.get(url)

                # create soup object
                soup = BeautifulSoup(response.content, 'html.parser')

                # find all tables
                tables = soup.find_all('table', attrs={'class': 'table_indices'})

                # choose first table
                table = tables[0]

            # find the data we are looking for
            crime = table.find_all('td', attrs={'style': 'text-align: right'})

            # retrieve specific numbers
            index_table = list(zip(crime, ['crime_index', 'safety_index']))

            # define city name
            data = {'city': name}

            # loop and add to data dictionary
            for v, k in index_table:
                data[k] = v.text.strip('\n')

            results.append(data)

        except:
            continue

    return results
