import json

from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet

from LoggerUtils import App_logger

def calculateTaxLiability(clientId):
    # Delete form data for client
    try:
        App_logger.info("DBOps - Calculating taxliability")
        msg = {"operation" : "delete form data", "clientId" : clientId}
        queueSet.get_queue_client("dbopsqueue").send_message(json.dumps(msg, default=str))

        # Get wallets to calculate holdings first
        filter = {"clientId": clientId}
        proj = {"clientId" : 0, "_id": 0}
        wallets = dbSet.findOneDB(dbSet.getWallets(), filter, proj)
        userWallets = []
        if wallets: 
            userWallets = [wallet["address"] for wallet in wallets]
        else:
            # If no wallets then delete 8949 checkbox saved data
            filter = {"clientId" : clientId, "checkboxData" : {"$exists" : True}}
            dbSet.deleteManyDB(dbSet.getFormData(), filter)
        calculateHoldingsNew(clientId, userWallets)

        # Reset tax calc status
        filter = {"clientId" : clientId}, {"$set" : {"taxCalculation" : 3}}
        dbSet.updateOneDB(dbSet.getStatuses(), filter)
        
        # Kick off tax calc function
        msg_list = []
        msg_list.append({"clientId" : clientId, "mode": "fifo"})
        msg_list.append({"clientId" : clientId, "mode": "lifo"})
        msg_list.append({"clientId" : clientId, "mode": "hifo"})
        for msg in msg_list:
            queueSet.get_queue_client("taxcalcqueue").send_message(json.dumps(msg, default=str))
    
    except Exception as err:
        App_logger.info("DBOps - Issue in calculating taxliability")
        App_logger.error(err)
    
def calculateHoldingsNew(clientId, wallets):
    holdings = []
    totalValueIn = 0
    totalValueOut = 0

    try:
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
        App_logger.info("DBOps - Issue with calculating holdings")
        App_logger.error(err)