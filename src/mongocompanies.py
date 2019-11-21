from pymongo import MongoClient
from src.apiqueries import locRequest


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll


def extractBadCompanies(compan):
    '''Devuelve una lista con las empresas que tienen más de 10 años de antigüedad'''
    bad_companies = []
    for com in compan:
        for i in range(0, len(com['offices'])):
            coord = []
            coord.append(com['offices'][i]['latitude'])
            coord.append(com['offices'][i]['longitude'])
            bad_companies.append(coord)
    return [co for co in bad_companies if str(co[0])[:2] == "45"]


def extractStartups(start, compan):
    '''Devuelve una lista de Startups que han recaudado >1M$ sitas en MTL'''
    loc1 = []
    nombres_startups = [st['Name'].strip() for st in start]
    nombres_viejunas = [v['name'].strip() for v in compan]
    for name in nombres_startups:
        if name not in nombres_viejunas:
            crd = locRequest(name + "Montreal")
            loc1.append(crd)
    loc2 = [startup for startup in loc1 if startup != None and str(startup[0])[
        0:2] == '45']
    return loc2


def toMongo(coords, typ, i, db, collec):
    dicc = {
        'name': f"{typ} {i}",
        'type': f"{typ}",
        'location': {
            'type': 'Point',
            'coordinates': [coords[1], coords[0]]}
    }
    return db.collec.insert_one(dicc)


def generateGeoquery(typeLoc, lng, lat, radius):
    return {"type": typeLoc, "location":
            {"$near":
             {"$geometry":
              {"type": "Point", "coordinates":
               [lng, lat]},
              "$maxDistance": radius}}}
