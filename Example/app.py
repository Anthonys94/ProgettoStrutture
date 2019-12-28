from flask import Flask, flash, render_template, json, request, redirect, make_response
from Model.gestore import *
from flask import jsonify
from werkzeug.utils import secure_filename
import datetime
#BOOTSTRAP BUONO vendor/boostrap/css/min.css
'''
TODO:
    aggiustare la post del LOGIN --> ok
    AGGIUSTARE LUOGO A STRINGA --> ok
    gestire un duplicato sul documento  --> ok 
    struttura materiale o prova -> ok 
    eliminare una struttura, materiale o prova e documento nel caso di errore
    
    controllare i maiuscoli
    query by materiale
    query by anno
    query by luogo
'''
app = Flask(__name__)

UPLOAD_FOLDER = '/Users/antonio/Downloads'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
#------ UTILITY FUNCTIONS
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def Scaduto(dataInserimento):
    dataInserimentoNew = datetime.datetime.strptime(dataInserimento, '%Y-%m-%d').date()
    dataCorrente = datetime.datetime.now().date()
    if (dataCorrente - dataInserimentoNew).days > 30:
        return True
    else:
        return False

regUsers = []

def AnnullaTuttoVaiLogIn(username,ruolo, data, url):
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        if [username, ruolo] in regUsers: #MI SERVE NEL CASO A FARE TRUE è LA PARTE DI DESTRA
            regUsers.remove([username, ruolo])
        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        return resp
    else:
        return make_response(render_template('/'+ url))

#--------- login e logOut
#la prima cosa da fare è quella di vedere se l'utente sta in regUsers, poi vado a controllare la data
#Un problema da gestire è quello degli utenti che fanno scadere i cookie senza fare il logOut.
#la loro utenza rimane nel registro
@app.route('/', methods=['GET'])
def main():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    print(username)
    print(ruolo)
    print(data)
    if ruolo not in ['Amministratore', 'Leader', 'Operatore', 'Utente Semplice', 'Utente Pro']:
        return make_response(render_template("index.html"))
    elif ruolo == 'Amministratore':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'home.html')
    elif ruolo == 'Operatore':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'homeOperatore.html')
    elif ruolo == 'Leader':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'homeLeader.html')
    elif ruolo in ['Utente Semplice', 'Utente Pro']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'homeUser.html')


    '''
    if [username, ruolo] in regUsers:
        regUsers.remove([username, ruolo])
        print(regUsers)
    resp = make_response(render_template("index.html"))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('ruolo', '', expires=0)
    resp.set_cookie('dataIns', '', expires=0)
    return resp
    '''

@app.route('/logOut', methods=['GET'])
def logOut():
    #questa funzione viene chiamata quando mi disconnetto, eliminando i cookie relativi all'utente
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    if [username, ruolo] in regUsers:
        regUsers.remove([username, ruolo])
        print(regUsers)
    resp = make_response(redirect('/'))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('ruolo', '', expires=0)
    resp.set_cookie('dataIns', '', expires=0)
    return resp

@app.route('/', methods=['POST'])
def main_post_login():
    gestore = GestoreForWrite()
    login = gestore.Login(request.form['Username'], request.form['pass'])
    if login.count() == 1:
        #Suppendo che i dati ci siano, se si tratta di un utenteSemplice con l'account Scaduto, non può accedere
        if login[0]["ruolo"] == 'Utente Semplice' and Scaduto(login[0]["dataInserimento"].date().strftime("%Y-%m-%d")):
            if [login[0]["_id"], login[0]["ruolo"]] in regUsers:
                regUsers.remove([login[0]["_id"], login[0]["ruolo"]])
            return redirect(request.url)
        else:
            if login[0]["ruolo"] == 'Amministratore':
                resp = make_response(render_template("home.html"))
            elif login[0]["ruolo"] == 'Leader':
                resp = make_response(render_template("homeLeader.html"))
            elif login[0]["ruolo"] == 'Operatore':
                resp = make_response(render_template("homeOperatore.html"))
            elif login[0]["ruolo"] in ['Utente Semplice', 'Utente Pro']:
                resp = make_response(render_template("homeUser.html"))
            resp.set_cookie('username', login[0]["_id"])
            resp.set_cookie('ruolo', login[0]["ruolo"])
            resp.set_cookie('dataIns',login[0]["dataInserimento"].date().strftime("%Y-%m-%d"))
            if [login[0]["_id"],login[0]["ruolo"]]  not in regUsers:
                regUsers.append([login[0]["_id"],login[0]["ruolo"]])
            print(regUsers)
        return resp
    else:
        return redirect(request.url)

