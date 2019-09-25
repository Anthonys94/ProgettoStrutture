from Dao.DBManager import*

class GestoreForWrite:

    def __init__(self):
        super().__init__()

    def buildDocument(self, numeroPratica, dataRichiesta, committente, luogo, provincia, descrizione,
                      tipologiaStruttura, tipoProva, materiale, allegatoCertificato):
        data = {}
        data['numeroPratica'] = numeroPratica
        data['dataRichiesta'] = dataRichiesta
        data['committente'] = committente
        data['luogo'] = luogo
        data['provincia'] = provincia
        data['descrizione'] = descrizione
        data['tipologiaStruttura'] = tipologiaStruttura
        data['tipoProva'] = tipoProva
        data['materiale'] = materiale

        DBConnectionManager.getInstance().addCertificato(data)


    def buildTipologiaStruttura(self, tipologiaStruttura, descrizione):
        data = {}
        data['tipologiaStruttura'] = tipologiaStruttura
        data['descrizione'] = descrizione

        DBConnectionManager.getInstance().addStruttura(data)

    def buildTipoProva(self, tipoProva):
        data = {}
        data['tipoProva'] = tipoProva

        DBConnectionManager.getInstance().addProva(data)

    def buildMateriale(self, materiale):
        data = {}
        data['materiale'] = materiale

        DBConnectionManager.getInstance().addMateriale(data)
