from flask import Flask, render_template, json, request
from Model.gestore import *
#from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
def main():
    #dao = daoGestore()
    #dao.readMaterial()
    return render_template('index.html')

@app.route('/',methods=['POST'])
def main_post_login():
    _name = request.form['email']
    _email = request.form['pass']
    print(_name)
    print(_email)
    return render_template('home.html')

@app.route('/FormInserimentoMateriale.html',methods=['GET'])
def main_Materiale():
    return render_template('FormInserimentoMateriale.html')

@app.route('/FormInserimentoMateriale.html',methods=['POST'])
def upload_Materiale():
    newMaterial = request.form['TipoMateriale']
    if newMaterial == '':
        print('vuoto')
    else:
        gestore = GestoreForWrite()
        gestore.buildMateriale(newMaterial)
    return render_template('home.html')

@app.route('/FormInserimentoProva.html',methods=['GET'])
def main_Prova():
    return render_template('FormInserimentoProva.html')

@app.route('/FormInserimentoProva.html',methods=['POST'])
def upload_prova():
    newProva = request.form['TipologiaProva']
    if newProva=='':
        print('vuoto')
    else:
        gestore = GestoreForWrite()
        gestore.buildTipoProva(newProva)
        return render_template('home.html')


@app.route('/FormInserimentoStruttura.html',methods=['GET'])
def main_Struttura():
    return render_template('FormInserimentoStruttura.html')

@app.route('/FormInserimentoStruttura.html',methods=['POST'])
def upload_struttura():
    newStruttura = request.form['TipologiadiStruttura']
    if newStruttura=='':
        print('vuoto')
    else:
        descrizione = request.form['Descrizionestruttura']
        gestore = GestoreForWrite()
        gestore.buildTipologiaStruttura(newStruttura, descrizione)
        return render_template('home.html')



@app.route('/FormInserimentoDocumento.html',methods=['GET'])
def main_Documento():
    return render_template('FormInserimentoDocumento.html')

if __name__ == "__main__":
    app.run(port=5002)