#----------------- GET REQUEST
@app.route('/home.html', methods=['GET'])
def main_home():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo == 'Amministratore':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'home.html')
    elif ruolo == 'Operatore':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'homeOperatore.html')
    elif ruolo == 'Leader':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'homeLeader.html')
    elif ruolo in ['Utente Semplice', 'Utente Pro']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'homeUser.html')
    else:
        return make_response(redirect('/'))
    #se l'utente è un amministratore o altro devo solo controllare l'esistenza nel registro
    #altrimenti se è un utente devo anche controllare se è scaduto
    #Condizione per cui deve essere fatto di nuovo il logIn:
    #   l'utente non è proprio registrato (non sta in regUsers) oppure è un utenteSemplice con accountScaduto


@app.route('/FormInserimentoMateriale.html', methods=['GET'])
def main_Materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo in ['Leader', 'Amministratore']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'FormInserimentoMateriale.html')
    else:
        return render_template('NoPermesso.html')

    '''
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        return render_template('FormInserimentoMateriale.html')
    '''

@app.route('/gestioneUtenze.html', methods=['GET'])
def gestioneUtenze():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo == 'Amministratore':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'gestioneUtenze.html')
    else:
        return render_template('NoPermesso.html')
    '''
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        return render_template('gestioneUtenze.html')
    '''

@app.route('/FormInserimentoProva.html', methods=['GET'])
def main_Prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo in ['Leader', 'Amministratore']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'FormInserimentoProva.html')
    else:
        return render_template('NoPermesso.html')

    '''
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        return render_template('FormInserimentoProva.html')
    '''

@app.route('/FormInserimentoStruttura.html', methods=['GET'])
def main_Struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo in ['Leader', 'Amministratore']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'FormInserimentoStruttura.html')
    else:
        return render_template('NoPermesso.html')

    '''
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        return render_template('FormInserimentoStruttura.html')
    '''

@app.route('/FormEliminaDocumento.html', methods=['GET'])
def delete_documento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo == 'Amministratore':
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'FormEliminaDocumento.html')
    else:
        return render_template('NoPermesso.html')

@app.route('/FormInserimentoDocumento.html', methods=['GET'])
def main_Documento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo in ['Leader', 'Amministratore', 'Operatore']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'FormInserimentoDocumento.html')
    else:
        return render_template('NoPermesso.html')

    '''
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        return render_template('FormInserimentoDocumento.html')
    '''

@app.route('/ricerca.html', methods=['GET'])
def formQuery():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ruolo in ['Leader',  'Utente Semplice']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'ricerca.html')
    elif ruolo in ['Amministratore', 'Utente Pro']:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, 'ricercaAdvanced.html')
    else:
        return render_template('NoPermesso.html')

@app.route('/getStrutture', methods=['GET'])
def getStrutture():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getStrutture()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['tipologiaStruttura'] = element['_id']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getStruttureWithDesc', methods=['GET'])
def getStruttureWithDesc():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo == 'Utente Semplice':
            render_template('NoPermesso.html')
        else:
            gestore = GestoreForWrite()
            strutture = gestore.getStrutture()
            jsonlist = []
            for element in strutture:
                ob = {}
                ob['tipologiaStruttura'] = element['_id']
                ob['descrizione'] = element['descrizione']
                jsonlist.append(ob)
            return jsonify(jsonlist)

