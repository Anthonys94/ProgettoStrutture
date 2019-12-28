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

    def Login(self, username, password):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.Utente.find({"_id":username, "password": password })
        client.close()
        return cnt

    def addDocumento(self, certificatiJSON, file, filename):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)
        certificatiJSON['filename'] = filename
        with grid_fs.new_file(filename=filename) as fp:
            fp.write(file)
            file_id = fp._id
        certificatiJSON['file_id'] = file_id
        db.documento.insert_one(certificatiJSON)
        client.close()
        return True

        '''
        try:
            db.documento.insert_one(certificatiJSON)
            client.close()
            return True
        except:
            client.close()
            return False
        '''
    def addCertificato(self, certificatiJSON, file, filename):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)    
        certificatiJSON['filename'] = filename
        with grid_fs.new_file(filename=filename) as fp:
            fp.write(file)
            file_id = fp._id
        certificatiJSON['file_id'] = file_id
        try:
            db.certificato.insert_one(certificatiJSON)
            client.close()
            return True
        except:
            client.close()
            return False

    def addMateriale(self, MaterialeJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture

        if db.materiale.find({"_id": MaterialeJSON['_id']}).count() == 0:
            db.materiale.insert_one(MaterialeJSON)
        else:
            db.materiale.update_one({"_id": MaterialeJSON['_id']}, {"$set": {"descrizione": MaterialeJSON['descrizione']}})

        client.close()
        return True


    def addProva(self, ProvaJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture

        if db.prova.find({"_id": ProvaJSON['_id']}).count() == 0:
            db.prova.insert_one(ProvaJSON)
        else:
            db.prova.update_one({"_id": ProvaJSON['_id']},{"$set": {"descrizione": ProvaJSON['descrizione']}})

        client.close()
        return True



    def addStruttura(self, StrutturaJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture

        if db.struttura.find({"_id": StrutturaJSON['_id']}).count() == 0:
            db.struttura.insert_one(StrutturaJSON)
        else:
            db.struttura.update_one({"_id": StrutturaJSON['_id']},{"$set": {"descrizione": StrutturaJSON['descrizione']}})

        client.close()
        return True


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

    def getProvince(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        province = db.comune.distinct("Provincia")
        client.close()
        return province

    def getComuni(self, provincia):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        comune = db.comune.find({"Provincia": provincia}, {"Comune": 1, "_id": 0})
        client.close()
        return comune

    def addUtente(self, UtenteJson):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.Utente.insert_one(UtenteJson)
            client.close()
            return True
        except:
            client.close()
            return False

    def getUtenti(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        utenti = db.Utente.find()
        client.close()
        return utenti

    def checkUtente(self, CF):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.Utente.find({"_id": CF}).count()
        client.close()
        return cnt

    def checkUtenteInattivo(self, CF):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.Utente.find({"_id": CF}, {"dataInserimento":1})
        client.close()
        return cnt

    def updateUtente(self, cf, ruolo, data):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.Utente.update_one({"_id": cf}, { "$set": { "ruolo": ruolo, "dataInserimento": data}})
        client.close()

    def findOldRuolo(self, CF):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        oldRuolo = db.Utente.find({"_id": CF}, {"_id":0 ,"ruolo": 1})[0]['ruolo']
        client.close()
        return oldRuolo

    def riattivaUtente(self, cf, ruolo, data):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.Utente.update_one({"_id": cf}, {"$set": {"ruolo": ruolo, "dataInserimento": data}})
        user = db.Utente.find({"_id": cf})
        client.close()
        return user

    def DoQuerybyPratica(self, numeroPratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        num = db.documento.find({"_id": numeroPratica})
        client.close()
        return num

    def DoQueryOnDocument(self, jsonElement):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        doc = db.documento.find(jsonElement)
        client.close()
        return doc

    def DoQueryOnCertificato(self, jsonElement ):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        doc = db.certificato.find(jsonElement)
        client.close()
        return doc

    def DeleteDocument(self, pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        #fai il check se esiste
        documento = db.documento.find({"_id": pratica})
        if documento.count() > 0:
           filename = []
           filename.append(documento[0]['filename'])
           cursor = db.certificato.find({"_id.NumeroPratica": pratica}, {"_id":0 ,"filename": 1})
           for element in cursor:
               filename.append(element['filename'])
            #quindi filename contiene la lista dei file
           oggetti = db.fs.files.find({"filename":{"$in":filename}},{"_id":1})
           obj = []
           for o in oggetti:
               obj.append(o['_id'])

            #cancello i chunk
           db.fs.chunks.remove({"files_id":{"$in":obj}})
           #cancello i files
           db.fs.files.remove({"filename": {"$in": filename}})
           #cancello i certificati
           db.certificato.remove({"_id.NumeroPratica": pratica})
           #cancello i documenti
           db.documento.remove({"_id": pratica})
           client.close()
           return True
        else:
            client.close()
            return False
        #prendi i filename ni documenti

        # prendi i filename nei certificato
        #per ogni file:
        #vai in fs.files e prendi gli id, elimina quell'id in fs.chunck


