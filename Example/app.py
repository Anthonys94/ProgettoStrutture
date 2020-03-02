from flask import Flask, flash, render_template, json, request, redirect, make_response
from Model.gestore import *
from flask import jsonify
import datetime
import pandas as pd
from werkzeug.utils import secure_filename

Amministratore = 'Amministratore'
Master = 'Master'
Operatore = 'Operatore'
Leader = 'Leader'
UtentePro = 'Utente Pro'
UtenteSemplice = 'Utente Semplice'

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/antonio/Downloads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


# ------ UTILITY FUNCTIONS
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def Scaduto(dataInserimento, flag):
    '''
    :param dataInserimento:  datetime
    :param flag: boolean
    '''
    dataCorrente = datetime.datetime.now().date()
    if (not flag) or (dataCorrente - dataInserimento).days > 30:
        return True
    else:
        return False


regUsers = []


def AnnullaTuttoVaiLogIn(username, ruolo, data, flag,  url):
    if ([username, ruolo] not in regUsers) or (Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        return make_response(render_template('/' + url))

#----------- > FUNZIONI DEFINITIVE
 # main
@app.route('/', methods=['GET'])
def main():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')

    if ruolo not in [Amministratore, Master, Leader, Operatore, UtenteSemplice, UtentePro]:
        return make_response(render_template("index.html"))
    elif ruolo == Amministratore or ruolo == Master:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'Home.html')
    elif ruolo == Operatore:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'HomeOperatore.html')
    elif ruolo == Leader:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'homeLeader.html')
    elif ruolo == UtenteSemplice or ruolo == UtentePro:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'HomeUser.html')
    else:
        return make_response(render_template("index.html"))
#Log in
@app.route('/', methods=['POST'])
def main_post_login():
    gestore = GestoreForWrite()
    login = gestore.Login(request.form['Username'].upper(), request.form['pass'])

    if login.count() == 1:
        if Scaduto(login[0]["dataInserimento"].date(), login[0]['flag']):
            if [login[0]["_id"], login[0]["ruolo"]] in regUsers:
                regUsers.remove([login[0]["_id"], login[0]["ruolo"]])
            return redirect(request.url)
        else:

            if login[0]["ruolo"] == Amministratore or login[0]["ruolo"] == Master:
                resp = make_response(render_template('/Home.html'))
            elif login[0]["ruolo"] == Leader:
                resp = make_response(render_template('/homeLeader.html'))
            elif login[0]["ruolo"] == Operatore:
                resp = make_response(render_template('/HomeOperatore.html'))
            elif login[0]["ruolo"] == UtentePro or login[0]["ruolo"] == UtenteSemplice:
                resp = make_response(render_template("/HomeUser.html"))

            resp.set_cookie('username', login[0]["_id"])
            resp.set_cookie('ruolo', login[0]["ruolo"])
            resp.set_cookie('dataIns', login[0]["dataInserimento"].date().strftime("%Y-%m-%d"))
            resp.set_cookie('flag', str(login[0]['flag']))

            if [login[0]["_id"], login[0]["ruolo"]] not in regUsers:
                regUsers.append([login[0]["_id"], login[0]["ruolo"]])
                print(regUsers)

            return resp
    else:
        ob = {}
        ob['check'] = False
        return jsonify(ob)

        #return redirect(request.url)
#home
@app.route('/home.html', methods=['GET'])
def main_home():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')

    if ruolo not in [Amministratore, Master, Leader, Operatore, UtenteSemplice, UtentePro]:
        return make_response(render_template("index.html"))
    elif ruolo == Amministratore or ruolo == Master:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'Home.html')
    elif ruolo == Operatore:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'HomeOperatore.html')
    elif ruolo == Leader:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'homeLeader.html')
    elif ruolo == UtenteSemplice or ruolo == UtentePro:
        return AnnullaTuttoVaiLogIn(username, ruolo, data, flag, 'HomeUser.html')
    else:
        return make_response(render_template("index.html"))

