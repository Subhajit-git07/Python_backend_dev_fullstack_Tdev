import json
from datetime import datetime
from api.models.response import *
from api.models.request import *
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet

def createWalletStatus(clientId, Wallet):
	filter = {'clientId': clientId}
	walletUpdates = {
		'address': Wallet,
		'totalPages': 0,
		'failedPages': [],
		'stats': {
			'nfts': 0,
			'classified': 0,
			'unclassified': 0,
		},
		'queuedJobs': 0,
		'completedJobs': 0
	}
	dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, {'$push': {"wallets" : walletUpdates}})

def createUser(emailId):
    newUser = {}
    newUser["emailId"] = emailId.lower()
    newUser["clients"] = []
    dbSet.insertOneDB(dbSet.getUsers(), newUser)

def AddWalletToUser(clientId: UUID, walletInfo: WalletResponse):
    newWallet = {
            "chain" : walletInfo.chain,
            "address": walletInfo.address,
            "status": walletInfo.status
        }
    filter = {"clientId" : clientId}
    proj = {"$push" : {"wallets" : newWallet}}
    dbSet.updateOneDB(dbSet.getWallets(), filter, proj)

def GetTransactionsByKey(key, keyValue, walletList, skips, size):
	select_columns = {
		"Wallet": 1,
		"TxHash": 1,
		"From": 1,
		"To": 1,
		"Token": 1,
		"TokenList":1,
		"TransactionDesc": 1,
		"TxDirection": 1,
		"Amount": 1,
		"Price": 1,
		"TimeStamp": 1,
		"_id": 1
	}
	filter = {key: keyValue, "Wallet" : {"$in" : walletList}, "isdelete":False}
	proj = select_columns
	if skips != 0:
		skips = skips - 1

	if key == "TxHash":
		allUnclassifiedTxs = dbSet.findManyDB(dbSet.getUnclassifiedTxs(), filter, proj)
		allUnclassifiedList = list(allUnclassifiedTxs)
		for tx in allUnclassifiedList:
			tx["type"] = "Unclassified"
			tx["id"] = str(tx["_id"])
			del tx["_id"]
	elif key == "Token":
		allUnclassifiedList = []
	allClassifiedTxs = dbSet.findManyDB(dbSet.getClassifiedTxs(), filter, proj)        
	allClassifiedTxsList = list(allClassifiedTxs)
	for tx in allClassifiedTxsList:
		tx["type"] = "Classified"
		tx["id"] = str(tx["_id"])
		del tx["_id"]
    
	allTxs = []
	allTxs.extend(allUnclassifiedList)
	allTxs.extend(allClassifiedTxsList)
	totalTxsNum = len(allTxs)
	totalOut = sum(float(tx["Amount"]) for tx in allTxs if tx["TxDirection"] == "OUT" and tx["Amount"])
	totalIn = sum(float(tx["Amount"]) for tx in allTxs if tx["TxDirection"] == "IN" and tx["Amount"])

	return allTxs[skips: skips+size], totalTxsNum, totalIn, totalOut

