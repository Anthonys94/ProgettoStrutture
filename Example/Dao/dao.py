import json

db = '/Users/antonio/Desktop/Università/ProgettoTrasporti/db/'

class daoGestore:
    def __init__(self) -> None:
        super().__init__()

    def uploadDocumento(self, newDocument):

        with open(db+"documents.json", "a+") as documents:
            print(documents)
            json.dump(newDocument, documents)
            print(documents)


    def uploadStructure(self, structure):

        with open(db+"structures.json", "a+") as structures:
            print(structures)
            json.dump(structure, structures)
            print(structures)

    def uploadProva(self, prova):
        with open(db+"prove.json", "a+") as prove:
            print(prove)
            json.dump(prova, prove)
            print(prove)

    def uploadMaterial(self, material):
        with open(db+"materials.json", "a+") as materials:
            print(materials)
            json.dump(material, materials)
            print(materials)

    def readMaterial(self):
        print('hereeee')

        data = [json.loads(line) for line in open(db+"materials.json", "r")]
        print(data)
        with open(db+"materials.json", "r") as materials:
            m = json.load(materials)
            print(m)