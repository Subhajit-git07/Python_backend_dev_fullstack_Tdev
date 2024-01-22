import os
import time
import pymongo
from tqdm import tqdm

from Config import EnvSettings

class MongoFunctions:

    def getCollectionDB(self, collection):
        return collection.get_collection(collection)

    def insertOneDB(self, collection, filter: object, projection = {}):
        collection.insert_one(filter, projection)
    
    def insertManyDB(self, collection, filter: object, projection = {}):
        # Batched updated 
        for batch in tqdm(self.GenerateBatchedData(filter, batch_size=100), desc=f"Uploading docs(Total={len(filter)/100}): ", leave=False):
            collection.insert_many(batch)
            time.sleep(1.0)

    def findOneDB(self, collection, filter: object, projection = {}):
        return collection.find_one(filter, projection)

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
    
    def findOneUpdateDBWithReturn(self, collection, filter: object, return_document, projection = {}):
        return collection.find_one_and_update(filter, projection)

    def selectDistinctDB(self, collection, filter: object, projection = {}):
        return collection.distinct(filter, projection)

    def countDB(self, collection, filter: object): #Tested
        return collection.count_documents(filter)

    def getDistinctDB(self, collection, filter: object, projection = {}):
        return collection.distinct(filter, projection)

    def aggregateDB(self, collection, filter: object):
        return collection.aggregate(filter)

    def GenerateBatchedData(self, data, batch_size):
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            yield batch

class TADADB:

    def tadaUtility(self, collection_name):
        return self.tadaDB.get_collection(collection_name)

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

    def metaUtility(self, collection_name):
        return self.metaDB.get_collection(collection_name)

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


class DbSettings(MongoFunctions, TADADB, MetaDataDB):
    def __init__(self):
        cosmosConnectStr = os.getenv(EnvSettings.cdbAccessKey)
        self.client = pymongo.MongoClient(cosmosConnectStr, uuidRepresentation="standard")
        self.tadaDB = self.client.get_database("TADADB")
        self.metaDB = self.client.get_database("MetaDataDB")

dbSet = DbSettings()