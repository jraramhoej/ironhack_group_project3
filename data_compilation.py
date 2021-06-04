import web_scrape
import crime_data
import traffic_data
import perceived_crime
import json
import requests
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Other Name")


# get coordinates for location using geopy
def get_coordinates(city, country="Portugal"):

    # define city
    city = city

    # define country
    country = country

    # get coordinates
    loc = geolocator.geocode(city + ',' + country)

    return str({"latitude": loc.latitude, "longitude": loc.longitude})


# alternative way of getting coordinates for location using google maps API
def get_coord(city):

    # define API key
    key = "MY_API_KEY"

    # define url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + city + "&key=" + key

    # make request
    response = requests.get(url)

    latitude = response.json()["results"][0]["geometry"]["location"]["lat"]
    longitude = response.json()["results"][0]["geometry"]["location"]["lng"]

    return str({"latitude": latitude, "longitude": longitude})


def string_to_dict(dict_string):

    # Convert to proper json format
    dict_string = dict_string.replace("'", '"').replace('u"', '"')

    return json.loads(dict_string)


def get_traffic_incidents(row):

    try:
        out = traffic_data.get_incident_count(float(row["latitude"]), float(row["longitude"]))
    except:
        out = 0
    return out


def compile_data():

    # create df with cities and population
    df = web_scrape.get_population()

    # create df with city and crime rate
    crime = crime_data.get_crimes()

    # add longitude and latitude with either geopy or the Google Maps API
    #df["coordinates"] = df["city"].apply(get_coordinates)
    df["coordinates"] = df["city"].apply(get_coord)

    # convert string to dict
    df["coordinates"] = df["coordinates"].apply(string_to_dict)

    # create empty lists for lat and long
    latitudes = []
    longitudes = []

    # retrieve lat and long from coordinates
    for row in df["coordinates"]:
        latitudes.append(row["latitude"])
        longitudes.append(row["longitude"])

    df["latitude"] = latitudes
    df["longitude"] = longitudes

    # merge df with crime df
    df = df.merge(crime, how="inner", left_on="city", right_on="city")

    # drop coordinates
    df.drop(columns=['coordinates'], inplace=True)

    # add traffic incidents
    df["traffic_incidents_live_count"] = df.apply(get_traffic_incidents, axis=1)

    # replace NaN with None
    df = df.replace(np.nan, None)

    # remove special characters in city names
    df["city"] = df['city'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # change Lisboa to Lisbon
    df["city"] = df["city"].str.replace("Lisboa", "Lisbon")

    # retrieveing the perceived crime data from Numbeo
    crime_perceived = perceived_crime.get_perceived_crime(list(df['city']))

    # create dataframe
    crime_perceived_df = pd.DataFrame(crime_perceived)

    # remove "-Portugal"
    crime_perceived_df["city"] = crime_perceived_df["city"].str.replace("-Portugal", "")

    # merge df with perceived crime df
    df = df.merge(crime_perceived_df, how="inner", left_on="city", right_on="city")

    # fill empty values with None
    #df["crime_index"].where(df["crime_index"].notnull(), None, inplace=True)
    #df["safety_index"].where(df["safety_index"].notnull(), None, inplace=True)

    #df = df.replace(np.nan, None)

    #save as csv
    df.to_csv("data_out.csv", index=False)

    return df
