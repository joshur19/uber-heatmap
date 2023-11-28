# Generate Heatmap from Exported Uber Data

![Santo Domingo Uber Heatmap](/mapexamples/santodomingo.png)

Uber provides a csv file containing your full ride history via this link: https://myprivacy.uber.com/privacy/exploreyourdata

The goal of this small project is to extract the location data from this csv file and use it to visualize a heatmap of the ride history.
The following Medium article was a big inspiration for this project: https://python.plainenglish.io/how-to-build-route-heatmaps-in-python-ebac363471d7

Here's a list of fields the csv file contains: 
```City, Product Type, Trip or Order Status, Request Time, Begin Trip Time, Begin Trip Lat, Begin Trip Lng, Begin Trip Address, Dropoff Time, Dropoff Lat, Dropoff Lng, Dropoff Address, Distance (miles), Fare Amount, Fare Currency```

Most interesting to this project are the fields ```City```, ```Begin Trip Address```, ```Dropoff Address```, and the four fields storing the coordinates for both Begin and Dropoff Address. In a pandas DataFrame all unnecessary fields are removed and the Begin/Dropoff Addresses are used to count up the number of unique trips.

The core functionality of the program is provided by the [Route and Directions API](https://rapidapi.com/geoapify-gmbh-geoapify/api/route-and-directions/details) which calculates a list of coordinates between the starting and end points of a given uber trip. This list of coordinates is then interpolated by [Folium](https://python-visualization.github.io/folium/latest/index.html) resulting in the presented visualization.

The code is implemented in a way that anyone should be able to use it with their downloaded Uber data. The only changes that have to be configured are:
1. create an ```archive.py``` file containing a valid API key for the Route and Directions API
2. implement the variables ```CITY``` and ```FILENAME``` in the main ```uber_agg.py``` file to reflect the city the heatmap should focus on and the filename of the uber ride history .csv

Non-standard Python libraries used are limited to pandas and Folium.