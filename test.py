#%%
import folium
import json

m = folium.Map(location=[41.8844, -87.6293], tiles='Stamen Toner')
folium.GeoJson('./chicago_neighborhoods.geojson', name='geojson', tooltip=folium.features.GeoJsonTooltip(fields=['pri_neigh', 'sec_neigh'], localize=True)).add_to(m)
folium.LayerControl().add_to(m)
m.save('test.html')
m
#%%
