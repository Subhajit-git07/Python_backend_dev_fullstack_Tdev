from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet
from util import *
from loggerUtil import logger
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
from bson import ObjectId

class classificationManagement:
	def retryFailedTransactionTask(self, clientId: UUID):
		clientId = str(clientId)
		filter = {"clientId": clientId}
		walletStatuses = dbSet.findOneDB(dbSet.getStatuses(), filter)["wallets"]
		# Format, chainName:chainID
		chainName_ID_map = {}
		msgList = []
		# Loop through all wallets and update the status to processing for any wallet with failed pages
		for wallet in walletStatuses:
			if wallet["failedPages"]:
				filter = {"wallets.address": wallet["address"]}
				proj = {"wallets" : {"$elemMatch" : {"address" : wallet["address"]}}}
				chain = dbSet.findOneDB(dbSet.getWallets(), filter, proj)["wallets"][0]["chain"]
				if chain not in chainName_ID_map.keys():
						filter = {"name": chain}
						chainName_ID_map[chain] = dbSet.findOneDB(dbSet.getBlockchains(), filter)["chainID"]
				msgList.append({
						"chainID": chainName_ID_map[chain],
						"chainName": chain,
						"clientId": clientId,
						"wallet": wallet["address"],
						"retry" : 1
					})
				filter = {"clientId" : clientId, "wallets.address" : wallet["address"]} 
				proj = {"$set" : {"wallets.$.status" : "processing"}}
				dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
		# Update classification status of client by `number of messages`
		filter = {'clientId': clientId}
		proj = {'$inc': {'classification': len(msgList)}}
		dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)

		if len(msgList) > 0:
			for msg in msgList:
				queueSet.get_queue_client("covalentq").send_message(json.dumps(msg, default=str))
			return StatusResponseDomain(status="Retrying wallets", message=f"Repulling transactions for {len(msgList)} wallets")
		else:
			return StatusResponseDomain(status="No wallets to retry", message="No transactions missing for client's added wallets")

	def commitClassificationTask(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId": clientId}
			proj = {"clientId" : 0, "_id": 0}
			wallets = dbSet.findOneDB(dbSet.getWallets(), filter, proj)["wallets"]
			# Format, chainName:chainID
			chainName_ID_map = {}
			# Messages format, address:chainID
			msg_list = []
			# Create messages for queue for all wallets with status of new
			for wallet in wallets:
				if wallet["status"] == "New":
					if wallet["chain"] not in chainName_ID_map.keys():
						filter = {"name": wallet["chain"]}
						chainName_ID_map[wallet["chain"]] = dbSet.findOneDB(dbSet.getBlockchains(), filter)["chainID"]
					msg_list.append({
						"chainID": chainName_ID_map[wallet["chain"]],
						"chainName": wallet["chain"],
						"clientId": clientId,
						"wallet": wallet["address"]
					})
					# Update status of wallet
					filter = {"clientId" : clientId, "wallets.address" : wallet["address"]}
					proj = {"$set" : {"wallets.$.status" : "processing"}}
					dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
			# Update classification status of client by number of messages
			filter = {'clientId': clientId}
			proj = {'$inc': {'classification': len(msg_list)}}
			dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
			# Send messages to Covalent function app queue for processing
			for msg in msg_list:
				queueSet.get_queue_client("covalentq").send_message(json.dumps(msg, default=str))
			return msg_list
		except Exception as e:
			logger.exception(e)
	
	def deleteUnclassifiedTxsTask(self, clientId: UUID, txId: str):
		clientId = str(clientId)
		filter = {"_id" : ObjectId(txId), "isdelete":False}
		# Get the transaction details
		tx = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
		# Delete the transaction

		proj = {"$set" : {"isdelete" : True}}
		dbSet.updateOneDB(dbSet.getUnclassifiedTxs(),filter,proj)
		# After classifying tx, check if there are any more unclassified for wallet. If not, change status to complete and run tax calc
		filter = {"Wallet" : tx["Wallet"], "isdelete":False}
		stillUnclDocs = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
		if not stillUnclDocs:
			filter = {"wallets.address" : tx["Wallet"]}
			proj = {"$set" : {"wallets.$.status" : "complete"}}
			dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
			calculateTaxLiability(clientId)
		return StatusResponseDomain(status = "Transaction Deleted", message=f'Transaction from hash {tx["TxHash"]} with Id {txId} deleted from UnclassifiedTxs collection')
		# except Exception as e:
		# 	logger.exception(e)
		
	def updateUnclassifiedTxsTask(self, clientId: UUID, item: TransactionRequestDomain):	
		try:
			clientId = str(clientId)
			txOut = UnclassifiedTxPutResponseDomain(Wallet=item.Wallet, TxHash=item.TxHash, From=item.From, To=item.To, Token=item.Token, TransactionDesc=item.TransactionDesc, TxDirection=item.TxDirection, Amount=item.Amount, Price=item.Price, id=item.id, TimeStamp=item.TimeStamp)
			# Check if all fields are filled out, if not, return error
			if item.Wallet == "" or item.From == "" or item.To == "" or item.Token == "" or item.TransactionDesc == "" or item.TxDirection == "" or item.Amount == "" or item.Price == "" or item.TimeStamp == "":
				txOut.error = StatusResponseDomain(status = "incomplete", message="Please make sure data is complete before submitting change")
				return txOut
			# Update all fields
			filter = {"_id" : ObjectId(item.id), "isdelete":False}
			proj = {"$set" : {
				"Wallet" : item.Wallet,
				"TxHash" : item.TxHash,
				"From" : item.From,
				"To" : item.To,
				"Token" : item.Token,
				"TransactionDesc" : item.TransactionDesc,
				"TxDirection" : item.TxDirection,
				"Amount" : item.Amount,
				"Price" : item.Price,
				"TimeStamp" : item.TimeStamp
				}}
			dbSet.updateOneDB(dbSet.getUnclassifiedTxs(), filter, proj)
			#Get updated document
			try:
				filter = {"_id" : ObjectId(item.id), "isdelete":False}
				document = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
				# Check if we have to update TokenMeta 
				update_tokenmeta = False
				# If TokenMeta doesn't exist
				if "TokenMeta" not in document.keys():
					update_tokenmeta = False
				elif document and "symbol" in document['TokenMeta'].keys():
					# If Token is not the same same as symbol in TokenMeta -> it means Token is updated by user and we must update TokenMeta
					if document['TokenMeta']['symbol'] != item.Token:
						update_tokenmeta = True
				else:
					# If TokenMeta exists but is empty 
					update_tokenmeta = True
				if update_tokenmeta:
					# Get list of token from DB
					filter = {"Wallet": item.Wallet}
					tokenDocs = dbSet.findOneDB(dbSet.getTokens(), filter)
					# Find the Token meta if the token exists in Tokens DB for the wallet
					metaDoc = [x for x in tokenDocs['TokenMetaData'] if x['symbol'] == item.Token]
					# Update TokenMeta of the unclassified doc if symbol is found else replace it with empty doc
					document['TokenMeta'] = metaDoc[0].copy() if len(metaDoc) > 0 else {}
				# Insert transaction into Classified colleciton, remove it from Unclassified
				dbSet.insertOneDB(dbSet.getClassifiedTxs(), document)
				filter = {"_id" : ObjectId(item.id), "isdelete":False}
				proj = {"$set" : {"isdelete" : True}}
				dbSet.updateOneDB(dbSet.getUnclassifiedTxs(), filter, proj)
			except TypeError:
				pass
			#After classifying tx, check if there are any more unclassified for wallet. If not, change status to complete and rerun tax calc
			filter = {"Wallet" : item.Wallet, "isdelete":False}
			stillUnclDocs = dbSet.findOneDB(dbSet.getUnclassifiedTxs(), filter)
			if not stillUnclDocs:
				filter = {"wallets.address" : item.Wallet}
				proj = {"$set" : {"wallets.$.status" : "complete"}}
				dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
				calculateTaxLiability(clientId)
			return txOut
		except Exception as e:
			logger.exception(e)
			
	def getTaxSummaryDetails(self, clientId: UUID):
		try:
			clientId = str(clientId)
			# Query the client tax summary from Clients collection
			filter = {"clientId": clientId}
			taxSummary = dbSet.findOneDB(dbSet.getClients(), filter)["taxSummary"]
			# Query the client tax liability to get the mode
			filter = {"clientId": clientId}
			mode = dbSet.findOneDB(dbSet.getClients(), filter)["taxLiability"]["mode"]
			return TaxSummaryResponseDomain(fifoTotalTax=taxSummary["fifo"]["totalTax"], lifoTotalTax=taxSummary["lifo"]["totalTax"], 
			hifoTotalTax=taxSummary["hifo"]["totalTax"], mode=mode)
		except Exception as e:
			logger.exception(e)
				
	def testTaxCalculationTask(self, clientId: UUID):
		try:
			clientId = str(clientId)
			# Delete form data for client
			msg = {"operation" : "delete form data", "clientId" : clientId}
			queueSet.get_queue_client("dbopsqueue").send_message(json.dumps(msg, default=str))
			# Get wallets to calculate holdings first
			filter = {"clientId": clientId}
			wallets = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]
			userWallets = []
			if wallets: 
				userWallets = [wallet["address"] for wallet in wallets]
			else:
				# If no wallets then delete 8949 checkbox saved data
				filter = {"clientId" : clientId, "checkboxData" : {"$exists" : True}}
				dbSet.deleteManyDB(dbSet.getFormData(), filter)
			calculateHoldingsNew(clientId, userWallets)
			# Reset tax calc status
			filter = {"clientId" : clientId}
			proj = {"$set" : {"taxCalculation" : 1}}
			dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
			# Kick off tax calc function
			msg_list = []
			msg_list.append({"clientId" : clientId})
			# msg_list.append({"clientId" : clientId, "mode": "lifo"})
			# msg_list.append({"clientId" : clientId, "mode": "hifo"})
			for msg in msg_list:
				queueSet.get_queue_client("taxcalcqueue").send_message(json.dumps(msg, default=str))
		except Exception as e:
			logger.exception(e)
			
classificationService = classificationManagement()