from Dao.DBManager import*
import datetime

class GestoreForWrite:

    def __init__(self):
        super().__init__()

    def Login(self, username, password):
        return DBConnectionManager.getInstance().Login(username, password)

    def buildDocument(self, numeroPratica, day, committente, descrizione, provincia,
                      comune, altriLuoghi, nCertificati, documento, nomefile):
        data = {}
        data["_id"] = numeroPratica
        data["data"] = day
        data["committente"] = committente
        data["descrizione"] = descrizione
        data["provincia"] = provincia
        data["comune"] = comune
        data["altroLuogo"] = altriLuoghi
        data["NumeroCertificati"]= nCertificati
        return DBConnectionManager.getInstance().addDocumento(data, documento, nomefile)

    def buildCertificato(self, numeroPratica, lettera, struttura, materiale,
                         prova, certificato, nomefile):
        data ={}
        id ={}
        id['NumeroPratica']=numeroPratica
        id['Lettera'] = lettera.upper()
        print(id['Lettera'])
        data['_id']= id
        #data['_id']['NumeroPratica'] = numeroPratica
        #data['_id']['Lettera'] = lettera
        data['struttura'] = struttura
        data['materiale'] = materiale
        data['prova'] = prova
        DBConnectionManager.getInstance().addCertificato(data, certificato, nomefile)

    def buildTipologiaStruttura(self, tipologiaStruttura, descrizione):
        data = {}
        data["_id"] = tipologiaStruttura
        data['descrizione'] = descrizione
        DBConnectionManager.getInstance().addStruttura(data)

    def buildTipoProva(self, tipoProva, descrizione):
        data = {}
        data["_id"] = tipoProva
        data['descrizione'] = descrizione

        DBConnectionManager.getInstance().addProva(data)

    def buildMateriale(self, materiale, descrizione):
        data = {}
        data["_id"] = materiale
        data['descrizione'] = descrizione
        DBConnectionManager.getInstance().addMateriale(data)

    def getStrutture(self):
        return DBConnectionManager.getInstance().getStrutture()

    def getProva(self):
        return DBConnectionManager.getInstance().getProva()

    def getMateriale(self):
        return DBConnectionManager.getInstance().getMateriale()

    def getProvince(self):
        return DBConnectionManager.getInstance().getProvince()

    def getComuni(self, provincia):
        return DBConnectionManager.getInstance().getComuni(provincia)

    def addUtente(self, nome, cognome, provincia, comune, bday, CF, password, ruolo, dataInserimento):
        data={}
        data['_id'] = CF
        data['nome']= nome
        data['cognome']= cognome
        data['provincia']= provincia
        data['comune'] = comune
        data['bday']=bday
        data['password']= password
        data['ruolo'] = ruolo
        data['dataInserimento']=dataInserimento

        return DBConnectionManager.getInstance().addUtente(data)

    def getUtenti(self):
        return DBConnectionManager.getInstance().getUtenti()

    def checkUtente(self, CF):
        return DBConnectionManager.getInstance().checkUtente(CF)

    def checkUtenteInattivo(self, CF):
        return DBConnectionManager.getInstance().checkUtenteInattivo(CF)

    def updateUtente(self, cf, ruolo,  data):
        return DBConnectionManager.getInstance().updateUtente(cf, ruolo, data)

    def findOldRuolo(self, CF):
        return DBConnectionManager.getInstance().findOldRuolo(CF)

    def riattivaUtente(self, CF,ruolo,data):
        return DBConnectionManager.getInstance().riattivaUtente(CF,ruolo, data)

    def DoQuerybyPratica(self, numeroPratica):
        return DBConnectionManager.getInstance().DoQuerybyPratica(numeroPratica)

    def DoQueryOnDocument(self, jsonElement ):
        return DBConnectionManager.getInstance().DoQueryOnDocument(jsonElement)

    def DoQueryOnCertificato(self, jsonElement ):
        return DBConnectionManager.getInstance().DoQueryOnCertificato(jsonElement)

    def DeleteDocument(self, pratica):
        return  DBConnectionManager.getInstance().DeleteDocument(pratica)

