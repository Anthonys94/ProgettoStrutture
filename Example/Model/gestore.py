import json
from Dao.dao import *

class Gestore:

    def __init__(self) -> None:
        super().__init__()

    def buildDocument(self, numeroPratica, dataRichiesta, committente, luogo, provincia, descrizione, tipologiaStruttura, tipoProva, materiale, allegatoCertificato):
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
        json_data = json.dumps(data)
        dao = daoGestore()
        dao.uploadDocumento(json_data)

    def buildTipologiaStruttura(self, tipologiaStruttura):
        data = {}
        data['tipologiaStruttura'] = tipologiaStruttura
        json_data = json.dumps(data)
        dao = daoGestore()
        dao.uploadStructure(json_data)

    def buildTipoProva(self, tipoProva):
        data = {}
        data['tipoProva'] = tipoProva
        json_data = json.dumps(data)
        dao = daoGestore()
        dao.uploadProva(json_data)

    def buildMateriale(self, materiale):
        data = {}
        data['materiale'] = materiale
        json_data = json.dumps(data)
        dao = daoGestore()
        dao.uploadMaterial(json_data)
