from util import *
from loggerUtil import logger
import pandas as pd
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
from Domain.clientMgmtService import clientService
import json
from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet

class walletsManagement:
	def getBlockchainsFunc(self):
		try:
			chains = []
			blockchains = list(dbSet.findManyDB(dbSet.getBlockchains(), {}))
			for chain in blockchains:
				if chain["chainID"] != "":
					chains.append(chain["name"])
			# chains = pd.DataFrame(list(dbSet.findManyDB(dbSet.getBlockchains(), {})))["name"].tolist()
			return chains
		except Exception as e:
			logger.exception(e)
		
	def getAllWallets(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId": clientId}
			wallets = list(dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"])
			wallets.sort(key=lambda x: x["chain"])
			return wallets
		except Exception as e:
			logger.exception(e)
		
	def addWalletDetails(self, clientId: UUID, walletInfo: WalletsRequestDomain):
		# try:
		clientId = str(clientId)
		# Create Output array
		walletResArr = list()
		# Create Array of incoming Chain Names
		chainsArr = [wl.chain for wl in walletInfo]
		# Create Array of incoming Addresses
		dataArr = [wl.address.lower() for wl in walletInfo]
		# Get DB Chain Names that match the input array Chain Names
		filter = {"name": {"$in": chainsArr}}
		proj = {"chainID": 1, "name": 1, "_id": 0, "API param.covalent": 1}
		chains = pd.DataFrame(
					data=list(
						dbSet.findManyDB(dbSet.getBlockchains(), filter, proj)
					),
					columns=['chainID','name','API param']
				)
		# Get DB Addresses that match the input array Addresses
		agg = [ 
						{"$unwind": {"path": "$wallets"}},
						{"$match": {"wallets.address": {"$in": dataArr}}},
						{"$group": {"_id": "$wallets.address"}},
					]
		data = pd.DataFrame(
						list(dbSet.aggregateDB(dbSet.getWallets(), agg)),
						columns=['_id']
					)
		# Convert Wallets list input to DataFrame 
		walletsDF = pd.DataFrame([ w.to_dict() for w in walletInfo]).drop_duplicates(subset=['address'])
		# Merge (Left join) DB dataframes and Input list (DataFrame), retrieves addresses that exist and chain name IDs if they exist.  
		walletsDF = pd.merge(
						pd.merge(walletsDF,chains, left_on='chain',right_on='name', how='left'),
						data, 
						left_on='address',right_on='_id', how='left'
					)
		# Renames column for Addressfound
		walletsDF = walletsDF.rename(columns={'_id':'addressfound'})
		# Loop through all input rows and their corresponding DB values found
		for ind in walletsDF.index:
			# Get current chain information
			walletRes = WalletResponseDomain(address=walletsDF['address'][ind].lower(),
							chain=walletsDF['chain'][ind])
			# Cannot add wallet when status is data processing
			curr_classification_status = clientService.getClientOverallStatus(clientId)
			if curr_classification_status.status == "Data Processing":
				walletRes.status = ""
				walletRes.error = curr_classification_status
			# Check if the chain is supported by the Application
			elif pd.isnull(walletsDF['chainID'][ind]): 
				walletRes.status = "Not Supported"
				walletRes.error = StatusResponseDomain(status="Unsupported", message=f'Chain: {walletsDF["chain"][ind]} is not supported by the Application')
			# Check if Covalent is an API Param for Chain
			elif not(pd.isnull(walletsDF['API param'][ind])) and  "covalent" not in walletsDF['API param'][ind].keys():
				walletRes.status = "Not Supported"
				walletRes.error = StatusResponseDomain(status="Unsupported", message=f'Chain: {walletsDF["chain"][ind]} is not supported by the Application')
			# Check if wallet exists in the database
			elif not(pd.isnull(walletsDF['addressfound'][ind])): #TODO
				walletRes.status = "Unauthorized"
				walletRes.error = StatusResponseDomain(status="Unauthorized", message=f'wallet address: {walletsDF["address"][ind]} already exists in the database')
			# If all checks pass, add to DB
			elif  not(pd.isnull(walletsDF['API param'][ind])) and "covalent" in  walletsDF['API param'][ind].keys(): #TODO
				walletRes.status = "New"
				AddWalletToUser(clientId, walletRes)
			# Added catch for unknown Error
			else: 
				walletRes.status = "Unknown Error"
				walletRes.error = StatusResponseDomain(status="Unknown Error", message=f'Unknown error occurred while adding Chain: {walletsDF["chain"][ind]}, wallet address: {walletsDF["address"][ind]} in the database')
			# Add result to output array
			walletResArr.append(walletRes)
		return walletResArr
		# except Exception as e:
		# 	logger.exception(e)
			
	def deleteWalletDetails(self, clientId: UUID, item: WalletRequestDomain):
		try:
			clientId = str(clientId)
			# Increment classification status
			filter = {'clientId': clientId}
			proj = {'$inc': {'classification': 1}}
			dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
			# Find wallet address to delete
			item.address = item.address.lower()
			filter = {"wallets.address": item.address}
			proj = {"wallets" : {"$elemMatch" : {"address" : item.address}}}
			addrData = dbSet.findOneDB(dbSet.getWallets(), filter, proj)
			# If address found in DB, delete it from Wallets collection and Status Collection
			if addrData:
				filter = {"clientId" : clientId}
				proj = {"$pull" : {"wallets" : {"address" : item.address}}}
				dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
				proj = {"$pull" : {"wallets" : {"address" : item.address}}}
				dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
				# Delete all wallet transactions if wallet is not new
				if addrData["wallets"][0]["status"] == "complete" or addrData["wallets"][0]["status"] == "incomplete":
					msg = {"operation": "delete wallet data", "wallet" : item.address, "clientId" : clientId}
					queueSet.get_queue_client("dbopsqueue").send_message(json.dumps(msg, default=str))
				else:
					# Decrement classification status here if wallet is new
					filter = {'clientId': clientId}
					proj = {'$inc': {'classification': -1}}
					dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
				return StatusResponseDomain(status="success", message="Deleted from TADADB")
			else:
				return StatusResponseDomain(status="invalid", message=f"client doesn't have the wallet - {item.address}")
		except Exception as e:
			logger.exception(e)
			return StatusResponseDomain(status="Error occurred", message="exception: {}.format(e)")
		
walletService = walletsManagement()	