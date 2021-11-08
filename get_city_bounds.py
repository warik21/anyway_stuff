import requests
import pandas as pd

# get a city list in hebrew\english
df = pd.read_excel(r'redash_jan.xlsx', engine='openpyxl')
city_list = ['holon']
north_bounds = []
east_bounds = []
south_bounds = []
west_bounds = []
cities_bounds = []

for city in city_list:
    city_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + \
                             city.__str__() + \
                             '&key=AIzaSyD_B16MmHv7mfQNKSanibF_S2ofJgI6Pc0&language = en')
    bounds = city_json.json()['results'][0]['geometry']['bounds']
    north_bound = bounds['northeast']['lng']
    east_bound = bounds['northeast']['lat']
    south_bound = bounds['southwest']['lng']
    west_bound = bounds['southwest']['lat']

    north_bounds.append(north_bound)
    east_bounds.append(east_bound)
    south_bounds.append(south_bound)
    west_bounds.append(west_bound)
    cities_bounds.append(north_bound, east_bound, south_bound, west_bound)


