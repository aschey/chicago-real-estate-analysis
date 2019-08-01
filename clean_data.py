# Imports
#%%
import pandas as pd
import json
from pandas.io.json import json_normalize
from shapely.geometry import shape, Point

# Initialize
#%%
with open('./results-7-31-2019.json') as f:
    data = json_normalize(json.load(f))
    data = data[data['address'].str.contains('Chicago, IL')]

with open('./chicago_neighborhoods.geojson') as f:
    geo = json.load(f)

# Add neighborhoods
#%%
def get_neighborhood(lon, lat):
    hoods = [polygon['properties']['pri_neigh'] for polygon in polygons if polygon['geometry'].contains(Point(lon, lat))]
    return hoods[0] if len(hoods) > 0 else None

polygons = [{'geometry': shape(feature['geometry']), 'properties': feature['properties']} for feature in geo['features']]

data['neighborhood'] = data \
    .apply(lambda row: get_neighborhood(row['hdpData.homeInfo.longitude'], row['hdpData.homeInfo.latitude']), axis=1)

data = data[data['neighborhood'].notnull()]
data[['address', 'neighborhood']]

#%%
data.to_csv('results-7-31-2019-cleaned.csv')