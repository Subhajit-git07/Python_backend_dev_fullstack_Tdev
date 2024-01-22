from bson import ObjectId
from util import *
from loggerUtil import logger
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
from Domain.walletsMgmtService import walletService
from Infrastructure.dbMgmt import dbSet
from Infrastructure.blobMgmt import blobSet
import pandas as pd
from collections import defaultdict
import time

class transactionsManagement:
	def manualuploadFunc(self, clientId: UUID, transactions: ManualUploadsRequestDomain):
		clientId = str(clientId)
		# Initialize variables
		uniqueWalletList = []
		duplicatewallets = []
		groupedTransactions = defaultdict(list)
		countoftxnsadded = 0

		# Get unique list of wallets from transactions
		wallets = list(set([transaction.Wallet.lower() for transaction in transactions]))

		blockchains = list(dbSet.findManyDB(dbSet.getBlockchains(), {}))
		
		# Group each transaction by asset and wallet for price processing
		# Send each wallet to addWallets function to be added to DB
		for transaction in transactions:
			transaction = transaction.to_dict()
			assetPlatform = [x for x in blockchains if x["name"] == transaction["Blockchain"]]
			# if len(assetPlatform) == 0:
			# 	x = 1
			transaction["AssetPlatform"] = assetPlatform[0]["assetPlatform"]
			groupedTransactions[transaction["Wallet"] + transaction["AssetPlatform"] + transaction["Asset"]].append(transaction)
			if transaction["Wallet"] in wallets:
				uniqueWallet = WalletRequestDomain(address=transaction["Wallet"].lower(),chain=transaction["Blockchain"])
				uniqueWalletList.append(uniqueWallet)
				wallets.remove(transaction["Wallet"])
		walletsToAdd = WalletsRequestDomain(__root__ = uniqueWalletList)
		walletsout = walletService.addWalletDetails(clientId=clientId,walletInfo=walletsToAdd)
		# If wallet was not added, send to duplicates list. If added, update status to processing
		# Update client status so client status changes immediately 
		filterforclient = {'clientId': clientId}
		proj = {'$inc': {'classification': 1}}
		dbSet.updateOneDB(dbSet.getStatuses(), filterforclient, proj)
		if walletsout:
			for wallet in walletsout:
				if wallet.status != 'New':
					duplicatewallets.append(wallet.address)
				else:
					filter = {"clientId" : clientId, "wallets.address" : wallet.address}
					proj = {"$set" : {"wallets.$.status" : "processing"}}
					dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
					createWalletStatus(clientId, wallet.address)
		# Message template for CoinGeko

		msg_template = {
			"database": "TADADB",
			"collection": "ClassifiedTxs",
			"blob": "",
			"AssetPlatform": "",
			"Token": "",
			"Address": "",
			"TimeStamp-Max": "",
			"TimeStamp-Min": "",
			"Wallet": "",
			"ClientID": clientId
		}
		msg_list = []
		# Loop through each group
		for group in groupedTransactions:
			wallet = groupedTransactions[group][0]["Wallet"]
			if wallet.lower() not in duplicatewallets:
				# Increment queued jobs by 1
				filter = {"wallets.address" : wallet.lower()}
				proj = {"$inc" : {"wallets.$.queuedJobs" : 1}}
				dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
				# Create a dataframe for data in group to get the Max and Min time
				data = pd.DataFrame([tx for tx in groupedTransactions[group]])
				MaxTime = data['TimeStamp'].max().strftime("%Y-%m-%dT%H:%M:%SZ")
				MinTime = data['TimeStamp'].min().strftime("%Y-%m-%dT%H:%M:%SZ")
				transactionsToUpload = []
				address = groupedTransactions[group][0]["Asset"]
				token = groupedTransactions[group][0]["Token"]
				wallet = groupedTransactions[group][0]["Wallet"]
				assetPlatform = groupedTransactions[group][0]["AssetPlatform"]
				for transaction in groupedTransactions[group]:
					# tx = transaction.to_dict()
					transaction["Source"] = "manual"
					transaction["TimeStamp"] = transaction["TimeStamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
					transactionsToUpload.append(transaction)
				blobName = "/".join(["ManualUploadTxns", clientId, group])
				blobSet.uploadToBlob(transactionsToUpload, blobName)

				msg = msg_template.copy()
				msg["Address"] = address
				msg["Token"] = token
				msg["Wallet"] = wallet.lower() 
				msg["TimeStamp-Min"] = str(MinTime)
				msg["TimeStamp-Max"] = str(MaxTime)
				msg["blob"] = blobName
				msg["AssetPlatform"] = assetPlatform
				msg_list.append(msg)
				countoftxnsadded += len(groupedTransactions[group])
		# Update client status
		filterforclient = {'clientId': clientId}
		proj = {'$inc': {'classification': len(msg_list) - 1}}
		dbSet.updateOneDB(dbSet.getStatuses(), filterforclient, proj)
		# Send messages
		for msg in msg_list:
			queueSet.get_queue_client("coingeckopricing").send_message(json.dumps(msg, default=str))
		result = {
			'TxnsInserted': countoftxnsadded,
    		'TxnsRejected': duplicatewallets
				}
		return result

	def deletetransactionManualFunc(self, clientId: UUID, txId: str):
		# Delete the transaction
		clientId = str(clientId)
		tx = {}
		filter = {"_id" : ObjectId(txId), "isdelete":False}
		txOutClass = dbSet.findOneDB(dbSet.getClassifiedTxs(), filter)
		txOutUnclass = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
		if txOutClass:
			tx = txOutClass
			proj = {"$set" : {"isdelete" : True}}
			dbSet.updateOneDB(dbSet.getClassifiedTxs(),filter,proj)
		else:
			tx = txOutUnclass
			proj = {"$set" : {"isdelete" : True}}
			dbSet.updateOneDB(dbSet.getUnclassifiedTxs(),filter,proj)
		
		filter = {"Wallet" : tx["Wallet"], "isdelete":False}
		remainingClass = dbSet.findOneDB(dbSet.getClassifiedTxs(), filter)
		remainingUnclass = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
		if not remainingClass and not remainingUnclass:
			deletion = WalletRequestDomain(address=tx["Wallet"].lower(), chain = None)
			walletResponse = walletService.deleteWalletDetails(clientId=clientId,item=deletion)
		else:
			calculateTaxLiability(clientId)
		return StatusResponseDomain(status="Transaction Deleted", message=f"Transaction with ID {txId} deleted")


	def deletebulktransactionManualFunc(self, clientId: UUID, wallets: list, txId: list):
			# Delete Bulk transactions in Manual classificaions
			try:
				unique_wallets = list(set(wallets))
				clientId = str(clientId)
				tx = {}
				for txns in txId:
					filter = {"_id" : ObjectId(txns), "isdelete":False}
					txOutClass = dbSet.findOneDB(dbSet.getClassifiedTxs(), filter)
					txOutUnclass = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
					if txOutClass:
						tx = txOutClass
						proj = {"$set" : {"isdelete" : True}}
						dbSet.updateOneDB(dbSet.getClassifiedTxs(),filter,proj)
					else:
						tx = txOutUnclass
						proj = {"$set" : {"isdelete" : True}}
						dbSet.updateOneDB(dbSet.getUnclassifiedTxs(),filter,proj)
																					
				for wallet in unique_wallets:
					filter = {"Wallet" : wallet, "isdelete": False}
					remainingClass = dbSet.findOneDB(dbSet.getClassifiedTxs(), filter)
					remainingUnclass = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
					if not remainingClass and not remainingUnclass:
						deletion = WalletRequestDomain(address=wallet.lower(), chain = None)
						walletResponse = walletService.deleteWalletDetails(clientId=clientId,item=deletion)
					else:
						calculateTaxLiability(clientId)
				return StatusResponseDomain(status="Transaction Deleted", message=f"Transaction with ID {txId} deleted")
			
			except Exception as e:
				logger.exception(e)

	
	def getTransactionManualFunc(self, clientId: UUID):
		clientId = str(clientId)
		filter = {"clientId": clientId}
		wallets = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]
		userWallets = []
		for wallet in wallets:
			userWallets.append(wallet["address"])           

		filter = {"Wallet" : {"$in" : userWallets}, "Source": "manual", "isdelete": False}
		classifiedTxns = list(dbSet.findManyDB(dbSet.getClassifiedTxs(), filter))
		for tx in classifiedTxns:
			tx["type"] = "Classified"
			tx["id"] = str(tx["_id"])
			del tx["_id"]
		unclassifiedTxns = list(dbSet.findManyDB(dbSet.getUnclassifiedTxs(), filter))
		for tx in unclassifiedTxns:
			tx["type"] = "Unclassified"
			tx["id"] = str(tx["_id"])
			del tx["_id"]
		finaltxns = classifiedTxns+unclassifiedTxns
		return finaltxns
				 
	def getTransactionReferenceHashDetails(self, clientId: UUID, start_index: int, size: int, transactionCount: int):
		try:
			clientId = str(clientId)
			filter = {"clientId": clientId}
			wallets = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]
			userWallets = []
			for wallet in wallets:
				userWallets.append(wallet["address"])           
			filter = "TxHash"
			proj = {"Wallet" : {"$in" : userWallets}, "isdelete": False}
			hashes = dbSet.getDistinctDB(dbSet.getUnclassifiedTxs(), filter, proj)
			total_hash_count = len(hashes)
			index = start_index - 1
			end_index = index + size
			hash_data = []
			if total_hash_count < end_index:
				end_index = total_hash_count
			while index < end_index:
				txData, total_count, total_in, total_out = GetTransactionsByKey("TxHash", hashes[index], userWallets, 0, transactionCount)
				hashObj = {
					"TxHash" : hashes[index],
					"transactionData" : txData,
					"total_count" : total_count
				}
				hash_data.append(hashObj)
				index = index + 1
			return_obj = {
				"data" : hash_data,
				"start_index" : start_index,
				"size" : size,
				"total_count" : total_hash_count
			}
			return return_obj
		except Exception as e:
			logger.exception(e)
		
	def getTransactionByHashDetails(self, clientId: UUID, TxHash: str, start_index: int, size: int):
		try:
			clientId = str(clientId)
			filter = {"clientId": clientId}
			wallets = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]
			userWallets = []
			for wallet in wallets:
				userWallets.append(wallet["address"])

			txData, total_count, total_in, total_out = GetTransactionsByKey("TxHash", TxHash, userWallets, start_index, size)

			return_obj = {
				"transactionData" : txData,
				"start_index" : start_index,
				"size" : size,
				"total_count" : total_count
			}
			return return_obj
		except Exception as e:
			logger.exception(e)
			
	def getTransactionReferenceAssetDetails(self, clientId: UUID, start_index: int, size: int, transactionCount: int):
		try:
			# ss= time.time()
			clientId = str(clientId)
			filterDB = {"clientId": clientId}
			wallets = dbSet.findOneDB(dbSet.getWallets(), filterDB)["wallets"]
			userWallets = []
			for wallet in wallets:
				userWallets.append(wallet["address"])           
			# filter = "Token"
			filterDB = {"Wallet" : {"$in" : userWallets}, "isdelete": False}
			time.sleep(1)

			# tokens = dbSet.getDistinctDB(dbSet.getClassifiedTxs(), filter, proj)# did not work 429

			# testcur = dbSet.aggregateDB(dbSet.getClassifiedTxs(),[{"$group":{"_id":'Token'}}, {"$skip":start_index-1}, {"$limit":size}]) # did not work 429
			# testcur = list(testcur)

			# walletCur = dbSet.findManyDB(dbSet.getClassifiedTxs(),filterDB) # client TXs
			# TokenCursor = dbSet.getDistinctDBCursor(walletCur, "Token") # client Tokens Hits RU limit > 700K TX below that is fine.
			TokenCursor = dbSet.findManyDB(dbSet.getClassifiedTxs(),#[
				# {"$match":
					filterDB
				# }
				,
				# {
				# 	"$project": 
					{
						"Token": 1
						,"TxDirection": 1
					}
				# }
			#]
			)
			# cost = dbSet.getCostofCall(dbSet.getClassifiedTxs())
			# print(cost)

			tokens = list(TokenCursor)
			if len(tokens) ==0:
				return {
					"data" : [],
					"start_index" : start_index,
					"size" : size,
					"total_count" : 0
				}
			# cost = dbSet.getCostofCall(dbSet.getClassifiedTxs())
			# print(cost)

			tokensDF = pd.DataFrame(tokens)
			tokensDF = tokensDF.groupby(['Token','TxDirection'], as_index=False).count().rename({'_id':'CountOfTokenTXByDirection'},axis='columns')
			# tokensSumDict = tokensDF.to_dict('r')
			# print(tokensDF)
			# cost = dbSet.getCostofCall(dbSet.getClassifiedTxs())
			# print(cost)
			tokens = list(set([ t['Token'] for t in tokens]))
			total_token_count = len(tokens)
			# tokens = tokens[start_index-1:start_index-1+size]
			# allTXData = list(dbSet.findManyDB(dbSet.getClassifiedTxs(),filterDB))# "0x6081258689a75d253d87ce902a8de3887239fe80" takes very long
			# tokens = set([t['Token'] for t in allTXData])
			# tx["type"] = "Classified" TODO
			# tx["id"] = str(tx["_id"])
			# allTXData =  # All client TXs
			# TXCursor = walletCur.limit(transactionCount*len(tokens))
			# tokens = list(tokens)
			# Try later
			# filterDB = {"Wallet" : {"$in" : userWallets}, "Token": {"$in": tokens}}
			# dbSet.findManyDB(dbSet.getClassifiedTxs(),filterDB)
			
			index = start_index - 1
			end_index = index + size
			if total_token_count < end_index:
				end_index = total_token_count
			token_data = []
			while index < end_index:
				# txData = list(filter(lambda t: t['Token'] == tokens[index] ,allTXData))
				filterDB = {"Wallet" : {"$in" : userWallets}, "Token": tokens[index], "isdelete": False}
				TXCursor = dbSet.findManyDB(dbSet.getClassifiedTxs(),filterDB).limit(transactionCount)
				txData = list(TXCursor)
				# cost = dbSet.getCostofCall(dbSet.getClassifiedTxs())
				# print(cost)
				txData = [dict(item, type="Classified") for item in txData]
				for t in txData:
					t['id'] = str(t["_id"])
					if 'TokenList' in t.keys():
						del t["TokenList"]
					del t["_id"]
				total_count = sum(tokensDF[tokensDF.Token == tokens[index]]['CountOfTokenTXByDirection'])
				total_out = sum(tokensDF[(tokensDF.Token == tokens[index]) & (tokensDF.TxDirection == 'OUT')]['CountOfTokenTXByDirection'])
				total_in = sum(tokensDF[(tokensDF.Token == tokens[index]) & (tokensDF.TxDirection == 'IN')]['CountOfTokenTXByDirection'])
				# GetTransactionsByKey("Token", tokens[index], userWallets, 0, transactionCount)
				net_amount = total_in - total_out
				assetObj = {
					"Asset" : tokens[index],
					"total_in" : total_in,
					"total_out" : total_out,
					"net_amount" : net_amount,
					"transactionData" : txData,
					"total_count" : total_count
				}
				token_data.append(assetObj)
				index = index + 1
			return_obj = {
				"data" : token_data,
				"start_index" : start_index,
				"size" : size,
				"total_count" : total_token_count
			}
			# print((time.time()-ss))
			return return_obj
		except Exception as e:
			logger.exception(e)
		
		
	def getTransactionByAssetDetails(self, clientId: UUID, Asset: str, start_index: int, size: int):
		try:
			clientId = str(clientId)
			filter = {"clientId": clientId}
			walletsList = dbSet.findOneDB(dbSet.getWallets(), filter)
			if walletsList is None:
				return {
					"transactionData" : [],
					"start_index" : start_index,
					"size" : size,
					"total_count" : 0
				}
			wallets = walletsList["wallets"]
			userWallets = []
			for wallet in wallets:
				userWallets.append(wallet["address"])

			txData, total_count, total_in, total_out = GetTransactionsByKey("Token", Asset, userWallets, start_index, size)
			for t in txData:
				if 'TokenList' in t.keys():
					del t["TokenList"]
		
			return_obj = {
				"transactionData" : txData,
				"start_index" : start_index,
				"size" : size,
				"total_count" : total_count
			}
			return return_obj
		except Exception as e:
			logger.exception(e)
				
transactionService = transactionsManagement()