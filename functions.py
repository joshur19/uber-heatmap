#### Project name: uber aggregation
### File: functions.py 
## Function: cleaning up of main file, storage for all functions
# Creation Date // Last Updated: 28/05/2023 // 26/11/2023

#imports
import requests
import archive


# function with API call to calculate point-by-point route between two coords
def points(start_lat, start_lng, end_lat, end_lng):

    url = "https://route-and-directions.p.rapidapi.com/v1/routing"

    querystring = {"waypoints":f"{start_lat},{start_lng}|{end_lat},{end_lng}","mode":"drive"}
    headers = {
        "X-RapidAPI-Key": archive.API_KEY,
        "X-RapidAPI-Host": "route-and-directions.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response



# function to calculate the mean coordinates and add them to a final dataframe by comparing two with different columns
def mean_coords(df_address, df_coords):

    # define lists to be appended to final df later
    mean_begin_lats = []
    mean_begin_lngs = []
    mean_dropoff_lats = []
    mean_dropoff_lngs = []

    # loop through the df containing only the addresses + respective counts
    for ind in df_address.index:

        # remember the current route
        current_begin = df_address['Begin Trip Address'][ind]
        current_dropoff = df_address['Dropoff Address'][ind]

        # initialize empty lists for calculation of mean of coords for current route
        list_begin_lat = []
        list_begin_lng = []
        list_end_lat = []
        list_end_lng = []

        # loop through the other df and find all the corresponding routes
        for inner_ind in df_coords.index:

            # if route is found then add the coords to list for later calculation
            if((df_coords['Begin Trip Address'][inner_ind] == current_begin) and (df_coords['Dropoff Address'][inner_ind] == current_dropoff)):

                list_begin_lat.append(df_coords['Begin Trip Lat'][inner_ind])
                list_begin_lng.append(df_coords['Begin Trip Lng'][inner_ind])
                list_end_lat.append(df_coords['Dropoff Lat'][inner_ind])
                list_end_lng.append(df_coords['Dropoff Lng'][inner_ind])

        # calculate the mean of all coords found for the current route
        mean_begin_lat = sum(list_begin_lat)/len(list_begin_lat)
        mean_begin_lng = sum(list_begin_lng)/len(list_begin_lng)
        mean_dropoff_lat = sum(list_end_lat)/len(list_end_lat)
        mean_dropoff_lng = sum(list_end_lng)/len(list_end_lng)

        # add calculated means to the list
        mean_begin_lats.append(mean_begin_lat)
        mean_begin_lngs.append(mean_begin_lng)
        mean_dropoff_lats.append(mean_dropoff_lat)
        mean_dropoff_lngs.append(mean_dropoff_lng)

    # add the new columns to the address dataframe
    df_address['Begin Lat'] = mean_begin_lats
    df_address['Begin Lng'] = mean_begin_lngs
    df_address['Dropoff Lat'] = mean_dropoff_lats
    df_address['Dropoff Lng'] = mean_dropoff_lngs



# iterate through DF, get coords via API and append them to given DF
def get_coords(df):
    points_list = []

    for i in range(len(df)):

        print("{:.2f}".format(i*100/len(df)), '% complete')

        begin_lat = df['Begin Lat'].iloc[i]
        begin_lng = df['Begin Lng'].iloc[i]
        dropoff_lat = df['Dropoff Lat'].iloc[i]
        dropoff_lng = df['Dropoff Lng'].iloc[i]

        coords_response = points(begin_lat, begin_lng, dropoff_lat, dropoff_lng)

        coords_json = coords_response.json()

        points_list.append(coords_json['features'][0]['geometry']['coordinates'])

    df['Coordinates'] = points_list

    df.to_csv('with_coords.csv', index=False)