from src.mongocompanies import connectCollection, extractBadCompanies, extractStartups, toMongo
from src.dataframe import infoForDataframe, puntuation, rankingLeader
from src.apiqueries import textSearch, locRequest, getAddress
import pymongo
import pandas as pd
import folium
from os import system


def main():
    # En primer lugar, extraigo las variables necesarias para obtener coordenadas de mis bases de datos
    _, companies = connectCollection('companies', 'companies')
    compan = list(companies.find({"offices.city": "Montreal", "founded_year": {
                  "$lt": 2008}, "offices.longitude": {"$ne": None}, "offices.latitude": {"$ne": None}}))
    db, startups = connectCollection('companies', 'startups')
    start = list(startups.find())
    # Genero listas de coordenadas para cada uno de los puntos de interés
    old_companies = extractBadCompanies(compan)
    succ_startups = extractStartups(start, compan)
    schools = textSearch("primary school")
    starbucks = textSearch("starbucks")
    vegan_locations = textSearch("vegan restaurant")
    airport_coord = locRequest("airport montreal")
    # genero una nueva colección Mongo en la que meto los puntos de interés
    try:
        db.collec.drop()
    except:
        pass
    db, collec = connectCollection('companies', 'collec')
    dicci = {'old_company': old_companies, 'startup': succ_startups,
             'school': schools, 'starbucks': starbucks, 'restaurant': vegan_locations}
    for tupl in dicci.items():
        for i in range(0, len(tupl[1])):
            toMongo(tupl[1][i], tupl[0], i, db, collec)
    db.collec.create_index([("location", pymongo.GEOSPHERE)])
    # genero, con datos extraídos de geoQueries, un dataframe sobre el que calcularé el punto idóneo para establecer la empresa
    dataframe = pd.DataFrame(columns=["LocationCoords", "NumStarbucks",
                                      "NumSchools", "NumOldCompanies", "NumStartups", "DistToAirport"])
    for i in range(0, len(vegan_locations)):
        values = infoForDataframe(vegan_locations[i], collec, airport_coord)
        dataframe.loc[i] = values
    def_loc = rankingLeader(dataframe)
    address = getAddress(def_loc)
    print("La localización más adecuada para los requisitos de la empresa es", address)
    def_map = folium.Map(location=[45.508888, -73.561668], zoom_start=14)
    folium.Marker(def_loc, radius=2, icon=folium.Icon(
        icon='home', color='green')).add_to(def_map)
    def_map.save('output/map.html')
    _ = system('open -a "Google Chrome" output/map.html')


if __name__ == '__main__':
    main()
