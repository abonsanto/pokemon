from models.database import Database
from models.pokemon import Pokemon


class Entrenador(object):

    def __init__(self):
        db = Database()
        self.db = db

    def createEntrenador(self, form):
        try:
            params = {"name": form["name"], "pokemons": form["pokemons"]}
        except Exception as e:
            return {"status": 400,
                    "message": "Bad request, invalid parameters"}
        insert = {}
        insert["pokemons"] = {}
        poke = Pokemon()
        for x in range(1, int(params["pokemons"])):
            pokemon = poke.getPokemonApi()
            insert["pokemons"][str(pokemon["id"])] = {}
            insert["pokemons"][str(pokemon["id"])]["name"] = pokemon["name"]
            insert["pokemons"][str(pokemon["id"])]["experience"] = pokemon["base_experience"]
        insert["name"] = params["name"]
        save = self.db.db["entrenadores"].insert_one(insert)
        return {"status": 200,
                "message": "Coach and pokemons created",
                "id": str(save.inserted_id)}



    def _messageBattle(self, pokeGanador, ganador, pokePerdedor, perdedor):
        return "The pokemon {} of coach {} has won the battle to the pokemon {} of coach {}" \
                .format(pokeGanador,
                        ganador,
                        pokePerdedor,
                        perdedor)

    def battle(self, fighterName, opponentName):
        fighter = self.db.db["entrenadores"].find_one({"name": fighterName})
        opponent = self.db.db["entrenadores"].find_one({"name": opponentName})
        if fighter and opponent:
            fpoke = fighter["pokemons"]
            opoke = opponent["pokemons"]
            result = []
            for pokeA in fpoke:
                if "lose" in fpoke[pokeA]:
                    continue
                for pokeB in opoke:
                    if "lose" in opoke[pokeB]:
                        continue
                    if fpoke[pokeA]["experience"] > opoke[pokeB]["experience"]:
                        fpoke[pokeA]["experience"] = fpoke[pokeA]["experience"] + 1
                        opoke[pokeB]["lose"] = 1
                        winner = fighter["name"]
                        result.append(self._messageBattle(fpoke[pokeA]["name"],
                                                          fighter["name"],
                                                          opoke[pokeB]["name"],
                                                          opponent["name"]))
                    else:
                        winner = opponent["name"]
                        result.append(self._messageBattle(opoke[pokeB]["name"],
                                                          opponent["name"],
                                                          fpoke[pokeA]["name"],
                                                          fighter["name"]))
                        opoke[pokeB]["experience"] = opoke[pokeB]["experience"] + 1
                        fpoke[pokeA]["lose"] = 1
                        break
            self.updateBattle(fighterName, fpoke)
            self.updateBattle(opponentName, opoke)
            return {"status": 200, "battle": result}
        else:
            return {"status": 500, "message": "An error has occurred with the fighters"}

    def updateBattle(self, fighter, poke):
        poke = self._removeKeys(poke)
        self.db.db["entrenadores"].update_one({"name": fighter}, {"$set": {"pokemons": poke}})
        self.db.db["entrenadores"].update_many({"name": entrenador}, {"$inc": total})
        

    def _removeKeys(self, pokemon, keys='lose'):
        for x in pokemon:
            pokemon[x].pop(keys, None)
        return pokemon
