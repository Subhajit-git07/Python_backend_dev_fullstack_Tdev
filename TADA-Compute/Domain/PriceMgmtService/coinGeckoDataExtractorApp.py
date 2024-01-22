import json
import time
import datetime
from collections import defaultdict
from pymongo import ReturnDocument
from datetime import timezone
from datetime import timedelta
import pandas as pd
import html_to_json
import numpy as np

from Domain.PriceMgmtService.util import createTimestamp, createMonthNameMap, calculateTaxLiability
from Domain.PriceMgmtService.priceExtractor import priceExtractor
from Domain.PriceMgmtService.coinGeckoConfig import config, configMethods

from Infrastructure.dbMgmt import dbSet
from Infrastructure.blobMgmt import blobSet

from LoggerUtils import App_logger

def toUnixTimestamp(timestamp:str):
	d = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%SZ')
	unixtime =  time.mktime(d.timetuple())
	return unixtime

def unixtimeToDatetime(timestamp):
	d = datetime.datetime.fromtimestamp(timestamp)
	return d
	
def strTo_DateTimeObject(timeStamp, format):
	datetime_str = datetime.datetime.strptime(timeStamp, format)
	return datetime_str
	
def convert_HTML_to_JSON(data):
	if not isinstance(data, dict):
		App_logger.warning("data is in HTML")
		data_json = html_to_json.convert(data)
	return data_json
        
