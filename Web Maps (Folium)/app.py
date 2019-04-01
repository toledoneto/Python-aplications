import folium
import pandas as pd

# função para dar cores diferentes para elevações diferente
def color_producer(elevation):
	if elevation < 1000:
		return 'green'
	elif 1000<= elevation < 3000:
		return 'orange'
	else:
		return 'red'

df = pd.read_csv("Volcanoes_USA.txt")
lat = list(df["LAT"])
lon = list(df["LON"])
elevation = list(df["ELEV"])

# criando a base do mapa
maps = folium.Map(location=[38.58, -99.09], zoom_start = 6)

# primeira camada, vulcões nos EUA
fg_volcanoes = folium.FeatureGroup(name = "Volcanoes USA Markers")

# para ícone tipo "gota" padrão
# for lt, ln, el in zip(lat, lon, elevation):
# 	fg.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(str(el) + " m", parse_html = True), 
# 								icon = folium.Icon(color = color_producer())))

# para ícone circular
for lt, ln, el in zip(lat, lon, elevation):
	fg_volcanoes.add_child(folium.CircleMarker(location = [lt, ln], popup = folium.Popup(str(el) + " m", parse_html = True), 
				fill_color = color_producer(el), radius = 6, fill_opacity = 0.7, fill = True))

# segunda camada , dados de população com GeoJson
fg_population = folium.FeatureGroup(name = "Country Population in 2005")
fg_population.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
							style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
													else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
													else 'red'}))

maps.add_child(fg_volcanoes)
maps.add_child(fg_population)

maps.add_child(folium.LayerControl())

maps.save("Map1.html")