@app.route('/getProva', methods=['GET'])
def getProva():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getProva()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['tipoProva'] = element['_id']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getProvaWithDesc', methods=['GET'])
def getProvaWithDesc():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    print(regUsers)
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getProva()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['tipoProva'] = element['_id']
            ob['descrizione'] = element['descrizione']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getMateriale', methods=['GET'])
def getMateriale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getMateriale()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['materiale'] = element['_id']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getMaterialeWithDesc', methods=['GET'])
def getMaterialewithDesc():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getMateriale()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['materiale'] = element['_id']
            ob['descrizione'] = element['descrizione']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getProvince', methods=['GET'])
def getProvince():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        province = gestore.getProvince()
        jsonlist = []
        for element in province:
            if element != None:
                ob = {}
                ob['provincia'] = element
                jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getComuni', methods=['GET'])
def getComuni():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        comuni = gestore.getComuni(request.args.get('provincia'))
        jsonlist = []
        for element in comuni:
            ob = {}
            ob['comune'] = element['Comune']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getUtenti', methods=['GET'])
def getUtenti():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        utenti = gestore.getUtenti()
        jsonlist = {}
        Scaduti = []
        Attivi = []
        for element in utenti:
            ob = {}
            ob['nome'] = element['nome']
            ob['cognome'] = element['cognome']
            ob['cf'] = element['_id']
            ob['ruolo'] = element['ruolo']
            ob['dataInserimento'] = element['dataInserimento'].date().strftime("%Y-%m-%d")
            if not Scaduto(element['dataInserimento'].date().strftime("%Y-%m-%d")):
                Attivi.append(ob)
            else:
                Scaduti.append(ob)

            jsonlist['Attivi']= Attivi
            jsonlist['Scaduti'] =Scaduti

        return jsonify(jsonlist)

@app.route('/verificaUtente', methods=['GET'])
#questa deve verificare l'esistenza e l'attività
def checkUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        ob = {}
        ut = gestore.checkUtenteInattivo(request.args.get('CF'))
        if ut.count() > 0 and not (Scaduto(ut[0]['dataInserimento'].date().strftime("%Y-%m-%d"))):
            ob['check'] = True
        else:
            ob['check'] = False
        return jsonify(ob)

@app.route('/verificaUtenteInattivo', methods=['GET'])
#un'altra funzione deve verificare l'esistenza e l'inattività
def checkUtenteInattivo():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        ob = {}
        ut = gestore.checkUtenteInattivo(request.args.get('CF'))
        if ut.count() > 0 and Scaduto(ut[0]['dataInserimento'].date().strftime("%Y-%m-%d")):
            ob['check'] = True
        else:
            ob['check'] = False
        return jsonify(ob)

@app.route('/DoquerybyPratica', methods=['GET'])
def doQuerybyPratica():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        ob={}
        gestore = GestoreForWrite()
        print(request.args.get('NumeroPratica'))
        doc = gestore.DoQuerybyPratica(request.args.get('NumeroPratica'))
        lResult=[]
        print(doc.count())
        num=0
        for element in doc:
            query = {}
            query["_id.NumeroPratica"] = element["_id"]
            cert = gestore.DoQueryOnCertificato(query)
            if cert.count() > 0:
                for y in cert:
                    oggetto = {}
                    oggetto['NumeroPratica'] = element["_id"]
                    oggetto['Rif'] = y['_id']['Lettera']
                    oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                    oggetto['descrizione'] = element['descrizione']
                    oggetto['provincia'] = element['provincia']
                    oggetto['comune'] = element['comune']
                    oggetto['altroLuogo'] = element['altroLuogo']
                    oggetto['struttura'] = y['struttura']
                    oggetto['materiale'] = y['materiale']
                    oggetto['prova'] = y['prova']
                    lResult.append(oggetto)

            num = num + cert.count()

        if ruolo == 'Utente Semplice':
            result = {}
            result["num"] = num
            return jsonify(result)
        else:
            return jsonify(lResult)

