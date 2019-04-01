import pandas as pd
from geopy.geocoders import GoogleV3

df = pd.read_csv("supermarkets.csv")
df.head()

goo = GoogleV3()

goo.geocode("3995 23rd St, San Francisco, CA 94114")

df["Address"] = df["Address"] + ", " + df['City'] + ", " + df['State']

df["Coordinates"] = df["Address"].apply(goo.geocode)

df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude if x != None else None)