import data_compilation
import mysql.connector

def sql_action(query):

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


# create new database
create_database = """CREATE DATABASE crime_db;"""

# create cities table
create_cities = """CREATE TABLE IF NOT EXISTS
crime_db.cities(
id INT PRIMARY KEY AUTO_INCREMENT,
city_name VARCHAR(50),
latitude FLOAT,
longitude FLOAT,
population FLOAT,
crime_frequency INT,
traffic_incidents INT);"""

def create_db():
    # dataframes
    df = data_compilation.compile_data()

    # create database
    sql_action(create_database)

    # create table
    sql_action(create_cities)

    # populate table
    # for city, latitude, longitude, population, crime_frequency, traffic_incidents in zip(df["city"], df["latitude"], df["longitude"], df["population"], df["crimes"], df["traffic_incidents"]):
    #
    #     # define query
    #     query = "INSERT INTO crime_db.cities(city_name, latitude, longitude, population, crime_frequency, traffic_incidents) VALUES(\"" + \
    #     str(city) + "\", " + \
    #     str(latitude) + ", " + \
    #     str(longitude) + ", " + \
    #     str(population) + ", " + \
    #     str(crime_frequency) + ", " + \
    #     str(traffic_incidents) + ");"
    #
    #     # execute query
    #     sql_action(query)

    # update table
    for city_name, traffic_incidents in zip(df["city"], df["traffic_incidents"]):

        # define query
        query = "UPDATE crime_db.cities SET crime_db.cities.traffic_incidents = crime_db.cities.traffic_incidents" \
                + str(traffic_incidents) \
                + "WHERE crime_db.cities.city_name = "\
                + str(city_name) \
                + ";"

        # execute query
        sql_action(query)
