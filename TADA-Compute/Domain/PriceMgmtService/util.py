import calendar
from datetime import timedelta, date
import pandas as pd
import datetime
import collections
import json
import requests
import os

from LoggerUtils import App_logger

from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet
from Infrastructure.blobMgmt import blobSet

def createMonthNameMap():
	calendar_month = calendar.month_name[1:]
	monthNameMap = dict()
	for i in range(1, 13):
		monthNameMap[i] = calendar.month_abbr[i].upper()
	return monthNameMap

def createTimestamp(year: int, max_date, min_date):
	'''Get start date start time and end date end time for each month of a year in below format'''

	# sample = {"jan":("2022-01-01T00:00:00Z", "2022-01-31T23:59:59Z"),
	#           "feb":("2022-01-01T00:00:00Z", "2022-01-28T23:59:59Z")}

	'''Determine start datetime and end datetime for all months in provided year'''

	month_dict = {}
	calendar_month = calendar.month_name[1:]
	start_date = date(year, 1, 1)
	end_date = date(year, 12, 31)
	# if min_date != None:
	# 	start_date = max(start_date, min_date)
	# if max_date != None:
	# 	end_date = min(end_date, max_date)
	sdtrange = pd.date_range(start=start_date, end=end_date, freq='d')
	edtrange = pd.date_range(start=start_date, end=end_date, freq=pd.DateOffset(minutes=60*24-0.000001))

	smonths = pd.Series(sdtrange.month)
	emonths = pd.Series(edtrange.month)

	starts =  smonths.ne(smonths.shift(1))
	ends = emonths.ne(emonths.shift(-1))

	df = pd.DataFrame({'Start_date': sdtrange[starts].strftime('%Y-%m-%dT%H:%M:%SZ'),
					   'End_date': edtrange[ends].strftime('%Y-%m-%dT%H:%M:%SZ')})

	end_date_tmp = edtrange[-1] + timedelta(days=1)
	df["End_date"].iloc[-1] = end_date_tmp.strftime('%Y-%m-%dT%H:%M:%SZ')
	for index, rows in enumerate(list(df.itertuples(index=False, name=None))):
		month_num = datetime.datetime.strptime(rows[0], '%Y-%m-%dT%H:%M:%SZ').month
		month_dict[calendar_month[month_num-1][:3].upper()] = rows
	return month_dict
	
def getTestData():
	# generator = list(config.blob_service_client.list_containers(include_metadata=False))
	# print(generator)
	file_name = "clf-0x5125e63cdb4e171921a1664831fcaaf1fb85bfff-1-1000-0.json"
	file_path = "/".join(["coingecko", "test", file_name])
	blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path)
	if blobClient.exists():
		streamdownloader = blobClient.download_blob()
		Testdata = json.loads(streamdownloader.readall())
		return Testdata
	
def getTokens(Testdata):
	tokens_set = set()
	for tokens in Testdata["Transactions"]:
		tokens_set.add(tokens["Token"])
	return list(tokens_set)
	
def symbolToBlockchain(url):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, timeout=30, verify = False)
        coins = json.loads(response.text)
        dict1 = collections.defaultdict(list)
        for coin in coins:
            dict1[coin["symbol"].lower()].append((coin["id"], coin["name"]))
        
        file_path = os.path.join("coingecko", "coins.json")
        blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path)
        blobClient.upload_blob(json.dumps(dict1, ensure_ascii=False, indent=4), overwrite = True)
        return dict1
    
    except Exception as err:
        App_logger.info("Pricing - Error while converting Symbol to Blockchain")
        App_logger.error(err)
        return {}
	
	
def tokenLists():
	file_name = "coins.json"
	file_path = "/".join(["coingecko", file_name])
	blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path)
	streamdownloader = blobClient.download_blob()
	data = json.loads(streamdownloader.readall())
	return data


def calculateTaxLiability(clientId):
    try:
        # Delete form data for client
        msg = {"operation" : "delete form data", "clientId" : clientId}
        queueSet.get_queue_client("dbopsqueue").send_message(json.dumps(msg, default=str))
        # Get wallets to calculate holdings first
        filter = {"clientId": clientId}
        proj = {"clientId" : 0, "_id": 0}
        wallets = dbSet.findOneDB(dbSet.getWallets(), filter, proj)["wallets"]
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
        proj = {"$set" : {"taxCalculation" : 3}}
        dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
        # Kick off tax calc function
        msg_list = []
        msg_list.append({"clientId" : clientId, "mode": "fifo"})
        msg_list.append({"clientId" : clientId, "mode": "lifo"})
        msg_list.append({"clientId" : clientId, "mode": "hifo"})
        for msg in msg_list:
            queueSet.get_queue_client("taxcalcqueue").send_message(json.dumps(msg, default=str))
    
    except Exception as err:
        App_logger.info("Pricing - Issue calculating Taxliability")
        App_logger.error(err)

def calculateHoldingsNew(clientId, wallets):
    try:
        holdings = []
        totalValueIn = 0
        totalValueOut = 0

        if wallets:
            filter = [
                {
                    "$match": {"Wallet": {"$in" : wallets}, "TxDirection" : "IN"}
                },
                {
                    "$group": {"_id" : "$Token", "totalQuantity": {"$sum": {"$toDouble" : "$Amount"}}, "totalValue": {"$sum": {"$multiply" : [{"$toDouble" : "$Amount"}, {"$toDouble" : "$Price"}]}}}
                }
            ]
            inResults = dbSet.aggregateDB(dbSet.getClassifiedTxs(), filter)

            filter = [
                {
                    "$match": {"Wallet": {"$in" : wallets}, "TxDirection" : "OUT"}
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
        
        filter = {"clientId" : clientId}
        proj = {"$set" : {"holdings" : holdings}}
        dbSet.updateOneDB(dbSet.getHoldings(), filter, proj)
	
    except Exception as err:
        App_logger.info("Pricing - Issue with calculaing Holdings")
        App_logger.error(err)
	
	
'''
tokenList = ['BFF', 'AIE', 'GOAT', 'ZOOT', '8%', 'SHEEBA', 'ECAW', 'xRES.org', 'GhostBlade', 'BAPE', 'ExpoInu', 'MAGIC', 'SHIB', '(Δ)', 'MKONG', 'USDC', 'SHEEB', 'HOGS', 'ETH', 'KWONDOM', 'NT', 'NFT', 'LOCKER', 'ARCADE', 'ShibaTwo', 'SANI', 'Key7.net', 'MGC', 'SAITAMA', 'CLIFF', 'KYC', 'WETH', 'KumKwon', 'LEASH', 'APOLLO', 'AeonCommunity', 'MONKE', 'CVC', 'KAREN', 'KORI', 'CDIEM']
'''