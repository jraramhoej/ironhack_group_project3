import pandas as pd


def get_crimes():

    # load file
    df = pd.read_json("crime.json")

    # create DataFrame
    df = pd.DataFrame(df["Dados"][0]["2020"])

    # change null values of "valor" to 0
    df['valor'] = df['valor'].fillna(0)

    # change "valor" to integer
    df['valor'] = df['valor'].astype(int)

    # aggregate the number of crimes per location
    df = df.groupby(["geodsg"]).agg({"valor": "sum"})

    # make locations into a column
    df.reset_index(level=0, inplace=True)

    # rename columns
    df.rename(columns={"geodsg": "city", "valor": "crimes_total_count_2020"}, inplace=True)

    return df
