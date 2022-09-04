"""


This py file determines what clients see when they access website



"""


from django.shortcuts import render, redirect
import os
import folium
from ipware import get_client_ip
import urllib, urllib3, json
from folium.plugins import LocateControl, MarkerCluster
from folium.plugins import MousePosition, HeatMap
import mysql.connector
import openrouteservice
from openrouteservice import convert
import jinja2
import pandas as pd

# explicit import
from .models import *



# Create your views here.
def explore(request):

    shp_dir = os.path.join(os.getcwd(), 'media', 'shp')

    m = folium.Map(location=[2.095368, 107.834810], zoom_start=6, tiles='Stamen Terrain')
    LocateControl().add_to(m)
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_river = {'color': 'blue'}
    style_MY = {'color': 'green'}
    style_SG = {'color': 'blue'}
    style_IND = {'color': 'beige'}

    folium.GeoJson('https://gist.githubusercontent.com/heiswayi/81a169ab39dcf749c31a/raw/b2b3685f5205aee7c35f0b543201907660fac55e/malaysia.geojson', name='Malaysia',
                   style_function=lambda x:style_MY, ).add_to(m)

    folium.GeoJson('https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/0-country.geojson', name='Singapore',
                   style_function=lambda y:style_SG, ).add_to(m)

    folium.GeoJson('https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson', name='Indonesia',
                    style_function=lambda z: style_IND, ).add_to(m)


    # folium.GeoJson(os.path.join(shp_dir, 'basin.geojson'), name='basin',
    #                style_function=lambda x:style_basin).add_to(m)
    #
    # folium.GeoJson(os.path.join(shp_dir, 'rivers.geojson'), name='basin',
    #                style_function=lambda y:style_river).add_to(m)


    folium.LayerControl().add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}
    return render(request, 'geoApp/Explore.html', context)

# introduction
def about(request):
    return render(request, 'geoApp/About.html')

