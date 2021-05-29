from bs4 import BeautifulSoup
import requests


def get_perceived_crime(list_of_cities):

    names = list_of_cities

    results = []

    for name in names:
        try:
            print(name)   
        
            url = 'https://www.numbeo.com/crime/in/' + name




            response = requests.get(url)
            response

            soup = BeautifulSoup(response.content)

            tables = soup.find_all('table', attrs= {'class' : 'table_indices'})

            table = tables[0]

            crime = table.find_all('td', attrs= {'style' : 'text-align: right'})

            Index_table = list(zip(crime, ['Crime index','Safety index']))

            data = {'city': name}

            for v,k in Index_table:
                data[k] = v.text.strip('\n')
        
            results.append(data)

        except:
            print(name + '-Portugal')   
        
            url = 'https://www.numbeo.com/crime/in/' + name




            response = requests.get(url)
            response

            soup = BeautifulSoup(response.content)

            tables = soup.find_all('table', attrs= {'class' : 'table_indices'})

            table = tables[0]

            crime = table.find_all('td', attrs= {'style' : 'text-align: right'})

            Index_table = list(zip(crime, ['Crime index','Safety index']))

            data = {'city': name}

            for v,k in Index_table:
                data[k] = v.text.strip('\n')
        
            results.append(data)

    return results