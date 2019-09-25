from Dao.DBManager import*
import json
a = DBConnectionManager.getInstance()

data = {}
data['numeroPratica'] = 'a'
data['dataRichiesta'] = 'b'
data['committente'] = 'c'
data['luogo'] = 'd'
data['provincia'] = 'e'
data['descrizione'] = 'f'
data['tipologiaStruttura'] = 'g'
data['tipoProva'] = 'h'
data['materiale'] = 'i'

a.addCertificato(data)