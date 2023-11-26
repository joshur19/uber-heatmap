#### Project name: uber aggregation
### File: uber_agg.py main source code file
## Function: main program 
# Creation Date // Last Updated: 28/05/2023 // 26/11/2023

# tutorial https://python.plainenglish.io/how-to-build-route-heatmaps-in-python-ebac363471d7

# imports
import pandas as pd
import folium
import json
import functions as fn
import archive

# globals
CITY = 'Santo Domingo'


######## code #########

# read csv file
df_raw = pd.read_csv('trips_data_lya.csv', encoding='utf8')
print("Raw DataFrame: \n", df_raw.head())
print(archive.separator)

# clean record (drop cancelled trips + focus on one city)
df_raw.drop(df_raw[df_raw['Trip or Order Status'] != 'COMPLETED'].index, inplace = True)
df_raw.drop(df_raw[df_raw['City'] != CITY].index, inplace = True)

# keep only the columns with the coordinates and relevant address information
df_coords = df_raw[['Begin Trip Lat','Begin Trip Lng','Begin Trip Address','Dropoff Lat','Dropoff Lng','Dropoff Address']]

# drop the numerical coordinates and count up trips by comparing start/end addresses
df_grouped = df_coords.groupby(['Begin Trip Address', 'Dropoff Address']).size().reset_index()
df_grouped = df_grouped.rename(columns={0: 'Count'})

# calculate the average coordinates of every trip and reintegrate the coords to df
fn.mean_coords(df_grouped, df_coords)

print("Grouped DataFrame: \n", df_grouped.head())
print(archive.separator)

# get coords list (through API) for every route and add it to DF
fn.get_coords(df_grouped)

# for testing: read df_grouped from csv
#df_grouped = pd.read_csv('with_coords.csv')
#if 'Unnamed: 0' in df_grouped.columns: df_grouped = df_grouped.drop(columns="Unnamed: 0")

# normalize count to between 0 and 1 for folium
cnt_list = df_grouped['Count'].tolist()
max_cnt = max(cnt_list)
min_cnt = min(cnt_list)

for i in range(len(cnt_list)):
    if(max_cnt-min_cnt != 0): cnt_list[i] = (cnt_list[i] - min_cnt) / (max_cnt - min_cnt)
    if (cnt_list[i] < 0.5): cnt_list[i] = cnt_list[i] + 0.4

df_grouped['Count'] = cnt_list

print("Normalized Count DF: \n", df_grouped.head())
print(archive.separator)

# try and create map

m = folium.Map(tiles='cartodbpositron')

lats = []
lngs = []

for index in df_grouped.index:
    
    coords = json.loads(str(df_grouped['Coordinates'][index]))

    points = [(i[1], i[0]) for i in coords[0]]

    folium.PolyLine(points, color='red', weight=1, opacity=float(df_grouped['Count'][index])).add_to(m)

    df = pd.DataFrame(coords[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
    lats.append(df[['Lat', 'Lon']].min().values.tolist())
    lngs.append(df[['Lat', 'Lon']].max().values.tolist())

sw = min(lats)
ne = max(lngs)
m.fit_bounds([sw, ne])

m.save("map.html")