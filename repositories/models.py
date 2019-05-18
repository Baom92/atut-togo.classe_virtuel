from pymongo import MongoClient
import traceback

class Recette():
    def __init__(self, _id, nom, nombre_personnes, temps_preparation, temps_cuisson, temps_total,
                 ingredients, etapes_preparation):
        self._id = _id
        self.nom = nom
        self.nombre_personnes = nombre_personnes
        self.temps_preparation = temps_preparation
        self.temps_cuisson = temps_cuisson
        self.temps_total = temps_total
        self.ingredients = ingredients
        self.etapes_preparation = etapes_preparation


class Etape():
    def __init__(self, numero, description):
        self.numero = numero
        self.description = description

def mongoConnection(mongo_url, mongo_database, collection):
    try:
        url = "mongodb://" + mongo_url + ":27017"
        conn = MongoClient(url)

        # database
        db = conn[mongo_database]

        # Created or Switched to the given collection
        return db[collection]
    except Exception:
        print(traceback.format_exc())
        return None