@app.route('/DoquerybyCampi', methods=['GET'])
def doQuerybyCampi():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        gestore = GestoreForWrite()
        criterio = request.args.get('criterio')
        num = 0
        lResult = []
        if criterio == 'and':
            ob = {}
            list = []
            if request.args.get('DataStart') is not "":
                app = {}
                app['data'] = {"$gte": datetime.datetime.strptime(request.args.get('DataStart'), '%Y-%m-%d')}
                list.append(app)
            if request.args.get('DataEnd') is not "":
                app = {}
                app['data'] = {"$lt": datetime.datetime.strptime(request.args.get('DataEnd'), '%Y-%m-%d')}
                list.append(app)
            if request.args.get('Provincia') is not "":
                app = {}
                app['provincia'] = request.args.get('Provincia')
                list.append(app)
            if request.args.get('Comune') is not "":
                app = {}
                app['comune'] = request.args.get('Comune')
                list.append(app)
            if request.args.get('AltroLuogo') is not "":
                appList = []
                app = {}
                parole = request.args.get('AltroLuogo').split(' ')
                for parola in parole:
                    p = {}
                    p['altroLuogo'] = {"$regex": parola}
                    appList.append(p)
                app["$or"] = appList
                list.append(app)
            if request.args.get('Committente') is not "":
                appList = []
                app = {}
                parole = request.args.get('Committente').split(' ')
                for parola in parole:
                    p = {}
                    p['committente'] = {"$regex": parola}
                    appList.append(p)
                app["$or"] = appList
                list.append(app)
            if request.args.get('Descrizione') is not "":
                appList = []
                app = {}
                parole = request.args.get('Descrizione').split(' ')
                for parola in parole:
                    p = {}
                    p['descrizione'] = {"$regex": parola}
                    appList.append(p)
                app["$or"] = appList
                list.append(app)
            if (len(list)>0):
                ob['$and'] = list
            print('and')
            print(ob)
            doc = gestore.DoQueryOnDocument(ob)
            for element in doc:
                query = {}
                query["_id.NumeroPratica"] = element["_id"]
                if request.args.get('Materiale') is not "":
                    query['materiale'] = request.args.get('Materiale')
                if request.args.get('Struttura') is not "":
                    query['struttura'] = request.args.get('Struttura')
                if request.args.get('Prova') is not "":
                    query['prova'] = request.args.get('Prova')
                print(query)
                cert = gestore.DoQueryOnCertificato(query)
                if cert.count() > 0:
                    for y in cert:
                        oggetto ={}
                        oggetto['NumeroPratica'] = element["_id"]
                        oggetto['Rif'] = y['_id']['Lettera']
                        oggetto['data']= element['data'].date().strftime("%Y-%m-%d")
                        oggetto['descrizione']= element['descrizione']
                        oggetto['provincia']=element['provincia']
                        oggetto['comune']= element['comune']
                        oggetto['altroLuogo'] = element['altroLuogo']
                        oggetto['struttura'] =y['struttura']
                        oggetto['materiale'] =y['materiale']
                        oggetto['prova']= y['prova']
                        lResult.append(oggetto)

                num = num + cert.count()

        else:
            ob = {}  # questo deve avere la or
            list = []
            listOr = []
            if request.args.get('DataStart') is not "":
                app = {}
                app['data'] = {"$gte": datetime.datetime.strptime(request.args.get('DataStart'), '%Y-%m-%d')}
                list.append(app)
            if request.args.get('DataEnd') is not "":
                app = {}
                app['data'] = {"$lt": datetime.datetime.strptime(request.args.get('DataEnd'), '%Y-%m-%d')}
                list.append(app)
            if request.args.get('Provincia') is not "":
                app = {}
                app['provincia'] = request.args.get('Provincia')
                listOr.append(app)
            if request.args.get('Comune') is not "":
                app = {}
                app['comune'] = request.args.get('Comune')
                listOr.append(app)
            if request.args.get('AltroLuogo') is not "":
                parole = request.args.get('AltroLuogo').split(' ')
                for parola in parole:
                    p = {}
                    p['altroLuogo'] = {"$regex": parola}
                    listOr.append(p)
            if request.args.get('Committente') is not "":
                parole = request.args.get('Committente').split(' ')
                for parola in parole:
                    p = {}
                    p['committente'] = {"$regex": parola}
                    listOr.append(p)
            if request.args.get('Descrizione') is not "":
                parole = request.args.get('Descrizione').split(' ')
                for parola in parole:
                    p = {}
                    p['descrizione'] = {"$regex": parola}
                    listOr.append(p)
            app = {}
            if ( len(listOr)>0):
                app['$or'] = listOr
                list.append(app)
            if (len(list)>0):
                ob['$and'] = list
            print('or')
            print(ob)
            doc = gestore.DoQueryOnDocument(ob)
            for element in doc:
                query = {}
                list= []
                listOr = []
                app = {}
                app["_id.NumeroPratica"] = element["_id"]
                list.append(app)
                if request.args.get('Materiale') is not "":
                    app={}
                    app['materiale'] = request.args.get('Materiale')
                    listOr.append(app)
                if request.args.get('Struttura') is not "":
                    app = {}
                    app['struttura'] = request.args.get('Struttura')
                    listOr.append(app)
                if request.args.get('Prova') is not "":
                    app = {}
                    app['prova'] = request.args.get('Prova')
                    listOr.append(app)

                app = {}
                if (len(listOr)>0):
                    app['$or'] = listOr
                    list.append(app)
                query["$and"] = list
                print(query)
                cert = gestore.DoQueryOnCertificato(query)
                if cert.count() > 0:
                    for y in cert:
                        oggetto ={}
                        oggetto['NumeroPratica'] = element["_id"]
                        oggetto['Rif'] = y['_id']['Lettera']
                        oggetto['data']= element['data'].date().strftime("%Y-%m-%d")
                        oggetto['descrizione']= element['descrizione']
                        oggetto['provincia']=element['provincia']
                        oggetto['comune']= element['comune']
                        oggetto['altroLuogo'] = element['altroLuogo']
                        oggetto['struttura'] =y['struttura']
                        oggetto['materiale'] =y['materiale']
                        oggetto['prova']= y['prova']
                        lResult.append(oggetto)

                num = num + cert.count()

        if ruolo == 'Utente Semplice':
            result={}
            result["num"] = num
            return jsonify(result)
        else:
            return jsonify(lResult)

