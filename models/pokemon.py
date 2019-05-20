from models.database import Database
import random
import requests

class Pokemon(object):

    def __init__(self):
        db = Database()
        self.db = db
        self.pokeapi = 'https://pokeapi.co/api/v2/'

    def getPokemonApi(self):
        number = str(random.randint(1, 151))
        url = "{}pokemon/{}".format(self.pokeapi, number)
        return requests.get(url).json()

    def getPokemonUser(self, entrenador):
        return self.db.db["entrenadores"].find_one({"name": entrenador}, {"pokemons": 1})

    def train(self, entrenador):
        poke = self.getPokemonUser(entrenador)
        total = {}
        for x in poke["pokemons"]:
            total.update({"pokemons."+x+".experience": 1})
        self.db.db["entrenadores"].update_many({"name": entrenador}, {"$inc": total})
        return {"status": 200, "message": "Your pokemons are now more strong"}
