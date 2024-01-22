import json
import os
import pymongo

class Settings:
	def __init__(self):
		self.cdbAccessKey = "mongodb://usndtaxtdacdb09:cfXF4GWmQyyabx2BUeOa7yVswC5tfXpMhltfQPgGFCaJQru15dIV3E8A5QaDfquRx6Awz7wO7LHrACDbUwFMfg%3D%3D@usndtaxtdacdb09.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@usndtaxtdacdb09@"

settings = Settings()

class DBcreationSettings:
	def __init__(self):
		connect = settings.cdbAccessKey
		self.client = pymongo.MongoClient(connect, uuidRepresentation="standard")

dbCreationSet = DBcreationSettings()

'''
# Create new index
DB = dbCreationSet.tadaDB
#DB.customers.create_index('name')

# Get indexes
print(DB.customers.index_information())

DB.customers.drop_index('name_1')
'''

# Create a new database
Tdb = dbCreationSet.client['TADADB']
Mdb = dbCreationSet.client['MetaDataDB']

tadaDB_collection_list = Tdb.list_collection_names()
metaDataDB_collection_list = Mdb.list_collection_names()


metaColList = ["Blockchains", "Exchanges", "FormConfigs", "PdfFormGeneration", "StatesByCountries"]
tadaColList = ["ClassifiedTxs", "Clients", "FormData", "FormDataTotals", "Holdings", "Statuses", "Tokens", "UnclassifiedTxs", "Users", "Wallets"]


for collection in metaColList:
	if collection not in metaDataDB_collection_list:
		coll = Mdb.create_collection(collection)
		
for collection in tadaColList:
	if collection not in tadaDB_collection_list:
		coll = Tdb.create_collection(collection)
		
StatesByCountries = Mdb["StatesByCountries"]
Blockchains = Mdb["Blockchains"]
FormConfigs = Mdb["FormConfigs"]
		
with open("StatesByCountries.json", "rb") as json_file:
	stateData = json.load(json_file)
if isinstance(stateData, list):
    StatesByCountries.insert_many(stateData) 
else:
    StatesByCountries.insert_one(stateData)
	
with open("Blockchains.json", "rb") as json_file:
	blockchainData = json.load(json_file)
if isinstance(blockchainData, list):
    Blockchains.insert_many(blockchainData) 
else:
    Blockchains.insert_one(blockchainData)

	
with open("FormConfigs.json", "rb") as json_file:
	formConfigsData = json.load(json_file)
if isinstance(formConfigsData, list):
    FormConfigs.insert_many(formConfigsData) 
else:
    FormConfigs.insert_one(formConfigsData)
	