#------- POST REQUESTS

@app.route('/FormInserimentoProva.html', methods=['POST'])
def upload_prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo in ['Leader', 'Amministratore']:
            gestore = GestoreForWrite()
            gestore.buildTipoProva(request.form['TipologiaProva'], request.form['DescrizioneProva'])
            #return render_template('home.html')
            return redirect(request.url)
        else:
            return render_template('NoPermesso.html')

@app.route('/FormInserimentoStruttura.html', methods=['POST'])
def upload_struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo in ['Leader', 'Amministratore']:
            gestore = GestoreForWrite()
            gestore.buildTipologiaStruttura(request.form['TipologiadiStruttura'], request.form['Descrizionestruttura'])
            return redirect(request.url)
        else:
            return render_template('NoPermesso.html')

@app.route('/FormInserimentoDocumento.html', methods=['POST'])
def upload_file():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo in ['Leader', 'Amministratore', 'Operatore']:
            documento = request.files['Documento']
            numeroDocumenti = int(request.form['NumCertificati'])
            gestore = GestoreForWrite()
            if documento and allowed_file(documento.filename):
                documento.filename = request.form['TextPratica'] + ".pdf"
                documento.filename = secure_filename(documento.filename)
                esitoDocumento =gestore.buildDocument(request.form['TextPratica'], datetime.datetime.strptime(request.form['day'], '%Y-%m-%d'),
                                                      request.form['Committente'],
                                                      request.form['Descrizione'], request.form['Provincia'], request.form['Comune'],
                                                      request.form['AltroLuogo'],int(request.form['NumCertificati']),
                                                      documento, documento.filename)
                if esitoDocumento:
                    for index in range(0, numeroDocumenti):
                        certificato = request.files['Certificato'+ str(index)]
                        if certificato and allowed_file(certificato.filename):
                            certificato.filename = request.form['TextPratica']+ '_' + request.form['Lettera'+str(index)]+'.pdf'
                            certificato.filename = secure_filename(certificato.filename)
                            gestore.buildCertificato(request.form['TextPratica'],request.form['Lettera'+str(index)],
                                                     request.form['Struttura'+str(index)],  request.form['Materiale'+str(index)],
                                                     request.form['Prova'+str(index)], certificato, certificato.filename)
                        else:
                            print('formato errato di un certificato')
                            return render_template('FormInserimentoDocumentoErrore.html')
                    return render_template('home.html')
                else:
                    print('inserimento documento fallito')
                    return render_template('FormInserimentoDocumentoErrore.html')
            else:
                print('formato errato del documento')
                return render_template('FormInserimentoDocumentoErrore.html')
        else:
            print('No permesso')
            return render_template('NoPermesso.html')

