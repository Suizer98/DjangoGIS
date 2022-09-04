import folium
from folium.plugins import HeatMap, LocateControl, MousePosition
import pandas as pd


import folium
from folium import plugins

# df = pd.read_csv("latlng2.csv")
# print(df)
#
# def simple_folium(df:pd.DataFrame, lat_col:str, lon_col:str, map_name:str):
#     """
#     Descrption
#     ----------
#         Returns a simple Folium HeatMap with Markers
#     ----------
#     Parameters
#     ----------
#         df : padnas DataFrame, required
#             The DataFrane with the data to map
#         lat_col : str, required
#             The name of the column with latitude
#         lon_col : str, required
#             The name of the column with longitude
#         test_cols: list, optional
#             A list with the names of the columns to print for each marker
#
#     """
#     #Preprocess
#     #Drop rows that do not have lat/lon
#     df = df[df[lat_col].notnull() & df[lon_col].notnull()]
#
#     # Convert lat/lon to (n, 2) nd-array format for heatmap
#     # Then send to list
#     df_locs = list(df[[lat_col, lon_col]].values)
#
#     #Set up folium map
#     fol_map = folium.Map([3, 105], zoom_start=4)
#
#     # plot heatmap
#     heat_map = plugins.HeatMap(df_locs, name=map_name)
#     fol_map.add_child(heat_map)
#
#     # plot markers
#     markers = plugins.MarkerCluster(locations = df_locs, name="Testing Site")
#     fol_map.add_child(markers)
#
#     #Add Layer Control
#     folium.LayerControl().add_to(fol_map)
#     fol_map.save("map.html")
#     return fol_map
#
# simple_folium(df, "lat", "lng", "Economic area")


import folium
from folium import plugins
import os

df = pd.DataFrame()
heatmap_map = folium.Map(location=[3, 105], zoom_start=3)

with open('latlng.csv', "r") as f:
    df = df.append(pd.read_csv(f),ignore_index = True)
    df = df.dropna()

hm = plugins.HeatMap(df, name="Economic")
heatmap_map.add_child(hm)

markers = folium.plugins.MarkerCluster(locations=df, name="markers")
heatmap_map.add_child(markers)

f.close()
folium.LayerControl().add_to(heatmap_map)
heatmap_map.save("heatmap.html")


