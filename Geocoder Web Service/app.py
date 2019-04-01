from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import pandas as pd
from geopy.geocoders import GoogleV3
import folium

app=Flask(__name__)

def plot_map(latitude, longitude):

    # criando a base do mapa
    maps = folium.Map(location=[38.58, -99.09], zoom_start = 6)

    fg_markers = folium.FeatureGroup(name = "Custom Markers")

    # para ícone circular
    for lt, ln in zip(latitude, longitude):
        fg_markers.add_child(folium.CircleMarker(location = [lt, ln], popup = folium.Popup(parse_html = True), 
                    fill_color = "green", radius = 6, fill_opacity = 0.7, fill = True))

    maps.add_child(fg_markers)

    maps.save("Map1.html")

def geocoding(file):

    df = pd.read_csv(file.name)

    goo = GoogleV3()

    df["Address"] = df["Address"] + ", " + df['City'] + ", " + df['State']

    df["Coordinates"] = df["Address"].apply(goo.geocode)

    df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
    df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude if x != None else None)

    df = df.drop("Coordinates",1)
    plot_map(df["Latitude"], df["Longitude"])

    return df
    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    global file
    if request.method=='POST':
        file=request.files["file"]
        file.save(secure_filename("uploaded"+file.filename))
        with open("uploaded"+file.filename,"r") as f:
            df = geocoding(f)
            return render_template("index.html", btn="download.html", text=df.to_html())

@app.route("/download")
def download():
    return send_file("uploaded"+file.filename, attachment_filename="yourfile.csv", as_attachment=True)


if __name__ == '__main__':
    app.debug=True
    app.run()