@app.route('/FormInserimentoMateriale.html', methods=['POST'])
def upload_Materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo in ['Leader', 'Amministratore']:
            gestore = GestoreForWrite()
            gestore.buildMateriale(request.form['TipoMateriale'], request.form['DescrizioneMateriale'])
            return redirect(request.url)
        else:
            return render_template('NoPermesso.html')

@app.route('/gestioneUtenze.html', methods=['POST'])
def newUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo =='Amministratore':
            ob = {}
            gestore = GestoreForWrite()
            if gestore.addUtente(request.form['Nome'], request.form['Cognome'],  request.form['Provincia'],
                                 request.form['Comune'], request.form['bday'], request.form['CodiceFiscale'],
                                 request.form['Password'], request.form['Ruolo'],
                                 datetime.datetime.now()):
                ob['check']= True
            else:
                ob['check']= False
            return jsonify(ob)
        else:
            return render_template('NoPermesso.html')

@app.route('/DeleteDocument', methods=['POST'])
def DeleteDocument():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo =='Amministratore':
            gestore= GestoreForWrite()
            result = {}
            result['esito'] = gestore.DeleteDocument(request.form['Pratica'])
            return jsonify(result)
        else:
            return render_template('NoPermesso.html')


#----- PUT REQUESTS
@app.route('/updateUtente', methods=['PUT'])
def updateRole():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo == 'Amministratore':
            gestore = GestoreForWrite()
            oldRuolo = gestore.findOldRuolo(request.form['CF'])
            if [request.form['CF'], oldRuolo] in regUsers:
                regUsers.remove([request.form['CF'], oldRuolo])
            gestore.updateUtente(request.form['CF'], request.form['ruolo'],datetime.datetime.now())
            return render_template('gestioneUtenze.html')
        else:
            return render_template('NoPermesso.html')

@app.route('/RiattivaUtente', methods=['PUT'])
def riattivaUtente():

    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    if ([username, ruolo] not in regUsers) or (ruolo == 'Utente Semplice' and Scaduto(data)):
        return redirect('/')
    else:
        if ruolo == 'Amministratore':
            gestore = GestoreForWrite()
            oldRuolo = gestore.findOldRuolo(request.form['CF'])
            if [request.form['CF'], oldRuolo] in regUsers:
                regUsers.remove([request.form['CF'], oldRuolo])
            user = gestore.riattivaUtente(request.form['CF'], request.form['ruolo'],datetime.datetime.now())
            ob={}
            ob['nome']= user[0]['nome']
            ob['cognome'] = user[0]['cognome']
            ob['cf'] = user[0]['_id']
            ob['ruolo'] = user[0]['ruolo']
            ob['dataInserimento'] = user[0]['dataInserimento']
            return jsonify(ob)
        else:
            return render_template('NoPermesso.html')






if __name__ == "__main__":
    app.run(port=5002)
