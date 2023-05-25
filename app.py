from flask import Flask
import requests

app = Flask(__name__)

format = "&format=json"
baseURLlat = "https://nominatim.openstreetmap.org/search?q="
timeZone = "&forecast_days=2&daily=temperature_2m_max&timezone=PST"
baseUrlFor = "https://api.open-meteo.com/v1/forecast?"
basePlaces = "https://api.openstreetmap.org/api/0.6/map.json?bbox="

def getPlaces(lat1, lon1, lat2, lon2):
    URL = basePlaces + str(lon1) + "," + str(lat1) + "," + str(lon2) + "," + str(lat2)
    response = requests.get(URL).json()
    elements = response["elements"]
    cont = 0
    result = []
    for e in elements:
        if cont == 4:
            break
        if 'tags' in e:
            tags = e['tags']
            for key in tags:
                if 'amenity' in key:
                    if tags[key]=='restaurant':
                        result.append(( tags["name"]))
                        cont = cont + 1
    return result


def getCoords(place):
    URL = baseURLlat + place + format
    response = requests.get(URL).json()
    return (response[0]['lat'], response[0]['lon'])

def getForecast(lat, lon):
    latitude = "latitude="+lat
    longitude = "longitude="+lon
    URL = baseUrlFor + latitude + "&" + longitude + timeZone
    response = requests.get(URL).json()
    a = response["daily"]["time"][1]
    b = response["daily"]["temperature_2m_max"][1]
    return (a, b)

@app.route('/info/<path:place>')
def getResults(place):
    coords = getCoords(place)
    temp = getForecast(coords[0], coords[1])
    places = getPlaces(float(coords[0])-0.01, float(coords[1])-0.01, float(coords[0])+0.01, float(coords[1])+0.01)
    res = {
        'coordenadas' : coords,
        'clima': temp,
        'lugares': places
    }
    return res

if __name__ == '__main__':
    app.run()