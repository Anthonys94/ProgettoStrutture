from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from Model.gestore import *
#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    #dao = daoGestore()
    #dao.readMaterial()
    return render_template('index.html')

@app.route('/',methods=['POST'])
def main_post():
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
        gestore = Gestore()
        gestore.buildMateriale(newMaterial)
    return render_template('home.html')

@app.route('/FormInserimentoProva.html',methods=['GET'])
def main_Prova():
    return render_template('FormInserimentoProva.html')

@app.route('/FormInserimentoStruttura.html',methods=['GET'])
def main_Struttura():
    return render_template('FormInserimentoStruttura.html')

@app.route('/FormInserimentoDocumento.html',methods=['GET'])
def main_Documento():
    return render_template('FormInserimentoDocumento.html')

if __name__ == "__main__":
    app.run(port=5002)
