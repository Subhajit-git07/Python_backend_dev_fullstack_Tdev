import time
import pymongo
from config import settings
import time 
from loggerUtil import logger

class MongoFunctions:
	def getCollectionDB(self, collection):
		return collection.get_collection(collection)
	
	def insertOneDB(self, collection, filter: object, projection = {}):
		collection.insert_one(filter, projection)

	def findOneDB(self, collection, filter: object, projection = {}):
		return collection.find_one(filter, projection)

	def findManyDBComplex(self, collection, filter: object, projection = {}):
		time.sleep(1)
		batchSize = 100000
		ss = time.time()
		total_ru = 0
		totalData = []
		data = list(collection.find(filter, projection).sort("_id", 1).limit(batchSize))
		totalData += data
		while len(data) != 0:
			time.sleep(1.0)
			last_id = data[-1]["_id"]
			filter["_id"] = {"$gt": last_id}
			data = list(collection.find(filter, projection).sort("_id", 1).limit(batchSize))
			totalData += data
			currRU = (collection.database.command('getLastRequestStatistics')['RequestCharge'])
            # print(currRU)
			total_ru += currRU
		print("Logs, time: ",(time.time()-ss)," Total RU: ", total_ru, " Len of Array: ",len(totalData))
		return totalData

	def findManyDB(self, collection, filter: object, projection = {}):
		return collection.find(filter, projection)

	def deleteOneDB(self, collection, filter: object): # tested
		collection.delete_one(filter)
		
	def deleteManyDB(self, collection, filter: object): # TESTED
		collection.delete_many(filter)

	def updateOneDB(self, collection, filter: object, projection = {}):
		return collection.update_one(filter, projection)
	
	def updateManyDB(self, collection, filter: object, projection = {}):
		return collection.update_many(filter, projection)

	def findOneUpdateDB(self, collection, filter: object, projection = {}):
		return collection.find_one_and_update(filter, projection)

	def selectDistinctDB(self, collection, filter: object, projection = {}):
		return collection.distinct(filter, projection)

	def countDB(self, collection, filter: object): #Tested
		return collection.count_documents(filter)

	def getDistinctDB(self, collection, filter: object, projection = {}):
		return collection.distinct(filter, projection)
	
	def getDistinctDBCursor(self, cursor, filter: object):
		return cursor.distinct(filter)

	def aggregateDB(self, collection, filter: object):
		return collection.aggregate(filter)
	
	def getCostofCall(self, collection):
		return collection.database.command('getLastRequestStatistics')['RequestCharge']

	def deleteManualDB(self, collection, filter: object, batchSize = 27):
		time.sleep(1)
		ss = time.time()
		total_ru = 0
		totalData = 0
		data = list(collection.find(filter, {"_id": 1}).sort("_id", 1).limit(batchSize))
		totalData += len(data)
		log_lastFilter = filter
		while len(data) != 0:
			time.sleep(1.0)
			collection.delete_many(filter | {"_id": {"$lte": data[-1]['_id']}})
			# Cost of delete
			total_ru += (collection.database.command('getLastRequestStatistics')['RequestCharge'])
			log_lastFilter = log_lastFilter | {"_id": {"$gt": data[-1]['_id']}}
			data = list(collection.find(filter | {"_id": {"$gt": data[-1]['_id']}}, {"_id": 1}).sort("_id", 1).limit(batchSize))
			# Cost of find
			total_ru += (collection.database.command('getLastRequestStatistics')['RequestCharge'])
			totalData += len(data)
		logger.info(f"Cosmos DB:{collection.name} Delete time: {time.time()-ss:.2f} secs; documents count: {totalData}; RU Cost: {total_ru:.2f}; filter: {log_lastFilter}")
		# print(f"Cosmos DB:{collection.name} Delete time: {time.time()-ss:.2f} secs; documents count: {totalData}; RU Cost: {total_ru}")
		return totalData

class TADADB:
	
	def getUnclassifiedTxs(self):
		return self.tadaDB.get_collection("UnclassifiedTxs")
	
	def getClassifiedTxs(self):
		return self.tadaDB.get_collection("ClassifiedTxs")

	def getClients(self):
		return self.tadaDB.get_collection("Clients")
	
	def getFormData(self):
		return self.tadaDB.get_collection("FormData")
	
	def getFormDataTotals(self):
		return self.tadaDB.get_collection("FormDataTotals")

	def getHoldings(self):
		return self.tadaDB.get_collection("Holdings")

	def getStatuses(self):
		return self.tadaDB.get_collection("Statuses")
	
	def getTokens(self):
		return self.tadaDB.get_collection("Tokens")
	
	def getUsers(self):
		return self.tadaDB.get_collection("Users")
	
	def getWallets(self):
		return self.tadaDB.get_collection("Wallets")

class MetaDataDB:

	def getBlockchains(self):
		return self.metaDB.get_collection("Blockchains")

	def getClassificationLogic(self):
		return self.metaDB.get_collection("ClassificationLogic")
	
	def getFormConfigs(self):
		return self.metaDB.get_collection("FormConfigs")
	
	def getIconMapping(self):
		return self.metaDB.get_collection("IconMapping")
	
	def getPdfFormGeneration(self):
		return self.metaDB.get_collection("PdfFormGeneration")
	
	def getExchanges(self):
		return self.metaDB.get_collection("Exchanges")
	
	def getStatesByCountries(self):
		return self.metaDB.get_collection("StatesByCountries")

class DBSettings(MongoFunctions, TADADB, MetaDataDB):
	def __init__(self):
		connect = settings.cdbAccessKey
		self.client = pymongo.MongoClient(connect, uuidRepresentation="standard")
		self.metaDB = self.client.get_database("MetaDataDB")
		self.tadaDB = self.client.get_database("TADADB")
		# self.tadaDB.get_collection("ClassifiedTxs").find().

dbSet = DBSettings()