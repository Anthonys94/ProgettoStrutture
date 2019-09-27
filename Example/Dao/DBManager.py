import pymongo
from pymongo import MongoClient
from gridfs import GridFS

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


    def addCertificato(self, certificatiJSON, file, filename):

        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)

        certificatiJSON['filename'] = filename
        with grid_fs.new_file(filename=filename) as fp:
            fp.write(file)
            file_id = fp._id

        certificatiJSON['file_id'] = file_id

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

    def getStrutture(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        strutture = db.struttura.find()
        client.close()
        return strutture

    def getProva(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        prove = db.prova.find()
        client.close()
        return prove

    def getMateriale(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        materiale = db.materiale.find()
        client.close()
        return materiale