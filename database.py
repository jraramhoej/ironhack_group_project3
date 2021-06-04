import mysql.connector
import pandas as pd

def save_to_db(query):

    # establish connection to a database
    connection = mysql.connector.connect(user='root', password='18Rj7192!', host='localhost', database='sakila',
                                         auth_plugin='mysql_native_password')

    # try / except (or if statement) to check if connected
    if connection.is_connected():
        print("Connection open.")
    else:
        print("Connection is not successfully open.")

    # define object used to interact with the database
    cursor = connection.cursor()

    # execute query, call cursor to execute
    cursor.execute(query)
    print("Query executed.")

    # commit changes to MySQL
    connection.commit()
    print("Committed to MySQL.")

    # clear the cursor
    cursor.close()
    connection.close()

def fetch_from_db():

    # establish connection to a database
    connection = mysql.connector.connect(user='root', password='18Rj7192!', host='localhost', database='sakila',
                                         auth_plugin='mysql_native_password')

    # try / except (or if statement) to check if connected
    if connection.is_connected():
        print("Connection open.")
    else:
        print("Connection is not successfully open.")

    # define object used to interact with the database
    cursor = connection.cursor()

    # define query
    query = ("SELECT * FROM crime_database.cities;")

    # execute query, call cursor to execute
    cursor.execute(query)
    print("Query executed.")

    # create variable for results
    results = cursor.fetchall()

    # define column names
    column_names = cursor.description

    # create df
    results_df = pd.DataFrame(results, columns=[header[0] for header in column_names])

    # commit changes to MySQL
    connection.commit()
    print("Committed to MySQL.")

    # clear the cursor
    cursor.close()
    connection.close()

    return results_df


# create new database
create_database = """CREATE DATABASE crime_database;"""

# create cities table
create_cities = """CREATE TABLE IF NOT EXISTS
crime_database.cities(
id INT PRIMARY KEY AUTO_INCREMENT,
city_name VARCHAR(50),
latitude FLOAT,
longitude FLOAT,
population FLOAT,
crimes_total_count_2020 INT,
traffic_incidents_live_count INT,
perceived_crime_index FLOAT,
perceived_safety_index FLOAT);"""
def print_df():
    print(pd.read_csv("data_out.csv"))

def create_db():
    # dataframes
    df = pd.read_csv("data_out.csv")

    # create database
    save_to_db(create_database)

    # create table
    save_to_db(create_cities)

    # populate table
    for city, latitude, longitude, population, crimes_total_count_2020, traffic_incidents_live_count, crime_index, safety_index in zip(df["city"], df["latitude"], df["longitude"], df["population"], df["crimes_total_count_2020"], df["traffic_incidents_live_count"], df["crime_index"], df["safety_index"]):

        # define query
        query = "INSERT INTO crime_database.cities(city_name, latitude, longitude, population, crimes_total_count_2020, traffic_incidents_live_count, perceived_crime_index, perceived_safety_index) VALUES(\"" + \
        str(city) + "\", " + \
        str(latitude) + ", " + \
        str(longitude) + ", " + \
        str(population) + ", " + \
        str(crimes_total_count_2020) + ", " + \
        str(traffic_incidents_live_count) + ", " + \
        str(crime_index) + ", " + \
        str(safety_index) + ");"

        # execute query
        save_to_db(query)

def update_traffic():

    # create dataframe
    df = pd.read_csv("data_out.csv")

    # update table
    for city_name, traffic_incidents in zip(df["city"], df["traffic_incidents_live_count"]):

        # define query
        query = "UPDATE crime_database.cities SET crime_database.cities.traffic_incidents_live_count = crime_database.cities.traffic_incidents_live_count + " + str(traffic_incidents) + " WHERE crime_database.cities.city_name = \"" + str(city_name) + "\";"

        # execute query
        save_to_db(query)