class pricingDataManagement:
	def __init__(self, msg):
		self.format = config.format
		self.commonFormat = config.commonFormat
		self.month_name_dict = createMonthNameMap()
		self.msg = msg
		self.monthTimestamp = dict()
		self.PriceData = defaultdict(dict)
		self.wallet = msg["Wallet"]
		self.clientID = msg["ClientID"]
		self.timeStamp_max = msg["TimeStamp-Max"]
		self.timeStamp_min = msg["TimeStamp-Min"]
		self.assert_platform = msg["AssertPlatform"]
		self.token = msg["Token"].lower()
		self.address = msg["Address"]
		self.database_name = msg["database"]
		self.collection_name = msg["collection"]
		self.blob = msg["blob"]
		self.timeStamp_max = strTo_DateTimeObject(msg["TimeStamp-Max"], self.format)
		self.timeStamp_min = strTo_DateTimeObject(msg["TimeStamp-Min"], self.format)
		for yr in range(self.timeStamp_min.year, self.timeStamp_max.year + 1):
			self.monthTimestamp[yr] = createTimestamp(yr, self.timeStamp_max.date(), self.timeStamp_min.date())
		self.price_extractor = priceExtractor(self.assert_platform)
		self.loadPrice()
		self.data = []
		self.priced_txs = []
		self.unpriced_txs = []
		self.blobclient = blobSet.blob_service_client.get_blob_client(container = "cache", blob = self.blob)
		if self.blobclient.exists():
			streamdownloader = self.blobclient.download_blob()
			self.data = json.loads(streamdownloader.readall())
		self.updatePricingData()
		
	def loadPrice(self):
		try:
			App_logger.info(f"Load Price for the Token: {self.token} for date ranges: ({self.timeStamp_min}, {self.timeStamp_max})")
			for year in self.monthTimestamp.keys():
				for monthName in self.monthTimestamp[year].keys():
					file_name = "-".join([self.token, str(year), monthName, "pricing"]) + ".json"
					file_path = "/".join(["coingecko", self.token, str(year), monthName, file_name])
					blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path)
					if not blobClient.exists():
						start, end = self.monthTimestamp[year][monthName]
						data = self.price_extractor.extractDataMonthly(self.token, self.address, start, end)
						self.PriceData[year][monthName] = data
					else:
						streamdownloader = blobClient.download_blob()
						data = json.loads(streamdownloader.readall())
						self.PriceData[year][monthName] = data

		except Exception as err:
			App_logger.info(f"Loading Price for the Token: {self.token} for date ranges: ({self.timeStamp_min}, {self.timeStamp_max}) was unsuccessful")
			App_logger.info("Error:", err)

	def getPrice(self, timestamp):
		dt = strTo_DateTimeObject(timestamp, self.format)
		monthName = self.month_name_dict[dt.month]
		year = dt.year
		day = str(dt.day)
		hour = str(dt.hour)
		data = self.PriceData[year][monthName]
		try:
			if data is None or len(data) == 0:
				App_logger.error(f'Getting empty data: {self.address}, {self.token}, {timestamp}')
				return ""
			if day not in data.keys():
				App_logger.error(f"Specific day data not available: {self.address}, {self.token}, {timestamp}")
				return ""
			dayData = data[day]
			if hour not in dayData.keys():
				App_logger.error(f"Specific hour data not available: {self.address}, {self.token}, {timestamp}")
				return ""
			hourData = dayData[hour]
			return str(hourData[1])

		except Exception as err:
			App_logger.info("Price data unavailable")
			App_logger.error(err)
			return ""
		
	def updatePricingData(self):
		try:
			self.priced_txs = []
			self.unpriced_txs = []
			for tx in self.data:
				timestamp = tx["TimeStamp"]
				price = self.getPrice(timestamp)
				if 'hasNFT' in tx.keys() and len(tx["Price"]) == 1:
					if len(price) > 0:
						price = str(float(price) * float(tx['Price'][0]['Amount']))
					else:
						price = ''
						tx['Log'] = {'NFT Price': tx['Price']}
				tx["Price"] = price
				if len(tx["Price"]) > 0:
					self.priced_txs.append(tx.copy())
				else:
					self.unpriced_txs.append(tx.copy())
			App_logger.info(f"total data length: {len(self.data)}")
			App_logger.info(f"{self.msg['collection']}: Priced Txs -> {len(self.priced_txs)}")
			App_logger.info(f"{self.msg['collection']}: Unpriced Txs -> {len(self.unpriced_txs)}")
		
		except Exception as err:
			App_logger.error(err)

	def ExportDataToDB(self):
		if len(self.priced_txs) > 0:
			dbSet.insertManyDB(dbSet.tadaUtility(self.collection_name), filter=self.priced_txs)
			# dbSet.tadaDB.get_collection(self.collection_name).insert_many(self.priced_txs)
		if len(self.unpriced_txs) > 0:
			dbSet.insertManyDB(dbSet.getUnclassifiedTxs(), filter=self.unpriced_txs)
			updated_status = "incomplete"
			filter = {"clientId" : self.clientID, "wallets.address" : self.wallet}
			proj = {"$set" : {"wallets.$.status" : updated_status}}
			# dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
		self.blobclient.delete_blob()
		
	# This function needs to be called at the very end 
	def UpdateStatus(self):
		try:
			filter = {'clientId': self.clientID}
			return_document = ReturnDocument.AFTER
			projection = {'$inc': {'classification': -1}}
			StatusDoc = dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, return_document, projection)
			
			# When last job, update all 'processing' wallets to complete, cuz if the wallet has unclassified Txs the status is already updated to incomplete in previous steps 
			if StatusDoc['classification'] == 0:
				filter = {"clientId": self.clientID, 'wallets.status': "processing"}
				proj = {"clientId" : 0, "_id": 0}
				wallets = dbSet.findOneDB(dbSet.getWallets(), filter, proj)
				if wallets is not None:
					for wal in wallets["wallets"]:
						filter = {"clientId" : self.clientID, "wallets.address" : wal["address"]}
						proj = {"$set" : {"wallets.$.status" : "complete"}}
						dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
				# Call tax calculation
				calculateTaxLiability(self.clientID)

		except Exception as err:
			App_logger.error(err)


if __name__ == "__main__":
	msg = {"database": "TADADB", 
	"collection": "ClassifiedTxs", 
	"blob": "covalent/41306048-d5fb-4b53-87f0-00655f0a7c85/pricing-clf-0xc47462dd85d9d2441a132fd348dd0c7a1fb92c2c-0x38d74b8a771ee16da1f1cad2a55b8f9937f1f174-MEEMEE.json", 
	"AssertPlatform": "ethereum", 
	"Token": "MEEMEE", 
	"Address": "0x38d74b8a771ee16da1f1cad2a55b8f9937f1f174", 
	"TimeStamp-Max": "2022-10-30T17:54:23Z", 
	"TimeStamp-Min": "2022-10-30T17:54:23Z", 
	"Wallet": "0xc47462dd85d9d2441a132fd348dd0c7a1fb92c2c", 
	"ClientID": "41306048-d5fb-4b53-87f0-00655f0a7c85"}
	# priceManager = pricingDataManagement(msg)
	priceManage = pricingDataManagement(msg)
	print()

