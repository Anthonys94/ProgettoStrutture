import pymongo
from pymongo import MongoClient

class DBConnectionManager:
    # private attriute
    __instance = None
    __dbname = 'localhost'
    __dbport = 27017


    @staticmethod
    def getInstance():
        """ Static access method. """
        if DBConnectionManager.__instance == None:
            DBConnectionManager()
        return DBConnectionManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DBConnectionManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DBConnectionManager.__instance = self


    def addCertificato(self, certificatiJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db =  client.Strutture
        db.certificato.insert_one(certificatiJSON)
        client.close()

    def addMateriale(self, MaterialeJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.materiale.insert_one(MaterialeJSON)
        client.close()

    def addProva(self, ProvaJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.prova.insert_one(ProvaJSON)
        client.close()

    def addStruttura(self, StrutturaJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.struttura.insert_one(StrutturaJSON)
        client.close()