import os
import urllib.request
from flask import Flask, flash, render_template, json, request, redirect
from Model.gestore import *
from flask import jsonify
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from gridfs import GridFS
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)

UPLOAD_FOLDER = '/Users/antonio/Downloads'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

#class ReusableForm(Form):
    #items = TextAreaField('Item:', validators=[validators.required()])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    # dao = daoGestore()
    # dao.readMaterial()
    return render_template('index.html')


@app.route('/', methods=['POST'])
def main_post_login():
    _name = request.form['email']
    _email = request.form['pass']
    print(_name)
    print(_email)
    return render_template('home.html')


@app.route('/FormInserimentoMateriale.html', methods=['GET'])
def main_Materiale():
    return render_template('FormInserimentoMateriale.html')


@app.route('/FormInserimentoMateriale.html', methods=['POST'])
def upload_Materiale():
    newMaterial = request.form['TipoMateriale']
    if newMaterial == '':
        print('vuoto')
    else:
        gestore = GestoreForWrite()
        gestore.buildMateriale(newMaterial)
    return render_template('home.html')


@app.route('/FormInserimentoProva.html', methods=['GET'])
def main_Prova():
    return render_template('FormInserimentoProva.html')


@app.route('/FormInserimentoProva.html', methods=['POST'])
def upload_prova():
    newProva = request.form['TipologiaProva']
    if newProva == '':
        print('vuoto')
    else:
        gestore = GestoreForWrite()
        gestore.buildTipoProva(newProva)
        return render_template('home.html')


@app.route('/FormInserimentoStruttura.html', methods=['GET'])
def main_Struttura():
    return render_template('FormInserimentoStruttura.html')


@app.route('/FormInserimentoStruttura.html', methods=['POST'])
def upload_struttura():
    newStruttura = request.form['TipologiadiStruttura']
    if newStruttura == '':
        print('vuoto')
    else:
        descrizione = request.form['Descrizionestruttura']
        gestore = GestoreForWrite()
        gestore.buildTipologiaStruttura(newStruttura, descrizione)
        return render_template('home.html')


@app.route('/FormInserimentoDocumento.html', methods=['GET'])
def main_Documento():
    return render_template('FormInserimentoDocumento.html')

@app.route('/FormInserimentoDocumento.html', methods=['POST'])
def upload_file():
    print(request.form)
    print(request.files)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            gestore = GestoreForWrite()
            gestore.buildDocument(request.form['TextPratica'], request.form['bday'], request.form['Committente'],
                                  request.form.getlist('Luoghi[]'), request.form.getlist('Province[]'), request.form['Descrizione'],
                                  request.form['Strutture'], request.form['Prova'],
                                  request.form['Materiale'], file, filename)


            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #flash('File successfully uploaded')

            return render_template('home.html')

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


@app.route('/getStrutture', methods=['GET'])
def getStrutture():
    gestore = GestoreForWrite()
    strutture = gestore.getStrutture()
    jsonlist = []
    for element in strutture:
        ob = {}
        ob['tipologiaStruttura'] = element['tipologiaStruttura']
        ob['descrizione'] = element['descrizione']
        jsonlist.append(ob)
    return jsonify(jsonlist)

@app.route('/getProva', methods=['GET'])
def getProva():
    gestore = GestoreForWrite()
    strutture = gestore.getProva()
    jsonlist = []
    for element in strutture:
        ob = {}
        ob['tipoProva'] = element['tipoProva']
        jsonlist.append(ob)
    return jsonify(jsonlist)

@app.route('/getMateriale', methods=['GET'])
def getMateriale():
    gestore = GestoreForWrite()
    strutture = gestore.getMateriale()
    jsonlist = []
    for element in strutture:
        ob = {}
        ob['materiale'] = element['materiale']
        jsonlist.append(ob)
    return jsonify(jsonlist)

if __name__ == "__main__":
    app.run(port=5002)
