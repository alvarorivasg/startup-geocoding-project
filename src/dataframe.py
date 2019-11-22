from src.mongocompanies import generateGeoquery
from haversine import haversine

# refactorizable. Podría además devolver el df formado


def infoForDataframe(coords, collec, airport_coord):
    '''para nutrir de valores un dataframe con respecto a unas coordenadas'''
    numbucks = len(list(collec.find(generateGeoquery(
        "starbucks", coords[1], coords[0], 1000))))
    numschools = len(
        list(collec.find(generateGeoquery("school", coords[1], coords[0], 3000))))
    numoldcomp = len(list(collec.find(generateGeoquery(
        "old_company", coords[1], coords[0], 2000))))
    numups = len(list(collec.find(generateGeoquery(
        "startup", coords[1], coords[0], 1000))))
    airportdist = round(haversine(tuple(coords), tuple(airport_coord)), 2)
    return [coords, numbucks, numschools, numoldcomp, numups, airportdist]


def puntuation(i, dataframe):
    '''para poder generar un ranking entre las distintas posibles localizaciones'''
    if (dataframe.iloc[i]["NumStarbucks"] == 0) or (dataframe.iloc[i]["NumSchools"] == 0) or (dataframe.iloc[i]["NumStartups"] == 0) or (dataframe.iloc[i]["NumOldCompanies"] >= 5):
        score = 0
    else:
        score = ((dataframe.iloc[i]["NumStarbucks"])/100+dataframe.iloc[i]["NumSchools"]*3-dataframe.iloc[i]
                 ["NumOldCompanies"]*7+dataframe.iloc[i]["NumStartups"]*7)/dataframe.iloc[i]["DistToAirport"]
    return score


def rankingLeader(dataframe):
    punt = []
    for i in range(0, len(dataframe.index)):
        punt.append(puntuation(i, dataframe))
    dataframe["Score"] = punt
    dataframe = dataframe.sort_values(["Score"], ascending=False)
    return dataframe.iloc[0]["LocationCoords"]
