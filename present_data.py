import database
import pandas as pd
from tabulate import tabulate


def show_final_data():

    # retrieve data from database
    results_df = database.fetch_from_db()

    # get column per person
    results_df["crimes_per_person_2020"] = results_df["crimes_total_count_2020"] / results_df["population"]

    # get percentile for crime frequencies
    results_df["crimes_percentiles"] = pd.qcut(results_df["crimes_per_person_2020"], 10, labels=["10% cities with least ", "20% cities with least ", "30% cities with least ", "40% cities with least ", "the mid range ", "the middle range ", "40% cities with most ", "30% cities with most ", "20% cities with most ", "10% cities with most "])

    # get percentile for perceived crime frequencies
    results_df["perceived_crime_percentiles"] = pd.qcut(results_df["perceived_crime_index"], 10, labels=["10% cities where the locals think least ", "20% cities where the locals think least ", "30% cities where the locals think least ", "40% cities where the locals think least ", "the mid range of perceived ", "the middle range of perceived ", "40% cities where the locals think most ", "30% cities where the locals think most ", "20% cities where the locals think most ", "10% cities where the locals think most "])

    # input first city
    city1 = input("Enter city in Portugal.").strip()

    # input second city
    city2 = input("Enter another Portuguese city for comparison. If you don't want to compare, press enter.").strip()

    #if input is single city, give information about that city
    if city2 == "":
        try:
            # define condition
            condition = results_df["city_name"] == city1

            # define data
            total_crime_city1 = list(results_df[condition]["crimes_total_count_2020"])[0]
            crime_city1 = list(results_df[condition]["crimes_per_person_2020"])[0]
            perceived_crime_city1 = list(results_df[condition]["perceived_crime_index"])[0]
            crime_percentiles_city1 = list(results_df[condition]["crimes_percentiles"])[0]


            data = [["city", city1],
                    ["total crime frequency 2020", total_crime_city1],
                    ["crimes per person 2020", round(crime_city1, 2)],
                    ["perceived crime index", perceived_crime_city1]]

            # print table
            print(tabulate(data, headers='firstrow', tablefmt='psql'))

            # crime
            print(f'{city1} is among the {crime_percentiles_city1}crime in Portugal.')

            # actual crime levels
            if crime_percentiles_city1 == "10% cities with least ":
                crime_level = 1
            if crime_percentiles_city1 == "20% cities with least ":
                crime_level = 2
            if crime_percentiles_city1 == "30% cities with least ":
                crime_level = 3
            if crime_percentiles_city1 == "40% cities with least ":
                crime_level = 4
            if crime_percentiles_city1 == "the mid range ":
                crime_level = 5
            if crime_percentiles_city1 == "the middle range ":
                crime_level = 6
            if crime_percentiles_city1 == "40% cities with most ":
                crime_level = 7
            if crime_percentiles_city1 == "30% cities with most ":
                crime_level = 8
            if crime_percentiles_city1 == "20% cities with most ":
                crime_level = 9
            if crime_percentiles_city1 == "10% cities with most ":
                crime_level = 10

            # perceived crime
            if perceived_crime_city1 < 20:
                print(f"Based on the index of perceived crime, the crime levels are very low.")
                index_level = 2
            elif perceived_crime_city1 < 40:
                print(f"Based on the index of perceived crime, the crime levels are low.")
                index_level = 4
            elif perceived_crime_city1 < 60:
                print(f"Based on the index of perceived crime, the crime levels are moderate.")
                index_level = 6
            elif perceived_crime_city1 < 80:
                print(f"Based on the index of perceived crime, the crime levels are high.")
                index_level = 8
            else:
                print(f"Based on the index of perceived crime, the crime levels are very high.")
                index_level = 10

            # compare perceived crime with actual crime
            if crime_level > index_level:
                print(f'In {city1}, people feel safer than what the actual crime rate would suggest.')
            if index_level > crime_level:
                print(f'In {city1}, people feel that it is more dangerous than it actually is')
            if index_level == crime_level:
                print("The perceived crime rate matches the actual crime rate.")

        # alternative if the city is not found
        except:
            print("There is no data for the city you chose. Please run again and enter another city.")

    # if two cities are chosen, we do a comparison
    else:
        try:
            # condition for first city
            condition1 = results_df["city_name"] == city1

            # condition for second city
            condition2 = results_df["city_name"] == city2

            # define data for table
            total_crime_city1 = list(results_df[condition1]["crimes_total_count_2020"])[0]
            total_crime_city2 = list(results_df[condition2]["crimes_total_count_2020"])[0]
            crime_city1 = list(results_df[condition1]["crimes_per_person_2020"])[0]
            crime_city2 = list(results_df[condition2]["crimes_per_person_2020"])[0]
            perceived_crime_city1 = list(results_df[condition1]["perceived_crime_index"])[0]
            perceived_crime_city2 = list(results_df[condition2]["perceived_crime_index"])[0]
            data = [["city", "total crime frequency 2020", "crimes per person", "perceived crime index"], [city1, total_crime_city1, crime_city1, perceived_crime_city1], [city2, total_crime_city2, crime_city2, perceived_crime_city2]]

            # print table
            print(tabulate(data, headers='firstrow', tablefmt='psql'))

            # print statements
            # actual crime
            if crime_city1 > crime_city2:
                print(f'There are more crimes committed in {city1}, which means that {city2} is safer.')
            elif crime_city1 < crime_city2:
                print(f'There are more crimes committed in {city2}, which means that {city1} is safer.')
            else:
                print("The two cities have the same crime rate.")

            # perceived crime
            if perceived_crime_city1 > perceived_crime_city2:
                print(f'The locals feel that {city2} is safer.')
            elif perceived_crime_city1 < perceived_crime_city2:
                print(f'The locals feel that {city1} is safer.')
            else:
                print("The two cities have the same perceived crime rate.")

        # alternative if one or both of the cities are not found
        except:
            print("There is no data for the cities you chose. Please run again and enter another pair of cities.")
