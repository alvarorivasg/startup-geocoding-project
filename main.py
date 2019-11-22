from src.mongocompanies import connectCollection, extractBadCompanies, extractStartups, toMongo
from src.dataframe import infoForDataframe, puntuation, rankingLeader
from src.apiqueries import textSearch, locRequest, getAddress
import pymongo
import pandas as pd
import folium
from os import system


def main():
    _, companies = connectCollection('companies', 'companies')
    compan = list(companies.find({"offices.city": "Montreal", "founded_year": {
                  "$lt": 2008}, "offices.longitude": {"$ne": None}, "offices.latitude": {"$ne": None}}))
    db, startups = connectCollection('companies', 'startups')
    start = list(startups.find())
    old_companies = extractBadCompanies(compan)
    succ_startups = extractStartups(start, compan)
    schools = textSearch("primary school")
    starbucks = textSearch("starbucks")
    vegan_locations = textSearch("vegan restaurant")
    airport_coord = locRequest("airport montreal")
    try:
        db.collec.drop()
    except:
        pass
    db, collec = connectCollection('companies', 'collec')
    dicci = {'old_company': old_companies, 'startup': succ_startups,
             'school': schools, 'starbucks': starbucks, 'restaurant': vegan_locations}
    for v in dicci.items():
        for i in range(0, len(v[1])):
            toMongo(v[1][i], v[0], i, db, collec)
    db.collec.create_index([("location", pymongo.GEOSPHERE)])
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