# Second page
def home(request):

    # connection = mysql.connector.connect(host='localhost',
    #                                      database='mymcd_scraped',
    #                                      user='root',
    #                                      password='REAPINGHOOK980921')
    #
    # sql_select_Query = "select * from mcdmalaysiascraped"
    # cursor = connection.cursor()
    # cursor.execute(sql_select_Query)
    #
    # # get all records
    # records = cursor.fetchall()
    # connection.close()
    # cursor.close()

    # sqlite3
    import sqlite3
    conn = sqlite3.connect('GrabEV.db')
    cursor2 = conn.cursor()


    # get all records
    sql_select_Query = "Select * from Electro"
    cursor2.execute(sql_select_Query)
    recordsElectro = cursor2.fetchall()

    sql_select_Query = "Select * from Shopping"
    cursor2.execute(sql_select_Query)
    recordsShopping = cursor2.fetchall()

    sql_select_Query = "Select * from Shell"
    cursor2.execute(sql_select_Query)
    recordsShell = cursor2.fetchall()

    sql_select_Query = "Select * from Petronas"
    cursor2.execute(sql_select_Query)
    recordsPetronas = cursor2.fetchall()

    sql_select_Query = "Select * from Paul"
    cursor2.execute(sql_select_Query)
    recordsPaul = cursor2.fetchall()

    sql_select_Query = "Select * from mcdmalaysiascraped"
    cursor2.execute(sql_select_Query)
    records = cursor2.fetchall()

    sql_select_Query = "Select * from Government"
    cursor2.execute(sql_select_Query)
    recordsGo = cursor2.fetchall()

    sql_select_Query = "Select * from heatmapweighted"
    cursor2.execute(sql_select_Query)
    recordsheatmap = cursor2.fetchall()


    cursor2.close()
    conn.close()




    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip="0.0.0.0"
    else:
        if is_routable:
            ip_type="Public"
        else:
            ip_type="Private"

    ip_address = '175.143.31.41'
    # ip_address = '192.168.0.184'

    # try:
    #     url = 'https://api.ipfind.com/?ip=' + client_ip
    #     response = urllib.request.urlopen(url)
    #     data1 = json.loads(response.read())
    #     longitude=data1["longitude"]
    #     latitude=data1["latitude"]
    # except:
    #     url = 'https://api.ipfind.com/?ip=' + ip_address
    #     response = urllib.request.urlopen(url)
    #     data1 = json.loads(response.read())
    #     longitude=data1["longitude"]
    #     latitude=data1["latitude"]

    # place all markers

    df = pd.DataFrame(records, columns=['locations', 'lat', 'lng'])
    df = df.iloc[1:, :]

    df2 = pd.DataFrame(recordsElectro, columns=['locations', 'lat', 'lng'])
    df2 = df2.iloc[1:, :]

    df3 = pd.DataFrame(recordsShell, columns=['locations', 'lat', 'lng'])
    df3 = df3.iloc[1:, :]

    df4 = pd.DataFrame(recordsPetronas, columns=['locations', 'lat', 'lng'])
    df4 = df4.iloc[1:, :]

    df5 = pd.DataFrame(recordsPaul, columns=['locations', 'lat', 'lng'])
    df5 = df5.iloc[1:, :]

    df6 = pd.DataFrame(recordsShopping, columns=['locations', 'lat', 'lng'])
    df6 = df6.iloc[1:, :]

    df7 = pd.DataFrame(recordsGo, columns=['locations', 'lat', 'lng'])
    df7 = df7.iloc[1:, :]

    df8 = pd.DataFrame(recordsheatmap, columns=['locations', 'lat', 'lng', 'weight'])
    df8 = df8.iloc[1:, :]

    # for row in records:
    #     df.append(row)
    # print(df)
    dfh2 = df8.iloc[:, 1:3]
    dfh2 = dfh2.astype(float)
    print(dfh2)
    dfh = df8.iloc[:, 1:4]
    dfh = dfh.astype(float)
    print(dfh)

    # df2 = pd.DataFrame()
    # csv_file = os.path.join(os.path.dirname(__file__), 'latlng.csv')
    #
    # with open(csv_file, "r") as f:
    #     df2 = df2.append(pd.read_csv(f), ignore_index=True)
    #     df2 = df2.dropna()

    map_center = [df["lat"].mean(), df["lng"].mean()]
    m = folium.Map(location=map_center, zoom_start=5, )
    # m = folium.Map(location=[latitude,longitude],zoom_start=5,)

    LocateControl(auto_start=True, zoom_start=5,
                  strings={'title': 'See you current location', 'popup': 'Your position'}).add_to(m)


    MousePosition().add_to(m)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

    MousePosition(
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=False,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)


    # same directory files
    files = os.path.join(os.path.dirname(__file__), '')



    markerClusterMcd = MarkerCluster(name="Mcd", show=False).add_to(m)
    markerClusterShopping = MarkerCluster(name="Shopping malls", show=False).add_to(m)
    markerClusterGo = MarkerCluster(name="Government agencies", show=False).add_to(m)

    fg = folium.FeatureGroup(name='EV Stations (ElectroMaps)', show=True)
    fg2 = folium.FeatureGroup(name='EV Stations (Shell)', show=True)
    fg3 = folium.FeatureGroup(name='EV Stations (Petronas)', show=True)
    fg4 = folium.FeatureGroup(name='EV Stations (Third party media)', show=True)
    # fg5 = folium.FeatureGroup(name='Prominent cities', show=False)
    m.add_child(fg)
    m.add_child(fg2)
    m.add_child(fg3)
    m.add_child(fg4)
    # m.add_child(fg5)

    # for i in df:
    #     # iframe = folium.IFrame(f'<input type="text" value="{i[1]}, {i[2]}" id="myInput"><br><button onclick="myFunction()">Copy location</button>'
    #     # + '<br>' + 'Address:' + str(i[0]) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
    #     #         i[1]) + '<br>' + 'Longitude: ' + str(i[2]) + '<br>')
    #     # popup = folium.Popup(iframe, min_width=300, max_width=300)
    #     folium.Marker(location=(i[1], i[2]),
    #                   popup = f'<br>Address: <br>{i[0]}<br>Name: McDonald<br>Latitude & Longitude:'
    #                           f'<input type="text" value="{i[1]}, {i[2]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
    #                   min_width=300, max_width=300,).add_to(markerCluster)

    for i, row in df[["locations","lat", "lng"]].dropna().iterrows():
        icon = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsMGaR6_5NuBpKQ6FlrxLUUHf-nTrm8UK42w&usqp=CAU"
        icon = folium.CustomIcon(icon, icon_size=(20, 20))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: McDonald<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(markerClusterMcd)

    for i, row in df6[["locations","lat", "lng"]].dropna().iterrows():
        icon = "https://w7.pngwing.com/pngs/1022/32/png-transparent-shopping-cart-icon-shopping-cart-logo-icon-shopping-cart-label-coffee-shop-shopping-mall-thumbnail.png"
        icon = folium.CustomIcon(icon, icon_size=(20, 20))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: Shopping Malls<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(markerClusterShopping)

    for i, row in df7[["locations","lat", "lng"]].dropna().iterrows():
        icon = "https://www.malaysia.gov.my/media/uploads/c9558a31-7723-4558-9fee-f69baca119ff.png"
        icon = folium.CustomIcon(icon, icon_size=(20, 20))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: Government agencies<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(markerClusterGo)


    for i, row in df2[["locations","lat", "lng"]].dropna().iterrows():
        icon = "https://play-lh.googleusercontent.com/7xluZNpeebETJ1er8t2Fd7CY_oah6rFtPUJv28uxp3W7X0FLh-rwCdWkNa2aVEMuuhQ"
        icon = folium.CustomIcon(icon, icon_size=(20, 20))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: EV stations<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(fg)


    for i, row in df3[["locations","lat", "lng"]].dropna().iterrows():
        icon = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRy9QDJhzwiQOWmxnU88NomgAKPJ2vF4min-JP0eJhJ1HhRGoUWFi99tJ4yH6ujbAjEMsk&usqp=CAU"
        icon = folium.CustomIcon(icon, icon_size=(20, 20))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: Shell EV stations<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(fg2)


    for i, row in df4[["locations","lat", "lng"]].dropna().iterrows():
        icon = "https://redhaholdings.com.my/v2/wp-content/uploads/2018/06/petronas-png-petronas-800.png"
        icon = folium.CustomIcon(icon, icon_size=(30, 25))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: Petronas EV stations<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(fg3)


    for i, row in df5[["locations","lat", "lng"]].dropna().iterrows():
        icon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALUAAAC0CAMAAADl0Z0+AAAAY1BMVEUAAAD////tHCRAQEC/v7+AgIAQEBA7Bwl3DhLv7+8wMDDf398gICBgYGCfn5/Pz8" \
               "+yFRuvr69QUFCPj49wcHAPAgKUEhcsBQceBAXPGSBZCw7eGiJKCQvBFx2FEBSjExloDBCjf0I6AAAM3UlEQVR4nO2dDZeqLBCAMYEUFTPtc6vd//8r35kB1KxNpWx9z23OPbdSPh6HYRh" \
               "AXcY+8pGPfOQjH/nIRz7yUpHhe+V5YlXxOHi3JEWVPqHkKnk7sROeeTKL92u5LYkPd/h3enbCR9tJ2eQV67d2xqzkrup4nLplbvMV67GX+wqRmatfj8llMxVPdOUn" \
               "JczHYlvo5AWe8wmp4nHYxq64nJJpgCijPDEsdTnaoiYS2+aDulY4F2iHHQ9pdPLTfHKiQSLjgRrMBl/eO8Q0vOpNlww2pbdIOUjZ2YzsA8XYSN+4QV7vbx31tQgEKh+nSWemaqvs5" \
               "HEaMhDP0HYi0f0mQknm4kCMrPsViW49fxPOQJH9hj3A9O/LcrnceEH1S97X1eSIcOVaFovF0g+qV3hfdwy9h5gJqcn3PUoQenvr/zP15rjd+aE9kMmpV1No/F+g3i2RYPcTHff2yGYZRT/" \
               "GBPbL5d4dXO4M9XJ5Xix+jA/cn6LouGuVA1lP174RS7NJGJW2i46sTrmpKxhHDYpjp8MCZYUFLFf0fXHAmqLFIrIVwmlDvXCyPJpsJl9Tztexxby1SahxoLTNigqKvihltKwrGE19dBxf" \
               "QIrVHM72x2NqTHVG0AOo9wJJ3Zkae2fg3LHFYos6WbGtS7nyp/5afO/YHus8M3ZaneDo/mxUcoe6sZAfciX4M6Kki8VlR/r+skayAd4zaHn/bToEgW6jI6aNwDwojxc1Frilb8e2lrDC" \
               "zV3qm94Ipw6G+gd/7uHLyZy5mGYwtRwM9dGkMBX9+FJHVB4JtNt3nYjQBlHjUSrnXBdjM33V/Ai6Y1ZBP1QWycGf+mK/nqBtDWIURYdB1BtwIpGjjuoSv12er5YSIje0rpo23fpT12ZB" \
               "1e/rrtJL7fzNNfXJqbKlUzy9NeVTEyybw77UdXNjqUfs8efvaICFXMgLbLFZbjsuu2pG/L5y1PbjhdRogJeNO/6Q+oT9D5Oufqe+q+vFS3Rt85EdXpxHcdS2fx5vqc/WafxKfWo6OjqRyFG" \
               "37Prbn3prvwLxd22zW/xyajuGLnXd0L9ZyL5R6sb5EFuPbQP0r77UCxtJQBHHlXVWG+oyO1fvbnFNbUa6xcZS3qE+Rku2qvG2zl+7qzm6w/7UXwi6xIGMdLoxYyMCghrPcE2nrzY16Oq8o" \
               "XNbm2+x71Lj+LHHa/3e2Gjk1LQOduMttOTKe2zEUQb+rQ4m9EDFHdBOjP8/uTiibSEUihwo7Dh/nynpTcddUVIcbr9Wq686DjHUm7N1mF9P+OvTtw1lMHazodT2ZMq7mJ8X1qK2wY+LgaJ" \
               "77ubHGJ6NJhcHMrvG5ZmYb7tvRgsPz7eLVqvIdpw9ft/Vka/9ySi+disLx+1q+wM/L6vvnz1G4ZtuKL6JVmYwP2F+O64vl00ksKOivuv+6u+v3y8H7BIk/yPqY+PR50+" \
               "92RoFo2ty4838qUHF50t0obmQOzZ/6h8XKpI3NzKOGmLp/aPEk8juAuPDYXVpLQZNuB4yoXyo3yf/FLWS159M3r2wtN7yuXc69d7t8aTmZn9B1WfCu4XwuD5dNUeVlLihnMXeTeh" \
               "LnawN1WPqRtdFa8sqllXJWJn7G54vdZ5A864LPKPC1FKnIegwxHZXaSiEYinqFM/LkmXC3kioclasWailK1ZWIsPS6H/MDtkUHGQyw0NpJbo7LL7UIhGMJWEQyiTnwZqoi4THJStwwy" \
               "wug7LkTHBmzzMRC01baRUWSHucrlieC2gKnQieSzoI2XheCplzoTMVa8j7IuowSEWBdcA54EPqEPcv2TqBj1iQ4eP/5jzkcHl1lpr9K1csfSrciU2qmhqusKJkhcAu8CJqVugkZcZCNHcW" \
               "UsEHmHypw0CnhtqcR11bl5Gkmb6i5nhPJCWFy3PUwMqpbQIthO4g+lNLbLYgVEnCE6KWPOY5lCU0gisN1gLV2/PYCegOQkUGkrWpWZUniqjFNbVw1OJVFgIYEisuCqoFqCvooKjyNAipQV" \
               "WAKPY8wdHhdcFycydNq9iiIHMoizZ1QU0S39nsfILaVAxUaeKoZYFlFVwzibvClhrP44E1UZeVjF1m8ykRF64Vem7GoJfLxFBnMVyd1Fwy2blh6GlqlQQ84yyN84IHCZl3CD6jBH+ijYXQ" \
               "eZaDKyG7sGMM7c9TwTLgOfBlAeYAIBgLclNBAd/Bk8Q8rq6rf1kckob1+KywsVXY0U8Y/nZHhwwprzQJWgWZoQD+7w79U0RPhdfNAmNkAuo4n/wemH8qUv1j+VC/T/yoJQ/i5256V0/dQup" \
               "HncEw+ChT+vA20lDgQyzPXLUfNQUWdlRg3eGEuZmNS4Djhv1OaUXn9rDWKGIenko7A5LqDlBe1HiLF7cjcKApoJQ6DhJFA3EYmEJdgjJP4irJwSRUnCe5pNwQC+SYryhlnnBjLgKnFXBFGob" \
               "wEgIpjGQwhCzh9/U9h966TqFECYW5aSxEzxAoGWob+tkEQB7DGK8LDPoZ10bXQYihvgxSjUFhYlgU5Ewzih3XMEvI8KrzNV7TtUF6U1d4P6Uu2uGmDTAtdTsBHhacpivAaqkZXFJVsLgKaTLB" \
               "3PFChyFM7SD+y7NYpjFLbh538aZuR/HMWEhwRd1OYKhtQFhTwydMH4Kcc17P1+A4TCJAFASvCUsymPekRaBfpGuRX1HrPO3oup3AUcsr6jTAOWZTuKM2wZcKYAZTFfQolMyvnZI3tcJpdl65Sr" \
               "FLgsYKipCJup3AUKNJ4HTFUcOk3s1YZIuaZjU49YUhQdobeztux9/ztVYCGE7OeQ5z1SwotY5Bi7pIWwksdRaXmuJ/M7tnpHwVc2HmtZYanIrQuZnZMw3TolyUnWmYHzWtzjSrLnQopDkKHM" \
               "TFvzUuvDQJVGryKLOSUwll8pE/q1dpqFT07bR4AyXCT0Vlig7AvxSH/LX0Uqt6+WJGovuoaS49+URwpJig4JHgYx7Fm2iGStxLjdcVP0zxdlH97U+W3/+w2DuFFpMfzyrIiXg9xDGZ0DOO" \
               "PcsX8dxMhPTY19XIzVQ9id4pxRBnTI+vzeahTKvqnofXmH1UcD6WnQ8bQUjZs3mYlB4lTQY0PSWM5+H9ssEqlMlssA30sLHabAHNANt" \
               "AD7GPJnV3o+HdIvVI7Rlsj7eOvFDsW1fGNLnFps3PP5HQvvlknJ2u3Ttx8ur99h2W7u02ycjKlXtbCloK53eVHvIppFVxMX6Mrq5eQXTP/ehgUkm8hrrrVyfdtlU6LbP39FVmRV3K7dK6mA" \
               "451k+GFKHQ/P4bGrDLxBMYdvkiByDuKVvdb4H5CL2hoRt0U5Q1txWfKyHCTpSLHmpWc7UbuTPDkXM3EGZd8xUjTY3mtrjWEeOb2317hisnt0KQ7XUr8uR/hjNQzFt1WiF37/sxZiFZx0" \
               "bw13ym8r8KRbz1dMj/TSPvlTRum7b/m0beLPRaHef+ZrkXclfar8DL/jfUxtsZ7N4tnvmIfc0fYj9BrTJR8Pq9pwnnQvx6z+JLxGLn0pdaifq1ox3h5XoydIetfKjTsnmzbM5xrpFfT2+" \
               "TZ6cwv4nFjvlo6tDO5nJdmY3tpO7OMhSFnaPGepLYRraaeEQ2+17XIqvDXQzI2rFvPQ1Nnnkj86+iR1PblzsnWZsy604q8qSa8pW52Tjq1KxQdJcKym70FQZFvVIWJOXLFa5srxpScGqb5i" \
               "ZmyW+mQhpnGTX36xfrpOlZ/WNjzXDT5PL2SrRZjFw3HSfmZfbKAZiWL/sKzBpPdxOKr2/zJ/bdgM3Skc37ui05VPfDSDW8fld59zQGNRm98FoY0dQs6MFv3hf+yvX/dffRJyfofm9qNmilW2" \
               "Dqnn4oL43j7z3mmGZl3o8xUqadfawnIJ6YOisme+f+VNRpOeWfCZiIOuuv+RmZ5p6maXcNgomUXfbX+5xMsnbbds6xpofUsnEe2Uki6OHfmz8AMkHQ3TYQnqYCBhGIo9ce/bOUoYbccOGdTZ" \
               "8JVgOqpnRdW0u8VqOxs3rKwdPrDj4BdaMX3t6DzNRIaJE21xmrqn3q9dAt6hS/JlUYErwat7eXmHXaLKQ+kbNWz5jC9dUBscag2Tw6iObB5SjqDI3ChHf4LWvF2VMsctW9cV01uzdYZ9qNlB8" \
               "Kxr5OqRqV3VzPBND2RjBbb72mjQsHY0yEKJ1SsUu4vwcy1SKJa0usp66CY0w9gpojdV0kfi+4yKbc+UlNiEqkLer1aGo3f5bBm9Y+1VqgC3ETRDR21b0XI29tlxeiJeswVGho7pqzITdMvow8" \
               "qLsOx3rVqD9KVtZ3DKEHeuMOLHYgfDFEyoPxXR8HGXreLouDYYstLxIzuuWef+3F/L0Vc2PHW7eNm+DDZxWjCT7evNdt7zvK/apVZlwq/mCrW/3+loUB8pK/KviRj3zkIx+ZhfwHm6ySMUsBcHAAAAAASUVORK5CYII="
        icon = folium.CustomIcon(icon, icon_size=(20, 20))
        position = (row["lat"], row["lng"])
        location = row["locations"]
        # iframe = folium.IFrame(
        #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
        #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
        # popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: EV stations (Based on PaulTan.org)<br>Latitude & Longitude:'
                                                    f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
                                                min_width=300, max_width=300, icon=icon ).add_to(fg4)

    # for i, row in df8[["locations","lat", "lng"]].dropna().iterrows():
    #     # icon = "https://redhaholdings.com.my/v2/wp-content/uploads/2018/06/petronas-png-petronas-800.png"
    #     # icon = folium.CustomIcon(icon, icon_size=(30, 25))
    #     position = (row["lat"], row["lng"])
    #     location = row["locations"]
    #     # iframe = folium.IFrame(
    #     #     'Address:' + str(location) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
    #     #         row["lat"]) + '<br>' + 'Longitude: ' + str(row["lng"]))
    #     # popup = folium.Popup(iframe, min_width=300, max_width=300)
    #     folium.Marker(location=(position), popup = f'Address: <br>{str(location)}<br><br>Name: Prominent cities<br>Latitude & Longitude:'
    #                                                 f'<input type="text" value="{row["lat"]}, {row["lng"]}" id="myInput"><button onclick="myFunction()">Copy location</button><br>',
    #                                             min_width=300, max_width=300, ).add_to(fg5)


    el = folium.MacroElement().add_to(m)
    el._template = jinja2.Template("""
        {% macro script(this, kwargs) %}
        function myFunction() {
          /* Get the text field */
          var copyText = document.getElementById("myInput");

          /* Select the text field */
          copyText.select();
          copyText.setSelectionRange(0, 99999); /* For mobile devices */

          /* Copy the text inside the text field */
          document.execCommand("copy");
        }
        {% endmacro %}
    """)


    folium.plugins.HeatMap(dfh, name="Economic areas", show=True, blur=25, max_zoom=17, gradient={0.1: 'blue', 0.3: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'}).add_to(m)

    # f.close()

    folium.LayerControl().add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}
    return render(request, 'geoApp/home.html', context)



def route(request):

    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip="0.0.0.0"
    else:
        if is_routable:
            ip_type="Public"
        else:
            ip_type="Private"

    ip_address = '175.143.31.41'
    # ip_address = '192.168.0.184'

    try:
        url = 'https://api.ipfind.com/?ip=' + client_ip
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]
    except:
        url = 'https://api.ipfind.com/?ip=' + ip_address
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]


    m = folium.Map(location=[latitude,longitude],zoom_start=7,)

    MousePosition().add_to(m)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

    MousePosition(
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=False,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)


    """ - setup openrouteservice client with api key, you can signup https://openrouteservice.org 
          if you don't have API key. Its totaly free😊
        - After signup, you can see your API key available under the dashboard tab.
    """
    client = openrouteservice.Client(key='5b3ce3597851110001cf624886badbf0420c486989b5fea743c4be17')

    # set location coordinates in longitude,latitude order
    coords = ((longitude, latitude), (103.8010235, 1.5825705))

    res = client.directions(coords)

    # call API
    res = client.directions(coords)

    # m = folium.Map(location=[6.074834613830474, 80.25749815575348], zoom_start=10, control_scale=True,
    #                tiles="cartodbpositron")

    LocateControl(auto_start=False, zoom_start=10,
                  strings={'title': 'See you current location', 'popup': 'Your position'}).add_to(m)

    """
     - Add the GoeJson overlay using folium.Geojson method. This will add route in to our map
    """

    geometry = client.directions(coords)['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)
    print(decoded)

    folium.GeoJson(decoded).add_to(m)


    folium.LayerControl().add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}
    return render(request, 'geoApp/route.html', context)