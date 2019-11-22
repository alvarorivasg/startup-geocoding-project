import requests
import os
import time
from dotenv import load_dotenv
import geocoder
load_dotenv()


def locRequest(direction):
    '''extrae un par de coordenadas de la API de Google Places'''
    if not os.getenv("GOOGLE"):
        raise ValueError("No token")
    else:
        g = geocoder.google(direction, key=os.getenv("GOOGLE"))
        return g.latlng


def textSearch(query, lat=45.508888, lng=-73.561668, radius=15000, maxPages=5):
    '''extrae listas de coordenadas de la API de Google Places'''
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'location': f'{lat},{lng}',
        'radius': radius,
        'key': os.getenv("GOOGLE")
    }
    list_of_places = []
    nextPageToken = None
    while maxPages != 0:  # introducido por Marc. Sabiendo que la API de Google nunca retornará más de tres páginas, podría poner aquí un while true, ¿verdad?
        if nextPageToken:
            params["pagetoken"] = nextPageToken
        res = requests.get(url, params=params)
        if(res.status_code != 200):
            break
        else:
            nextPageToken = res.json().get('next_page_token', None)
            coordin = extractCoords(res.json()['results'])
            list_of_places.extend(coordin)
            maxPages -= 1
            if not nextPageToken:
                break
            time.sleep(2)
    return list_of_places


def extractCoords(results):
    '''Complementa la función textSearch. No sé si no debería haberlo hecho así.'''
    listademovidas = []
    for el in range(0, len(results)):
        location = results[el]['geometry']['location']
        listilla = [location['lat'], location['lng']]
        listademovidas.append(listilla)
    return listademovidas


def getAddress(listcoords):
    '''extrae una dirección a partir de un par de coordenadas'''
    if not os.getenv("GOOGLE"):
        raise ValueError("No token")
    else:
        g = geocoder.google(listcoords, method='reverse',
                            key=os.getenv("GOOGLE"))
        return g.json['address']