@app.route('/getProvince', methods=['GET'])
def getProvince():
    #prendo comunque i cookie
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')

    if ([username, ruolo] not in regUsers) or (Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        province = gestore.getProvince()
        jsonlist = []
        for element in province:
            if element != None and element!='':
                ob = {}
                ob['provincia'] = element
                jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/getComuni', methods=['GET'])
def getComuni():
    # prendo comunque i cookie
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')

    if ([username, ruolo] not in regUsers) or (Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        comuni = gestore.getComuni(request.args.get('provincia'))
        jsonlist = []
        for element in comuni:
            ob = {}
            ob['comune'] = element['Comune']
            jsonlist.append(ob)

        return jsonify(jsonlist)

@app.route('/Contatti.html', methods=['GET'])
def Contatti():
    # prendo comunque i cookie
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')

    if ([username, ruolo] not in regUsers) or (Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        resp = make_response(render_template("/Contatti.html"))
        return resp

@app.route('/GestioneDocumento.html', methods=['GET'])
def getGestioneDocumento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    #controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, Operatore]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Documento/GestioneDocumento.html'))
        elif ruolo == Leader:
            resp = make_response(render_template('/Documento/GestioneDocumentiLeader.html'))
        elif ruolo == Operatore:
            resp = make_response(render_template('/Documento/GestioneDocumentoOperatore.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

@app.route('/GestioneMateriali.html', methods=['GET'])
def getGestioneMateriale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    #controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, Operatore]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Materiale/GestioneMateriali.html'))
        elif ruolo == Leader:
            resp = make_response(render_template('/Materiale/GestioneMateriali.html'))
        elif ruolo == Operatore:
            resp = make_response(render_template('/Materiale/GestioneMaterialiOperatore.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

@app.route('/GestioneProva.html', methods=['GET'])
def getGestioneProve():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, Operatore]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Prova/GestioneProva.html'))
        elif ruolo == Leader:
            resp = make_response(render_template('/Prova/GestioneProva.html'))
        elif ruolo == Operatore:
            resp = make_response(render_template('/Prova/GestioneProvaOperatore.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

@app.route('/GestioneStrutture.html', methods=['GET'])
def getGestioneStruttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, Operatore]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Struttura/GestioneStrutture.html'))
        elif ruolo == Leader:
            resp = make_response(render_template('/Struttura/GestioneStrutture.html'))
        elif ruolo == Operatore:
            resp = make_response(render_template('/Struttura/GestioneStruttureOperatore.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

@app.route('/GestioneUtente.html', methods=['GET'])
def getGestioneUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Utente/GestioneUtente.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

@app.route('/Ricerca.html', methods=['GET'])
def getRicerca():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, UtenteSemplice, UtentePro]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Ricerca/Ricerca_ad.html'))
        elif ruolo == Leader or ruolo==UtentePro:
            resp = make_response(render_template('/Ricerca/Ricerca_ad_Leader.html'))
        elif ruolo == UtenteSemplice:
            resp = make_response(render_template('/Ricerca/ricerca.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/Report.html', methods=['GET'])
def getReport():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, UtenteSemplice, UtentePro]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master or ruolo == UtenteSemplice or ruolo == UtentePro:
            resp = make_response(render_template('/Report/Report.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

### GESTIONE DOCUMENTO
@app.route('/FormInserimentoDocumento.html', methods=['GET'])
def main_Documento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, Operatore]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master or ruolo == Leader or ruolo == Operatore:
            resp = make_response(render_template('/Documento/FormInserimentoDocumento.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/EliminazioneDocumento.html', methods=['GET'])
def main_eliminazione():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Documento/EliminazioneDocumento.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/check_esistenza', methods=['GET'])
def check_esistenza_documento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        pratica = request.args.get('NumeroPratica')
        gestore = GestoreForWrite()
        esito = gestore.checkEsistenza(pratica)
        ob = {}
        ob['esito'] = esito
        return jsonify(ob)

@app.route('/FormInserimentoDocumento.html', methods=['POST'])
def upload_file():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        print(request.form)
        numeroDocumenti = int(request.form['NumCertificati'])
        documento_apertura = request.files['Documento_apertura']
        documento_foglio = request.files['Documento_foglio_lavoro']
        if documento_apertura:
            documento_apertura.filename = request.form['TextPratica'] + "_apertura" + ".pdf"
            documento_apertura.filename = secure_filename(documento_apertura.filename)
        if documento_foglio:
            documento_foglio.filename = request.form['TextPratica'] + "_foglio_lavoro" + ".pdf"
            documento_foglio.filename = secure_filename(documento_foglio.filename)

        gestore = GestoreForWrite()
        esitoDocumento = gestore.buildDocument(request.form['TextPratica'],
                                               datetime.datetime.strptime(request.form['day'], '%Y-%m-%d'),
                                               request.form['Committente'],
                                               request.form['Descrizione'], request.form['Provincia'],
                                               request.form['Comune'],
                                               request.form['AltroLuogo'], int(request.form['NumCertificati']),
                                               documento_apertura, documento_apertura.filename,
                                               documento_foglio, documento_foglio.filename)
        # significa ok
        if esitoDocumento == 0:
            esito_cert = True
            if numeroDocumenti > 1:
                index = 0
                while (esito_cert and index < numeroDocumenti):
                    certificato = request.files['Certificato' + str(index)]
                    certificato.filename = request.form['TextPratica'] + '_' + request.form[
                        'Lettera' + str(index)].upper() + '.pdf'
                    certificato.filename = secure_filename(certificato.filename)
                    esito_cert = gestore.buildCertificato(request.form['TextPratica'],
                                                          request.form['Lettera' + str(index)].upper(),
                                                          request.form['Struttura' + str(index)],
                                                          request.form['Materiale' + str(index)],
                                                          request.form['Prova' + str(index)], certificato,
                                                          certificato.filename)
                    index = index + 1

            else:
                certificato = request.files['Certificato' + str(0)]
                certificato.filename = request.form['TextPratica'] + '_' + 'unique' + '.pdf'
                certificato.filename = secure_filename(certificato.filename)
                esito_cert = gestore.buildCertificato(request.form['TextPratica'], 'unique',
                                                      request.form['Struttura' + str(0)],
                                                      request.form['Materiale' + str(0)],
                                                      request.form['Prova' + str(0)], certificato, certificato.filename)

            ob = {}
            ob['check'] = esito_cert
            return jsonify(ob)

        elif esitoDocumento == 1:
            ob = {}
            ob['check'] = False
            return jsonify(ob)
        else:
            ob = {}
            ob['check'] = False
            return jsonify(ob)

@app.route('/download', methods=['GET'])
def download_documento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        file = request.args.get('file')
        file = secure_filename(file)
        grid_fs_file = gestore.download(file)
        response = make_response(grid_fs_file.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(request.args.get('file'))
        return response

@app.route('/GetCertificati', methods=['GET'])
def getCertificati():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        pratica = request.args.get('NumeroPratica')
        gestore = GestoreForWrite()
        certificati = gestore.getCertificati(pratica)
        jsonlist = []
        for element in certificati:
            ob = {}
            ob['_id'] = (element['_id']['NumeroPratica']) if element['_id']['Lettera'] == "unique" else (
                        element['_id']['NumeroPratica'] + '/' + element['_id']['Lettera'])
            ob['struttura'] = element['struttura']
            ob['materiale'] = element['materiale']
            ob['prova'] = element['prova']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/DeleteDocument', methods=['GET'])
def eliminaDocumento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo== Master:
            gestore = GestoreForWrite()
            esito = gestore.deleteDocument(request.args.get('Pratica'))
            ob = {}
            ob['esito'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/ModificaDocumento.html', methods=['GET'])
def main_modificaPratica():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader, Operatore]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Documento/ModificaDocumento.html'))
        elif ruolo == Operatore:
            resp = make_response(render_template('/Documento/ModificaDocumentoOperatore.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/trovaDocumento', methods=['GET'])
def findDocumento():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        documento = gestore.findDocumento(request.args.get('NumeroPratica'))
        ob = {}
        ob['_id'] = documento[0]['_id']
        ob['data'] = documento[0]['data'].date().strftime("%Y-%m-%d")
        ob['committente'] = documento[0]['committente']
        ob['descrizione'] = documento[0]['descrizione']
        ob['altroLuogo'] = documento[0]['altroLuogo']
        ob['provincia'] = documento[0]['provincia']
        ob['comune'] = documento[0]['comune']
        return jsonify(ob)

@app.route('/UpdateDocumento', methods=['PUT'])
def updateDocumnto():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        esito = gestore.updateDocumnto(request.form['NumeroPratica'], request.form['committente'],
                                       request.form['descrizione'], request.form['altroLuogo'],
                                       datetime.datetime.strptime(request.form['data'], '%Y-%m-%d'),
                                       request.form['provincia'], request.form['comune'])
        ob = {}
        ob['check'] = esito
        return jsonify(ob)

@app.route('/trovaFoglioLavoro', methods=['GET'])
def trovaFoglioLavoro():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        foglio = gestore.trovaFoglioLavoro(request.args.get('NumeroPratica'))
        ob = {}
        ob['lavori_name'] = foglio[0]['lavori_name']
        return jsonify(ob)

@app.route('/trovaFoglioApertura', methods=['GET'])
def trovaFoglioApertura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        foglio = gestore.trovaFoglioApertura(request.args.get('NumeroPratica'))
        ob = {}
        ob['apertura_name'] = foglio[0]['apertura_name']
        return jsonify(ob)

@app.route('/ModificaFoglioLavoro', methods=['POST'])
def uploadFoglio():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        documento = request.files['Documento_foglio_lavoro']
        documento.filename = request.form['TextPratica'] + "_foglio_lavoro" + ".pdf"
        documento.filename = secure_filename(documento.filename)
        esito = gestore.uploadFoglioLavoro(request.form['TextPratica'], documento)
        ob = {}
        ob['check'] = esito
        return jsonify(ob)

@app.route('/ModificaFoglioApertura', methods=['POST'])
def uploadApertura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        documento = request.files['Documento_foglio_apertura_pratica']
        documento.filename = request.form['TextPratica'] + "_apertura" + ".pdf"
        documento.filename = secure_filename(documento.filename)
        esito = gestore.uploadFoglioApertura(request.form['TextPratica'], documento)
        ob = {}
        ob['check'] = esito
        return jsonify(ob)

@app.route('/NuovoCertificato', methods=['POST'])
def newCertificato():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        numeroDocumenti = int(request.form['NumCertificati'])
        esito_cert = True
        index = 0
        gestore = GestoreForWrite()
        while (esito_cert and index < numeroDocumenti):
            certificato = request.files['Certificato' + str(index)]
            certificato.filename = request.form['TextPratica'] + '_' + request.form[
                'Lettera' + str(index)].upper() + '.pdf'
            certificato.filename = secure_filename(certificato.filename)
            esito_cert = gestore.buildCertificato(request.form['TextPratica'],
                                                  request.form['Lettera' + str(index)].upper(),
                                                  request.form['Struttura' + str(index)],
                                                  request.form['Materiale' + str(index)],
                                                  request.form['Prova' + str(index)], certificato, certificato.filename)
            index = index + 1

        gestore.updateNumCertificati(request.form['TextPratica'], numeroDocumenti)
        ob = {}
        ob['check'] = esito_cert
        ob['num'] = index
        return jsonify(ob)

### GESTIONE MATERIALE -> ok
@app.route('/check_esistenza_materiale', methods=['GET'])
def check_esistenza_materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        materiale = request.args.get('Materiale')
        gestore = GestoreForWrite()
        esito = gestore.checkEsistenzaMateriale(materiale)
        ob = {}
        ob['esito'] = esito
        return jsonify(ob)

@app.route('/EliminaMateriale.html', methods=['GET'])
def get_EliminaMateriale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo ==   Amministratore or ruolo == Master or ruolo==Leader:
            resp = make_response(render_template('/Materiale/EliminaMateriale.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/ModificaMateriale.html', methods=['GET'])
def get_modifica_Materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader]:
            resp = make_response(render_template('/NoPermesso.html'))
        elif ruolo ==   Amministratore or ruolo == Master or ruolo==Leader:
            resp = make_response(render_template('/Materiale/ModificaMateriale.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/get_single_materiale', methods=['GET'])
def get_single_materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        mat = request.args.get('Materiale')
        gestore = GestoreForWrite()
        element = gestore.get_single_materiale(mat)
        ob = {}
        ob['esito'] = True
        ob['id'] = element[0]["_id"]
        ob['descr'] = element[0]["descrizione"]
        return jsonify(ob)

@app.route('/deleteMateriale', methods=['GET'])
def eliminaMateriale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            gestore = GestoreForWrite()
            esito = gestore.eliminaMateriale(request.args.get('elemento'))
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/ModificaMateriale.html', methods=['POST'])
def update_Materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            oldMateriale = request.form['TipologiadiMateriale']
            newMateriale = request.form['NewCodiceMateriale']
            newDesc = request.form['NewDescrizione']
            gestore = GestoreForWrite()
            esito = gestore.update_Materiale(oldMateriale, newMateriale, newDesc)
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/getMateriale', methods=['GET'])
def getMateriale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getMateriale()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['materiale'] = element['_id']
            jsonlist.append(ob)
        return jsonify(jsonlist)

@app.route('/FormInserimentoMateriale.html', methods=['GET'])
def main_Materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader]:
            resp = make_response(render_template('/NoPermesso.html'))
        else:
            resp = make_response(render_template('/Materiale/FormInserimentoMateriale.html'))

        return resp

@app.route('/FormInserimentoMateriale.html', methods=['POST'])
def upload_materiale():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo not in [Amministratore, Master, Leader]:
            return make_response(render_template('/NoPermesso.html'))
        else:
            gestore = GestoreForWrite()
            esito = gestore.buildMateriale(request.form['TipoMateriale'], request.form['DescrizioneMateriale'])
            ob = {}
            ob['check'] = esito
            return jsonify(ob)

@app.route('/getMaterialeWithDesc', methods=['GET'])
def getMaterialewithDesc():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
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

### GESTIONE PROVA --> ok
@app.route('/check_esistenza_prova', methods=['GET'])
def check_esistenza_prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        prova = request.args.get('Prova')
        gestore = GestoreForWrite()
        esito = gestore.checkEsistenzaProva(prova)
        ob = {}
        ob['esito'] = esito
        return jsonify(ob)

@app.route('/EliminaProva.html', methods=['GET'])
def EliminaProva():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Prova/EliminaProva.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/ModificaProva.html', methods=['GET'])
def get_modifica_prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Prova/ModificaProva.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/getProvaWithDesc', methods=['GET'])
def getProvaWithDesc():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
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

@app.route('/get_single_prova', methods=['GET'])
def get_single_prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        prova = request.args.get('Prova')
        gestore = GestoreForWrite()
        element = gestore.get_single_prova(prova)
        ob = {}
        ob['esito'] = True
        ob['id'] = element[0]["_id"]
        ob['descr'] = element[0]["descrizione"]
        return jsonify(ob)

@app.route('/FormInserimentoProva.html', methods=['GET'])
def main_Prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Prova/FormInserimentoProva.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/FormInserimentoProva.html', methods=['POST'])
def upload_prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            gestore = GestoreForWrite()
            esito = gestore.buildTipoProva(request.form['TipologiaProva'], request.form['DescrizioneProva'])
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/deleteProva', methods=['GET'])  # trasformare in get
def eliminaProva():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            gestore = GestoreForWrite()
            esito = gestore.eliminaProva(request.args.get('elemento'))
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/ModificaProva.html', methods=['POST'])
def update_prova():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            oldProva = request.form['TipologiadiProva']
            newProva = request.form['NewCodiceProva']
            newDesc = request.form['NewDescrizione']
            gestore = GestoreForWrite()
            esito = gestore.update_Prova(oldProva, newProva, newDesc)
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/getProva', methods=['GET'])
def getProva():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        strutture = gestore.getProva()
        jsonlist = []
        for element in strutture:
            ob = {}
            ob['tipoProva'] = element['_id']
            jsonlist.append(ob)
        return jsonify(jsonlist)

### GESTIONE STRUTTURA ---> ok
@app.route('/EliminaStruttura.html', methods=['GET'])
def get_EliminaStruttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Struttura/EliminaStruttura.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/ModificaStruttura.html', methods=['GET'])
def get_modifica_Struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Struttura/ModificaStruttura.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))

        return resp

@app.route('/check_esistenza_struttura', methods=['GET'])
def check_esistenza_struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        struttura = request.args.get('Struttura')
        gestore = GestoreForWrite()
        esito = gestore.checkEsistenzaStruttura(struttura)
        ob = {}
        ob['esito'] = esito
        return jsonify(ob)

@app.route('/get_single_struttura', methods=['GET'])
def get_single_struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        struttura = request.args.get('Struttura')
        gestore = GestoreForWrite()
        element = gestore.get_single_struttura(struttura)

        ob = {}
        ob['esito'] = True
        ob['id'] = element[0]["_id"]
        ob['descr'] = element[0]["descrizione"]
        return jsonify(ob)

@app.route('/FormInserimentoStruttura.html', methods=['GET'])
def main_Struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            resp = make_response(render_template('/Struttura/FormInserimentoStruttura.html'))
        else:
            resp = make_response(render_template('/NoPermesso.html'))
        return resp

@app.route('/FormInserimentoStruttura.html', methods=['POST'])
def upload_struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            gestore = GestoreForWrite()
            esito = gestore.buildTipologiaStruttura(request.form['TipologiadiStruttura'],
                                                    request.form['Descrizionestruttura'])
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/deleteStruttura', methods=['GET'])
def eliminaStruttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            gestore = GestoreForWrite()
            esito = gestore.eliminaStruttura(request.args.get('elemento'))
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/ModificaStruttura.html', methods=['POST'])
def update_Struttura():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master or ruolo == Leader:
            oldStruttura = request.form['TipologiadiStruttura']
            newStruttura = request.form['NewCodiceStruttura']
            newDesc = request.form['NewDescrizione']
            gestore = GestoreForWrite()
            esito = gestore.update_Struttura(oldStruttura, newStruttura, newDesc)
            ob = {}
            ob['check'] = esito
            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/getStrutture', methods=['GET'])
def getStrutture():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
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
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
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

### Gestione Utente ->
# trova un utente in generale -> ok
@app.route('/check_esistenza_utente', methods=['GET'])
def checkUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        ob = {}
        esito = gestore.checkEsistenzaUtente(request.args.get('CF').upper())
        ob['esito'] = esito
        return jsonify(ob)

# trova un utente attivo: ovvero data < 30 g e flag =true
@app.route('/check_esistenza_utente_attivo', methods=['GET'])
def checkUtente_attivo():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        ob = {}
        us = gestore.getSingleUser(request.args.get('CF').upper())
        if us.count() > 0 and not Scaduto(us[0]['dataInserimento'].date(), us[0]['flag']):
            ob['esito'] = True
        else:
            ob['esito'] = False
        return jsonify(ob)

@app.route('/GestioneUtente.html', methods=['GET'])
def gestioneUtenze():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master:
            resp = make_response(render_template('/Utente/GestioneUtente.html'))
        else:
            resp =  make_response(render_template('/NoPermesso.html'))
    return resp

@app.route('/NewUtente', methods=['POST'])
def newUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master:
            ob = {}
            gestore = GestoreForWrite()
            esito = gestore.addUtente(request.form['Nome'], request.form['Cognome'], request.form['Provincia'],
                                      request.form['Comune'], request.form['bday'],
                                      request.form['CodiceFiscale'].upper(),
                                      request.form['Password'], request.form['Ruolo'],
                                      request.form['Scadenza'] == "true",
                                      datetime.datetime.now(), True)
            if esito:
                ob['check'] = True
            else:
                ob['check'] = False

            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/updateUtente', methods=['PUT'])
def updateRole():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master:
            ob = {}
            gestore = GestoreForWrite()
            esito = gestore.updateUtente(request.form['CF'].upper(), request.form['ruolo'],
                                         request.form['Scade'] == "true", datetime.datetime.now())
            if esito:
                ob['check'] = True
            else:
                ob['check'] = False

            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/getUtenti', methods=['GET'])
def getUtenti():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master:
            gestore = GestoreForWrite()
            utenti = gestore.getUtenti()
            jsonlist = {}
            Scaduti = []
            Attivi = []
            for element in utenti:
                ob = {}
                ob['cf'] = element['_id']
                ob['ruolo'] = element['ruolo']
                ob['dataInserimento'] = element['dataInserimento'].date().strftime("%Y-%m-%d")
                ob['scadenza'] = element['scadenza']
                if not Scaduto(element['dataInserimento'].date(), element['flag']):
                    Attivi.append(ob)
                else:
                    Scaduti.append(ob)

            jsonlist['Attivi'] = Attivi
            jsonlist['Scaduti'] = Scaduti

            return jsonify(jsonlist)
        else:
            return make_response(render_template('/NoPermesso.html'))

# trova un utente inattivo: ovvero data > 30 g opp flag =false
@app.route('/check_esistenza_utente_inattivo', methods=['GET'])
def check_esistenza_utente_inattivo():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        ob = {}
        us = gestore.getSingleUser(request.args.get('CF').upper())
        print(us[0])
        if us.count() > 0 and Scaduto(us[0]['dataInserimento'].date(), us[0]['flag']):
            ob['esito'] = True
        else:
            ob['esito'] = False
        return jsonify(ob)

@app.route('/RiattivaUtente', methods=['PUT'])
def riattivaUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master:
            ob = {}
            gestore = GestoreForWrite()
            esito = gestore.riattivaUtente(request.form['CF'].upper(), datetime.datetime.now())
            if esito:
                ob['check'] = True
            else:
                ob['check'] = False

            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

@app.route('/DisattivaUtente', methods=['PUT'])
def disattivaUtente():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        if ruolo == Amministratore or ruolo == Master:
            ob = {}
            gestore = GestoreForWrite()
            esito = gestore.disattivaUtente(request.form['CF'].upper())
            if esito:
                ob['check'] = True
            else:
                ob['check'] = False

            return jsonify(ob)
        else:
            return make_response(render_template('/NoPermesso.html'))

### FUNZIONI DI RICERCA --> OK
@app.route('/DoquerybyPratica', methods=['GET'])
def doQuerybyPratica():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        ob = {}
        gestore = GestoreForWrite()
        print(request.args.get('NumeroPratica'))
        doc = gestore.DoQuerybyPratica(request.args.get('NumeroPratica'))
        lResult = []
        print(doc.count())
        num = 0
        for element in doc:
            # potrebbe non esserci il file di apertura
            if element['apertura_name'] is not "":
                oggetto = {}
                oggetto['Rif'] = element["_id"]
                oggetto['Tipologia'] = 'apertura pratica'
                oggetto['Committente'] = element['committente']
                oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                oggetto['provincia'] = element['provincia']
                oggetto['comune'] = element['comune']
                oggetto['struttura'] = ""
                oggetto['materiale'] = ""
                oggetto['prova'] = ""
                lResult.append(oggetto)
                num = num + 1
            # potrebbe non esserci il file di foglio di lavoro
            if element['lavori_name'] is not "":
                oggetto = {}
                oggetto['Rif'] = element["_id"]
                oggetto['Tipologia'] = 'foglio di lavoro'
                oggetto['Committente'] = element['committente']
                oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                oggetto['provincia'] = element['provincia']
                oggetto['comune'] = element['comune']
                oggetto['struttura'] = ""
                oggetto['materiale'] = ""
                oggetto['prova'] = ""
                lResult.append(oggetto)
                num = num + 1

            query = {}
            query["_id.NumeroPratica"] = element["_id"]
            cert = gestore.DoQueryOnCertificato(query)
            if cert.count() > 0:
                for y in cert:
                    oggetto = {}
                    oggetto['Rif'] = (element["_id"]) if y['_id']['Lettera'] == 'unique' else (
                            element["_id"] + '/' + y['_id']['Lettera'])
                    oggetto['Tipologia'] = 'certificato'
                    oggetto['Committente'] = element['committente']
                    oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                    oggetto['provincia'] = element['provincia']
                    oggetto['comune'] = element['comune']
                    oggetto['struttura'] = y['struttura']
                    oggetto['materiale'] = y['materiale']
                    oggetto['prova'] = y['prova']
                    lResult.append(oggetto)

            num = num + cert.count()

        if ruolo == UtenteSemplice:
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
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
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
                    p['altroLuogo'] = {"$regex": parola, "$options": "i"}
                    appList.append(p)
                app["$or"] = appList
                list.append(app)
            if request.args.get('Committente') is not "":
                appList = []
                app = {}
                parole = request.args.get('Committente').split(' ')
                for parola in parole:
                    p = {}
                    p['committente'] = {"$regex": parola, "$options": "i"}
                    appList.append(p)
                app["$or"] = appList
                list.append(app)
            if request.args.get('Descrizione') is not "":
                appList = []
                app = {}
                parole = request.args.get('Descrizione').split(' ')
                for parola in parole:
                    p = {}
                    p['descrizione'] = {"$regex": parola, "$options": "i"}
                    appList.append(p)
                app["$or"] = appList
                list.append(app)
            if (len(list) > 0):
                ob['$and'] = list
                print(ob)
            doc = gestore.DoQueryOnDocument(ob)
            for element in doc:
                if element['apertura_name'] is not "":
                    oggetto = {}
                    oggetto['Rif'] = element["_id"]
                    oggetto['Tipologia'] = 'apertura pratica'
                    oggetto['Committente'] = element['committente']
                    oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                    oggetto['provincia'] = element['provincia']
                    oggetto['comune'] = element['comune']
                    oggetto['struttura'] = ""
                    oggetto['materiale'] = ""
                    oggetto['prova'] = ""
                    lResult.append(oggetto)
                    num = num + 1
                # potrebbe non esserci il file di foglio di lavoro
                if element['lavori_name'] is not "":
                    oggetto = {}
                    oggetto['Rif'] = element["_id"]
                    oggetto['Tipologia'] = 'foglio di lavoro'
                    oggetto['Committente'] = element['committente']
                    oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                    oggetto['provincia'] = element['provincia']
                    oggetto['comune'] = element['comune']
                    oggetto['struttura'] = ""
                    oggetto['materiale'] = ""
                    oggetto['prova'] = ""
                    lResult.append(oggetto)
                    num = num + 1
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
                        oggetto = {}
                        oggetto['Rif'] = (element["_id"]) if y['_id']['Lettera'] == 'unique' else (
                                element["_id"] + '/' + y['_id']['Lettera'])
                        oggetto['Tipologia'] = 'certificato'
                        oggetto['Committente'] = element['committente']
                        oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                        oggetto['provincia'] = element['provincia']
                        oggetto['comune'] = element['comune']
                        oggetto['struttura'] = y['struttura']
                        oggetto['materiale'] = y['materiale']
                        oggetto['prova'] = y['prova']
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
                    p['altroLuogo'] = {"$regex": parola, "$options": "i"}
                    listOr.append(p)
            if request.args.get('Committente') is not "":
                parole = request.args.get('Committente').split(' ')
                for parola in parole:
                    p = {}
                    p['committente'] = {"$regex": parola, "$options": "i"}
                    listOr.append(p)
            if request.args.get('Descrizione') is not "":
                parole = request.args.get('Descrizione').split(' ')
                for parola in parole:
                    p = {}
                    p['descrizione'] = {"$regex": parola, "$options": "i"}
                    listOr.append(p)
            app = {}
            if (len(listOr) > 0):
                app['$or'] = listOr
                list.append(app)
            if (len(list) > 0):
                ob['$and'] = list
                print(ob)
            doc = gestore.DoQueryOnDocument(ob)
            for element in doc:
                if element['apertura_name'] is not "":
                    oggetto = {}
                    oggetto['Rif'] = element["_id"]
                    oggetto['Tipologia'] = 'apertura pratica'
                    oggetto['Committente'] = element['committente']
                    oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                    oggetto['provincia'] = element['provincia']
                    oggetto['comune'] = element['comune']
                    oggetto['struttura'] = ""
                    oggetto['materiale'] = ""
                    oggetto['prova'] = ""
                    lResult.append(oggetto)
                    num = num + 1
                # potrebbe non esserci il file di foglio di lavoro
                if element['lavori_name'] is not "":
                    oggetto = {}
                    oggetto['Rif'] = element["_id"]
                    oggetto['Tipologia'] = 'foglio di lavoro'
                    oggetto['Committente'] = element['committente']
                    oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                    oggetto['provincia'] = element['provincia']
                    oggetto['comune'] = element['comune']
                    oggetto['struttura'] = ""
                    oggetto['materiale'] = ""
                    oggetto['prova'] = ""
                    lResult.append(oggetto)
                    num = num + 1
                query = {}
                list = []
                listOr = []
                app = {}
                app["_id.NumeroPratica"] = element["_id"]
                list.append(app)
                if request.args.get('Materiale') is not "":
                    app = {}
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
                if (len(listOr) > 0):
                    app['$or'] = listOr
                    list.append(app)
                query["$and"] = list
                print(query)
                cert = gestore.DoQueryOnCertificato(query)
                if cert.count() > 0:
                    for y in cert:
                        oggetto = {}
                        oggetto['Rif'] = (element["_id"]) if y['_id']['Lettera'] == 'unique' else (
                                element["_id"] + '/' + y['_id']['Lettera'])
                        oggetto['Tipologia'] = 'certificato'
                        oggetto['Committente'] = element['committente']
                        oggetto['data'] = element['data'].date().strftime("%Y-%m-%d")
                        oggetto['provincia'] = element['provincia']
                        oggetto['comune'] = element['comune']
                        oggetto['struttura'] = y['struttura']
                        oggetto['materiale'] = y['materiale']
                        oggetto['prova'] = y['prova']
                        lResult.append(oggetto)

                num = num + cert.count()

        if ruolo == UtenteSemplice:
            result = {}
            result["num"] = num
            return jsonify(result)
        else:
            return jsonify(lResult)



### FUNZIONE DI REPORT --> OK
#document by year
@app.route('/DoquerybyAnno', methods=['GET'])
def queryByYear():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        result = gestore.queryByYear()
        tab = pd.DataFrame()
        for r in result:
            tab = tab.append({"date": r['_id'],
                              "conteggio": r['count']}, ignore_index=True)

        lResult = []
        tab = tab.set_index('date')
        x = tab.resample('10A').sum().reset_index()
        for i in range(0, x.shape[0]):
            ob = {}
            ob['name'] = x.loc[i].date.date().year
            ob['conteggio'] = x.loc[i].conteggio
            lResult.append(ob)
        return jsonify(lResult)

#group by materiali
@app.route('/DoquerybyMateriale', methods=['GET'])
def doQueryByMateriali():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        result = gestore.doQueryByMateriali()
        lResult = []
        for r in result:
            ob = {}
            ob['name'] = r['_id']
            ob['conteggio'] = r['count']
            lResult.append(ob)
        return jsonify(lResult)

#group by strutture
@app.route('/DoquerybyStruttura', methods=['GET'])
def doQueryByStrutture():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        result = gestore.doQueryByStrutture()
        lResult = []
        for r in result:
            ob = {}
            ob['name'] = r['_id']
            ob['conteggio'] = r['count']
            lResult.append(ob)
        return jsonify(lResult)

#group by prove
@app.route('/DoquerybyProve', methods=['GET'])
def doQueryByProve():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo] not in regUsers) or (
            Scaduto(datetime.datetime.strptime(data, "%Y-%m-%d").date(), bool(flag))):
        if [username, ruolo] in regUsers:
            regUsers.remove([username, ruolo])

        resp = make_response(render_template("index.html"))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('ruolo', '', expires=0)
        resp.set_cookie('dataIns', '', expires=0)
        resp.set_cookie('flag', '', expires=0)
        return resp
    else:
        gestore = GestoreForWrite()
        result = gestore.doQueryByProve()
        lResult = []
        for r in result:
            ob = {}
            ob['name'] = r['_id']
            ob['conteggio'] = r['count']
            lResult.append(ob)
        return jsonify(lResult)

@app.route('/logOut', methods=['GET'])
def logOut():
    username = request.cookies.get('username')
    ruolo = request.cookies.get('ruolo')
    data = request.cookies.get('dataIns')
    flag = request.cookies.get('flag')
    # controllo scadenza ed esistenza del ruolo
    if ([username, ruolo]  in regUsers):
        regUsers.remove([username, ruolo])

    resp = make_response(redirect('/'))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('ruolo', '', expires=0)
    resp.set_cookie('dataIns', '', expires=0)
    resp.set_cookie('flag', '', expires=0)
    return resp


if __name__ == "__main__":
    app.run(port=5002)