def createClientHelper(item: ClientRequestDomain, emailId: str):
    # Create client fields
    newClient = {}
    newClient["clientId"] = item.clientId
    newClient["name"] = item.name
    newClient["formName"] = item.formName
    newClient["taxId"] = item.taxId
    newClient["address"] = {
        "addressLn1" : item.addrLn1,
        "addressLn2" : item.addrLn2,
        "city" : item.city,
        "stateProvidence" : item.state,
        "zipCode" : item.zipCode,
        "country" : item.country
    }
    newClient["exchanges"]= []
    newClient["portfolioValues"] = {
        "in" : 0.00,
        "out" : 0.00
    }
    newClient["taxLiability"] = {
        "totalTax" : 0.00,
        "ltcg" : 0.00,
        "stcg" : 0.00,
        "mode" : ""
    }
    newClient["taxSummary"] = {
         "fifo" : {
            "totalTax" : 0,
            "ltcg" : 0,
            "stcg" : 0
         },
         "lifo" : {
            "totalTax" : 0,
            "ltcg" : 0,
            "stcg" : 0
         },
         "hifo" : {
            "totalTax" : 0,
            "ltcg" : 0,
            "stcg" : 0         
         }
    }
    newClient["userPreferences"] = [
        {
            "name" : "Portfolio",
            "size" : 6
        },
        {
            "name" : "EstimatedTaxLiability",
            "size" : 6
        }
    ]
    newClient["locked"] = False
    newClient["creator"] = emailId.lower()
    dbSet.insertOneDB(dbSet.getClients(), newClient)
    # Create document in Wallets collection for client
    walletDoc = {}
    walletDoc["clientId"] = item.clientId
    walletDoc["wallets"] = []
    dbSet.insertOneDB(dbSet.getWallets(), walletDoc)
    # Create document in Holdings collection for client
    holdingsDoc = {}
    holdingsDoc["clientId"] = item.clientId
    holdingsDoc["holdings"] = []
    dbSet.insertOneDB(dbSet.getHoldings(), holdingsDoc)
    # Create document in Statuses collection for client
    statusDoc = {}
    statusDoc["clientId"] = item.clientId
    statusDoc["classification"] = 0
    statusDoc["taxCalculation"] = 0
    statusDoc["pdfGeneration"] = 0
    statusDoc["wallets"] = []
    dbSet.insertOneDB(dbSet.getStatuses(), statusDoc)
    # Create document in PDFFormGeneration collection for client
    pdfFormDoc = {}
    pdfFormDoc["clientId"] = item.clientId
    pdfFormDoc["year"] = "2022"
    pdfFormDoc["8949Form"] = []
    dbSet.insertOneDB(dbSet.getPdfFormGeneration(), pdfFormDoc)

def TxsToStr(transaction):
    transaction['Sub-Transaction Value'] = str(transaction['Sub-Transaction Value'])
    for key, value in transaction["Filtered Contract Info"].items():
        updated_list = []
        for x in transaction["Filtered Contract Info"][key]:
            updated_list.append(str(x))
        transaction["Filtered Contract Info"][key] = updated_list
    return transaction.copy()

def calculateTaxLiability(clientId: UUID):
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
    for msg in msg_list:
        queueSet.get_queue_client("taxcalcqueue").send_message(json.dumps(msg, default=str))
    
def calculateHoldingsNew(clientId, wallets):
    holdings = []
    totalValueIn = 0
    totalValueOut = 0

    if wallets:
        filter = [
            {
                "$match": {"Wallet": {"$in" : wallets}, "TxDirection" : "IN", "isdelete":False}
            },
            {
                "$group": {"_id" : "$Token", "totalQuantity": {"$sum": {"$toDouble" : "$Amount"}}, "totalValue": {"$sum": {"$multiply" : [{"$toDouble" : "$Amount"}, {"$toDouble" : "$Price"}]}}}
            }
        ]
        inResults = dbSet.aggregateDB(dbSet.getClassifiedTxs(), filter)

        filter = [
            {
                "$match": {"Wallet": {"$in" : wallets}, "TxDirection" : "OUT", "isdelete":False}
            },
            {
                "$group": {"_id" : "$Token", "totalQuantity": {"$sum": {"$toDouble" : "$Amount"}}, "totalValue": {"$sum": {"$multiply" : [{"$toDouble" : "$Amount"}, {"$toDouble" : "$Price"}]}}}
            }
        ]
        outResults = dbSet.aggregateDB(dbSet.getClassifiedTxs(), filter)

        if inResults:
            final = list(inResults)
            for asset in final:
                holding = {
                    "name" : asset["_id"],
                    "direction" : "in",
                    "amount" : asset["totalQuantity"],
                    "totalValue" : asset["totalValue"],
                    "iconName" : ""
                }
                totalValueIn = totalValueIn + asset["totalValue"]
                holdings.append(holding)
        
        if outResults:
            final = list(outResults)
            for asset in final:
                holding = {
                    "name" : asset["_id"],
                    "direction" : "out",
                    "amount" : asset["totalQuantity"],
                    "totalValue" : asset["totalValue"],
                    "iconName" : ""
                }
                totalValueOut = totalValueOut + asset["totalValue"]
                holdings.append(holding)

    filter = {"clientId" : clientId}
    proj = {"$set" : {"portfolioValues.in" : totalValueIn, "portfolioValues.out" : totalValueOut}}
    dbSet.updateOneDB(dbSet.getClients(), filter, proj)
    proj = {"$set" : {"holdings" : holdings}}
    dbSet.updateOneDB(dbSet.getHoldings(), filter, proj)

def defaultconverter(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

