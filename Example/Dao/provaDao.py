from pymongo import MongoClient

client = MongoClient('localhost', 27017 )
db =  client.Strutture

x = db.struttura.find()
for element in x:
    print(element)
