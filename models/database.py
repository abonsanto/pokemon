from pymongo import MongoClient
class Database(object):

    def __init__(self):
        try: 
            mongoClient = MongoClient('172.17.0.2',27017)
            self.db = mongoClient.pokemon
        except:   
            print("Could not connect to MongoDB")
