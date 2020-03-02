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

    def checkEsistenza(self,pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        if db.documento.find({"_id": pratica}).count() > 0:
            client.close()
            return True
        else:
            client.close()
            return False

    def checkEsistenzaStruttura(self, struttura):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        if db.struttura.find({"_id": struttura}).count()>0:
            client.close()
            return True
        else:
            client.close()
            return False

    def checkEsistenzaProva(self, prova):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        if  db.prova.find({"_id": prova}).count()>0:
            client.close()
            return True
        else:
            client.close()
            return False

    def checkEsistenzaMateriale(self, materiale):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        if  db.materiale.find({"_id": materiale}).count()>0:
            client.close()
            return True
        else:
            client.close()
            return False

    def checkEsistenzaUtente(self, CF):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        if db.Utente.find({"_id": CF}).count() > 0:
            client.close()
            return True
        else:
            client.close()
            return False

    def addDocumento(self, certificatiJSON, file_ap, filename_ap, file_lavori, filename_lav):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        #verifico che non esiste un altro documento
        if db.documento.find({"_id":certificatiJSON['_id']}).count() > 0:
            client.close()
            return 1
        else:
            try:
                grid_fs = GridFS(db)
                certificatiJSON['apertura_name'] = filename_ap
                if filename_ap is not  "":
                    with grid_fs.new_file(filename=filename_ap) as fp:
                        fp.write(file_ap)
                        file_id = fp._id
                    certificatiJSON['file_apertura_id'] = file_id
                else:
                    certificatiJSON['file_apertura_id'] = ""

                certificatiJSON['lavori_name'] = filename_lav
                if  filename_lav is not "":
                    with grid_fs.new_file(filename=filename_lav) as fp:
                        fp.write(file_lavori)
                        file_id = fp._id
                    certificatiJSON['file_lavoro_id'] = file_id
                else:
                    certificatiJSON['file_lavoro_id'] = ""
                db.documento.insert_one(certificatiJSON)
                client.close()
                return 0
            except:
                client.close()
                return -1

    def findDocumento(self, pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        doc = db.documento.find({"_id": pratica})
        client.close()
        return doc

    def updateDocumnto(self, NumeroPratica, committente,descrizione, altroLuogo, day, provincia, comune):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.documento.update_one({"_id": NumeroPratica},
                                {"$set": {"committente": committente,"descrizione": descrizione,
                                          "altroLuogo": altroLuogo,"data": day,"provincia": provincia, "comune": comune}
                                 })
            client.close()
            return True
        except:
            client.close()
            return False

    def trovaFoglioLavoro(self, pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        doc = db.documento.find({"_id": pratica}, {"lavori_name": 1, "_id": 0} )
        client.close()
        return doc

    def trovaFoglioApertura(self,pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        doc = db.documento.find({"_id": pratica}, {"apertura_name": 1, "_id": 0})
        client.close()
        return doc

    def uploadFoglioLavoro(self, pratica, documento):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)
        try:
            # elimino il file di prima
            x = grid_fs.find({"filename": documento.filename})
            # elimino tutti i file relativi al numero di pratica
            for element in x:
                grid_fs.delete(element._id)

            # modifica del nome
            db.documento.update_one({"_id": pratica}, {"$set": {"lavori_name": documento.filename}})

            with grid_fs.new_file(filename=documento.filename) as fp:
                fp.write(documento)
                file_id = fp._id
            # aggiorno l'id del file
            db.documento.update_one({"_id": pratica}, {"$set": {"file_lavoro_id": file_id}})
            client.close()
            return True
        except:
            client.close()
            return False

    def uploadFoglioApertura(self,pratica,documento):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)
        try:
            # elimino il file di prima
            x = grid_fs.find({"filename": documento.filename})
            # elimino tutti i file relativi al numero di pratica
            for element in x:
                grid_fs.delete(element._id)

            # modifica del nome
            db.documento.update_one({"_id": pratica}, {"$set": {"apertura_name": documento.filename}})

            with grid_fs.new_file(filename=documento.filename) as fp:
                fp.write(documento)
                file_id = fp._id
            # aggiorno l'id del file
            db.documento.update_one({"_id": pratica}, {"$set": {"file_apertura_id": file_id}})
            client.close()
            return True
        except:
            client.close()
            return False

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

    def eliminaStruttura(self,struttura):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.struttura.remove({"_id": struttura})
        client.close()
        return True

    def eliminaProva(self, prova):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.prova.remove({"_id": prova})
        client.close()
        return True

    def eliminaMateriale(self, materiale):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.materiale.remove({"_id": materiale})
        client.close()
        return True

    def get_single_struttura(self, struttura):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        el = db.struttura.find({"_id": struttura})
        client.close()
        return el

    def get_single_prova(self, prova):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        el = db.prova.find({"_id": prova})
        client.close()
        return el

    def get_single_materiale(self, materiale):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        el = db.materiale.find({"_id": materiale})
        client.close()
        return el

    def update_Struttura(self,oldStruttura, newStruttura, newDesc):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.struttura.remove({"_id": oldStruttura})
            StrutturaJSON = {}
            StrutturaJSON["_id"] = newStruttura
            StrutturaJSON["descrizione"] = newDesc
            db.struttura.insert_one(StrutturaJSON)
            #devo aggiornare tutti i certificati che avevano quella struttura, solo se
            #è cambiato il nome ovviamente
            if oldStruttura is not newStruttura:
                db.certificato.update_many({"struttura": oldStruttura}, {"$set": {"struttura": newStruttura}})
            client.close()
            return True
        except:
            client.close()
            return False

    def update_Materiale(self, oldMateriale, newMateriale, newDesc):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.materiale.remove({"_id": oldMateriale})
            MaterialeJSON = {}
            MaterialeJSON["_id"] = newMateriale
            MaterialeJSON["descrizione"] = newDesc
            db.materiale.insert_one(MaterialeJSON)
            if oldMateriale is not newMateriale:
                db.certificato.update_many({"materiale": oldMateriale}, {"$set": {"materiale": newMateriale}})
            client.close()
            return True
        except:
            client.close()
            return False

    def update_Prova(self, oldProva, newProva, newDesc):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.prova.remove({"_id": oldProva})
            ProvaJSON = {}
            ProvaJSON["_id"] = newProva
            ProvaJSON["descrizione"] = newDesc
            db.prova.insert_one(ProvaJSON)
            if oldProva is not newProva:
                db.certificato.update_many({"prova": oldProva}, {"$set": {"prova": newProva}})
            client.close()
            return True
        except:
            client.close()
            return False

    def addMateriale(self, MaterialeJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            if db.materiale.find({"_id": MaterialeJSON['_id']}).count() == 0:
                db.materiale.insert_one(MaterialeJSON)
            else:
                db.materiale.update_one({"_id": MaterialeJSON['_id']},
                                        {"$set": {"descrizione": MaterialeJSON['descrizione']}})

            client.close()
            return True
        except:
            client.close()
            return False

    def addProva(self, ProvaJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            if db.prova.find({"_id": ProvaJSON['_id']}).count() == 0:
                db.prova.insert_one(ProvaJSON)
            else:
                db.prova.update_one({"_id": ProvaJSON['_id']}, {"$set": {"descrizione": ProvaJSON['descrizione']}})

            client.close()
            return True
        except:
            client.close()
            return False

    def addStruttura(self, StrutturaJSON):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            if db.struttura.find({"_id": StrutturaJSON['_id']}).count() == 0:
                db.struttura.insert_one(StrutturaJSON)
            else:
                db.struttura.update_one({"_id": StrutturaJSON['_id']},{"$set": {"descrizione": StrutturaJSON['descrizione']}})

            client.close()
            return True
        except:
            client.close()
            return False

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

    def getSingleUser(self, CF):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.Utente.find({"_id": CF}, {"dataInserimento":1, "flag": 1})
        client.close()
        return cnt

    def updateUtente(self, cf, ruolo, scade, data):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.Utente.update_one({"_id": cf}, { "$set": { "ruolo": ruolo, "scadenza": scade, "dataInserimento": data}})
            client.close()
            return True
        except:
            client.close()
            return False

    def findOldRuolo(self, CF):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        oldRuolo = db.Utente.find({"_id": CF}, {"_id":0 ,"ruolo": 1})[0]['ruolo']
        client.close()
        return oldRuolo

    def riattivaUtente(self, cf, data):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.Utente.update_one({"_id": cf}, {"$set": {"dataInserimento": data, "flag": True}})
            client.close()
            return True
        except:
            client.close()
            return False

    def disattivaUtente(self, cf):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        try:
            db.Utente.update_one({"_id": cf}, {"$set": {"flag": False}})
            client.close()
            return True
        except:
            client.close()
            return False

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

    def download(self, file):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)
        grid_fs_file = grid_fs.find_one({'filename': file})
        client.close()
        return grid_fs_file

    def deleteDocument(self, pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        grid_fs = GridFS(db)
        try:
            #prendo tutti i file legati alla pratica
            listOfFiles = []
            doc = db.documento.find({"_id": pratica})
            if doc[0]['apertura_name'] is not "":
                listOfFiles.append(doc[0]['apertura_name'])
            if doc[0]['lavori_name'] is not "":
                listOfFiles.append(doc[0]['lavori_name'])

            cert = db.certificato.find({"_id.NumeroPratica": pratica})
            for element in cert:
                listOfFiles.append(element['filename'])

            for f in  listOfFiles:
                x = grid_fs.find({"filename": f})
                #elimino tutti i file relativi al numero di pratica
                for element in x:
                    grid_fs.delete(element._id)

            #adesso elimino il certificato
            db.certificato.remove({"_id.NumeroPratica": pratica})
            #elimino il documento
            db.documento.remove({"_id": pratica})
            client.close()
            return True
        except:
            client.close()
            return False

    def getCertificati(self, pratica):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cert = db.certificato.find({"_id.NumeroPratica": pratica}, {"struttura": 1, "materiale": 1,
                                                                    "prova":1, "_id":1} )
        client.close()
        return cert

    def updateNumCertificati(self,pratica,num):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        db.documento.update_one({"_id": pratica}, {"$inc": {"NumeroCertificati": num}})
        client.close()

    def doQueryByMateriali(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.certificato.aggregate([{"$group": {"_id": "$materiale", "count": {"$sum":1}}}])
        client.close()
        return cnt

    def doQueryByStrutture(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.certificato.aggregate([{"$group": {"_id": "$struttura", "count": {"$sum": 1}}}])
        client.close()
        return cnt

    def doQueryByProve(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.certificato.aggregate([{"$group": {"_id": "$prova", "count": {"$sum": 1}}}])
        client.close()
        return cnt

    def queryByYear(self):
        client = MongoClient(DBConnectionManager.__dbname, DBConnectionManager.__dbport)
        db = client.Strutture
        cnt = db.documento.aggregate([{"$group": {"_id": "$data", "count": {"$sum":1}}}])
        client.close()
        return cnt






