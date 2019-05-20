from models.database import Database
class Liga(object):

    def __init__(self):
        db = Database()
        self.db = db

    def createLiga(self, form):
        try:
            liga = {"name": form["name"], "ubication": form["ubication"]}
        except Exception as e:
            return {"status" : 400, "message": "Bad request, invalid parameters"}
        insert = self.db.db["ligas"].insert_one(liga)
        return {"status": 200, "message": "Pokemon league has been created", "id": str(insert.inserted_id)}
