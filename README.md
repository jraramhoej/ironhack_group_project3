# Data Thieves (Ironhack group project)

## Purpose
There are many situations in which it could be useful to know how safe a certain area is. Maybe you're comparing the safety of different areas because you want to buy a house. Or maybe you're thinking about whether you need to put your scooter in a garage, or whether you can leave it out in the street. The purpose of the tool in this repository is to fetch and display relevant information about the safety of different areas in Portugal. 

## Method 
We retrieve the following information:

- the number of crimes reported to the police in Portugal during the year 2020 ([dados.gov.pt](https://dados.gov.pt/pt/datasets/crimes-registados-n-o-pelas-autoridades-policiais/))
- the perceived crime and safety indices reported by the website Numbeo ([numbeo.com](https://www.numbeo.com/crime/))
- the live traffic incidents retrieved by the HERE API ([website](https://developer.here.com/documentation/traffic/dev_guide/topics/what-is.html))
- cities and city population of Portugal from Wikipedia ([webpage](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Portugal_por_popula%C3%A7%C3%A3o))
- city coordinates from the Google Maps API ([website](https://developers.google.com/maps))

The data is stored in a MySQL database and can be retrieved to be presented to a user, using the command line interface. 

## Steps to setup
1. Run ```data_compilation.compile_data()``` in ```main.py``` to build dataframe
2. Run ```database.create_db()``` in ```main.py``` to create MySQL database
3. Run ```database.update_traffic()``` in ```main.py``` to update the traffic data, which changes continuously
4. Run ```present_data.show_final_data()``` in ```main.py``` to interface with the data using the command line

## Explanation of files

- ```main.py``` — see "Steps to setup" above
- ```crime.json``` — crime data from dados.gov.pt
- ```crime_meta.json``` — meta data about the crime data from dados.gov.pt
— ```data_compilation.py``` — compiling the data into one dataframe
- ```data_out.csv``` — csv-file with output data
- ```database.py``` — queries and functions to interact with MySQLWorkbench
- ```mysql_database.sql``` — the MySQL database
- ```perceived_crime.py``` — webscraping numpeo.com for crime and safety indices
- ```present_data.py``` — presenting the data using the command line
- ```requirements.txt``` — python libraries
- ```traffic_data.py``` — retrieving traffic data from the HERE API
- ```webscrape.py```— webscraping Wikipedia for city names and city populations