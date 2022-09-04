# import osmnx as ox
# import networkx as nx
#
# ox.config(log_console=True, use_cache=True)
#
# G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
#                              network_type='walk')
#
# orig_node = ox.get_nearest_node(G_walk,
#                                 (40.748441, -73.985664))
#
# dest_node = ox.get_nearest_node(G_walk,
#                                 (40.748441, -73.4))
#
# route = nx.shortest_path(G_walk,
#                          orig_node,
#                          dest_node,
#                          weight='length')
#
# route_map = ox.plot_route_folium(G_walk, route)
#
# route_map.save('route.html')

import openrouteservice
from openrouteservice import convert
import folium
from folium.plugins import LocateControl
import jinja2
import json
""" - setup openrouteservice client with api key, you can signup https://openrouteservice.org 
      if you don't have API key. Its totaly free😊
    - After signup, you can see your API key available under the dashboard tab.
"""
client = openrouteservice.Client(key='5b3ce3597851110001cf624886badbf0420c486989b5fea743c4be17')

#set location coordinates in longitude,latitude order
coords = ((80.21787585263182,6.025423265401452),(80.23929481745174,6.019639381180123))


res = client.directions(coords)

#call API
res = client.directions(coords)


#test our response
# with(open('test.json','+w')) as f:
#  f.write(json.dumps(res,indent=4, sort_keys=True))

geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)
print(decoded)



# Initialize the Map instance
m = folium.Map(location=[6.074834613830474, 80.25749815575348],zoom_start=10, control_scale=True,tiles="cartodbpositron")
"""
 - Add the GoeJson overlay using folium.Geojson method. This will add route in to our map
"""


folium.GeoJson(decoded).add_to(m)

LocateControl(auto_start=False, zoom_start=5,
                  strings={'title': 'See you current location', 'popup': 'Your position'}).add_to(m)


"""
   Save map and open it. Alternatively, if you are in Jupyter notebook 
   you can simply render the map as cell normal output.
"""


for location in coords:
    folium.Marker(
        location=(6.025423265401452,80.21787585263182),
        popup = f'<input type="text" value="{location[0]}, {location[1]}" id="myInput"><button onclick="myFunction()">Copy location</button>'
    ).add_to(m)

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

m.save('map.html')