from pymongo import MongoClient
from gridfs import GridFS
import datetime

client = MongoClient('localhost', 27017)
db = client.Strutture
'''
filename = []
filename.append(db.documento.find({"_id": '1'})[0]['filename'])
cursor = db.certificato.find({"_id.NumeroPratica": '1'}, {"_id":0 ,"filename": 1})
for element in cursor:
    filename.append(element['filename'])
oggetti = db.fs.files.find({"filename":{"$in":filename}},{"_id":1})
print(filename)
obj = []
for o in oggetti:
    print(o)
    obj.append(o['_id'])

c = db.fs.chunks.find({"files_id":{"$in":obj}},{"_id":1})
for x in c:
    print(x)
client.close()
ob={}
list = []
list2 = []

parole = ['Prova', 'super']
ob2={}
ob2['altroLuogo'] = {"$regex": parole[0]}
list.append(ob2)
ob2={}
ob2['altroLuogo'] = {"$regex": parole[1]}
list.append(ob2)
app ={}
app['$or'] = list
list2.append(app)
list = []
ob2={}
ob2['committente'] = {"$regex": "Michela"}
list.append(ob2)
ob2={}
ob2['committente'] = {"$regex": "Prova"}
list.append(ob2)
app={}
app['$or'] = list
list2.append(app)
ob["$and"] = list2
print(ob)
province = db.documento.find(ob)
print(province.count())
for element in province:
    print(element)
client.close()

'''
import pandas as pd
import datetime
client = MongoClient('localhost', 27017)
db = client.Strutture
tab = pd.DataFrame()
result =db.documento.aggregate([{"$group": {"_id": "$data", "count": {"$sum":1}}}])
for r in result:
    tab = tab.append({"date": r['_id'],
                "conteggio": r['count']}, ignore_index=True)

print(tab)
tab = tab.set_index('date')


x = tab.resample('10A').sum()
app = x.reset_index()
print(app.shape[0])
print(app.loc[0].date.date())
client.close()