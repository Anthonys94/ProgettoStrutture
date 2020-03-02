from Dao.DBManager import*
import datetime

class GestoreForWrite:

    def __init__(self):
        super().__init__()

    def Login(self, username, password):
        return DBConnectionManager.getInstance().Login(username, password)

    def buildDocument(self, numeroPratica, day, committente, descrizione, provincia,
                      comune, altriLuoghi, nCertificati, documento_apertura, nomefile_apertura,
                      documento_lavori, nomefile_lavori):
        data = {}
        data["_id"] = numeroPratica
        data["data"] = day
        data["committente"] = committente
        data["descrizione"] = descrizione
        data["provincia"] = provincia
        data["comune"] = comune
        data["altroLuogo"] = altriLuoghi
        data["NumeroCertificati"]= nCertificati
        return DBConnectionManager.getInstance().addDocumento(data, documento_apertura, nomefile_apertura,
                                                              documento_lavori, nomefile_lavori)

    def findDocumento(self, pratica):
        return DBConnectionManager.getInstance().findDocumento(pratica)

    def updateDocumnto(self, NumeroPratica, committente,descrizione, altroLuogo, day, provincia, comune):
        return  DBConnectionManager.getInstance().updateDocumnto(NumeroPratica, committente,descrizione,
                                                                 altroLuogo, day, provincia, comune)

    def trovaFoglioLavoro(self, pratica):
        return DBConnectionManager.getInstance().trovaFoglioLavoro(pratica)

    def trovaFoglioApertura(self,pratica):
        return DBConnectionManager.getInstance().trovaFoglioApertura(pratica)

    def uploadFoglioLavoro(self, pratica, documento):
        return DBConnectionManager.getInstance().uploadFoglioLavoro(pratica, documento)

    def uploadFoglioApertura(self, pratica, documento):
        return DBConnectionManager.getInstance().uploadFoglioApertura(pratica, documento)

    def buildCertificato(self, numeroPratica, lettera, struttura, materiale,
                         prova, certificato, nomefile):
        data ={}
        id ={}
        id['NumeroPratica']=numeroPratica
        id['Lettera'] = lettera
        data['_id']= id
        data['struttura'] = struttura
        data['materiale'] = materiale
        data['prova'] = prova
        return DBConnectionManager.getInstance().addCertificato(data, certificato, nomefile)

    def buildTipologiaStruttura(self, tipologiaStruttura, descrizione):
        data = {}
        data["_id"] = tipologiaStruttura
        data['descrizione'] = descrizione
        return DBConnectionManager.getInstance().addStruttura(data)

    def buildTipoProva(self, tipoProva, descrizione):
        data = {}
        data["_id"] = tipoProva
        data['descrizione'] = descrizione
        return DBConnectionManager.getInstance().addProva(data)

    def buildMateriale(self, materiale, descrizione):
        data = {}
        data["_id"] = materiale
        data['descrizione'] = descrizione
        return DBConnectionManager.getInstance().addMateriale(data)

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

    def addUtente(self, nome, cognome, provincia, comune, bday, CF, password, ruolo, scadenza, dataInserimento, flag):
        data={}
        data['_id'] = CF
        data['nome']= nome
        data['cognome']= cognome
        data['provincia']= provincia
        data['comune'] = comune
        data['bday']=bday
        data['password']= password
        data['ruolo'] = ruolo
        data['scadenza'] = scadenza
        data['dataInserimento']=dataInserimento
        data['flag']=flag
        return DBConnectionManager.getInstance().addUtente(data)

    def getUtenti(self):
        return DBConnectionManager.getInstance().getUtenti()

    def getSingleUser(self, CF):
        return DBConnectionManager.getInstance().getSingleUser(CF)

    def updateUtente(self, cf, ruolo, scade, data):
        return DBConnectionManager.getInstance().updateUtente(cf, ruolo, scade, data)

    def findOldRuolo(self, CF):
        return DBConnectionManager.getInstance().findOldRuolo(CF)

    def riattivaUtente(self, CF,data):
        return DBConnectionManager.getInstance().riattivaUtente(CF, data)

    def disattivaUtente(self, cf):
        return DBConnectionManager.getInstance().disattivaUtente(cf)

    def DoQuerybyPratica(self, numeroPratica):
        return DBConnectionManager.getInstance().DoQuerybyPratica(numeroPratica)

    def DoQueryOnDocument(self, jsonElement ):
        return DBConnectionManager.getInstance().DoQueryOnDocument(jsonElement)

    def DoQueryOnCertificato(self, jsonElement ):
        return DBConnectionManager.getInstance().DoQueryOnCertificato(jsonElement)

    def checkEsistenza(self, pratica):
        return DBConnectionManager.getInstance().checkEsistenza(pratica)

    def checkEsistenzaStruttura(self, struttura):
        return DBConnectionManager.getInstance().checkEsistenzaStruttura(struttura)

    def checkEsistenzaProva(self, prova):
        return DBConnectionManager.getInstance().checkEsistenzaProva(prova)

    def checkEsistenzaMateriale(self, materiale):
        return DBConnectionManager.getInstance().checkEsistenzaMateriale(materiale)

    def eliminaStruttura(self,struttura):
        return DBConnectionManager.getInstance().eliminaStruttura(struttura)

    def eliminaProva(self, prova):
        return DBConnectionManager.getInstance().eliminaProva(prova)

    def eliminaMateriale(self, materiale):
        return DBConnectionManager.getInstance().eliminaMateriale(materiale)

    def get_single_struttura(self, struttura):
        return DBConnectionManager.getInstance().get_single_struttura(struttura)

    def get_single_materiale(self, materiale):
        return DBConnectionManager.getInstance().get_single_materiale(materiale)

    def get_single_prova(self, prova):
        return DBConnectionManager.getInstance().get_single_prova(prova)

    def update_Struttura(self, oldStruttura, newStruttura, newDesc):
        return DBConnectionManager.getInstance().update_Struttura(oldStruttura, newStruttura, newDesc)

    def update_Prova(self, oldProva, newProva, newDesc):
        return DBConnectionManager.getInstance().update_Prova(oldProva, newProva, newDesc)

    def update_Materiale(self, oldMateriale, newMateriale, newDesc):
        return DBConnectionManager.getInstance().update_Materiale(oldMateriale, newMateriale, newDesc)

    def checkEsistenzaUtente(self, CF):
        return DBConnectionManager.getInstance().checkEsistenzaUtente(CF)

    def download(self, file):
        return DBConnectionManager.getInstance().download(file)

    def deleteDocument(self, pratica):
        return DBConnectionManager.getInstance().deleteDocument(pratica)

    def getCertificati(self, pratica):
        return DBConnectionManager.getInstance().getCertificati(pratica)

    def updateNumCertificati(self, pratica, num):
        return DBConnectionManager.getInstance().updateNumCertificati(pratica, num)

    def doQueryByMateriali(self):
        return DBConnectionManager.getInstance().doQueryByMateriali()

    def doQueryByStrutture(self):
        return DBConnectionManager.getInstance().doQueryByStrutture()

    def doQueryByProve(self):
        return DBConnectionManager.getInstance().doQueryByProve()

    def queryByYear(self):
        return DBConnectionManager.getInstance().queryByYear()