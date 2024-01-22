from DBOpsService.util import *

from LoggerUtils import App_logger

from Infrastructure.dbMgmt import dbSet

class DBOperater:
    def __init__(self, param: dict):
        self.params = param
    
    def completeOperation(self):
        try:
            operation = self.params["operation"]
            if operation == "delete wallet data":
                wallet = self.params["wallet"]
                clientId = self.params["clientId"]
                
                # Delete transactions and data from Token data
                filter = {"Wallet": {"$eq": wallet}}
                dbSet.deleteManyDB(dbSet.getClassifiedTxs(), filter)
                
                filter = {"Wallet": {"$eq": wallet}}
                dbSet.deleteManyDB(dbSet.getUnclassifiedTxs(), filter)

                filter = {"Wallet": {"$eq": wallet}}
                dbSet.deleteManyDB(dbSet.getTokens(), filter)
                
                # Decrement classification status
                filter = {'clientId': clientId}
                proj = {'$inc': {'classification': -1}}
                dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, proj)

                # Delete forms if user has no wallets left (not from storage just DB record)
                filter = {"clientId": clientId}
                proj = {"clientId" : 0, "_id": 0}
                wallets = dbSet.findOneDB(dbSet.getWallets(), filter, proj)["wallets"]
                
                if not wallets:
                    filter = {"clientId" : clientId}
                    proj = {"$set" : {"8949Form" : []}}
                    dbSet.updateOneDB(dbSet.getPdfFormGeneration(), filter, proj)
                
                # Run Tax Liability
                calculateTaxLiability(clientId)

            if operation == "delete form data":
                clientId = self.params["clientId"]
                filter = {"clientId" : clientId, "rowId" : {"$exists" : True}}
                dbSet.deleteManyDB(dbSet.getFormData(), filter)

            if operation == "delete client":
                clientId = self.params["clientId"]
                # If a client still has wallets, delete all transaction data
                filter = {"clientId": clientId}
                proj = {"clientId" : 0, "_id": 0}
                wallets = dbSet.findOneDB(dbSet.getWallets(), filter, proj)["wallets"]

                if wallets:
                    for wallet in wallets:
                        filter = {"Wallet": {"$eq": wallet["address"]}}
                        dbSet.deleteManyDB(dbSet.getClassifiedTxs(), filter)
                        dbSet.deleteManyDB(dbSet.getUnclassifiedTxs(), filter)
                        
                # Delete form data
                filter = {"clientId" : clientId, "rowId" : {"$exists" : True}}
                dbSet.deleteManyDB(dbSet.getFormData(), filter)

                filter = {"clientId" : clientId, "checkboxData" : {"$exists" : True}}
                dbSet.deleteManyDB(dbSet.getFormData(), filter)
               
                # Delete client from user list
                filter = {"clients": clientId}, {"$pull" : {"clients" : clientId}}
                dbSet.updateManyDB(dbSet.getUsers(), filter)
                
                # Delete client documents elsewhere
                filter = {"clientId": clientId}
                dbSet.deleteOneDB(dbSet.getClients(), filter)
                dbSet.deleteOneDB(dbSet.getWallets(), filter)
                dbSet.deleteOneDB(dbSet.getHoldings(), filter)
                dbSet.deleteOneDB(dbSet.getStatuses(), filter)
                dbSet.deleteOneDB(dbSet.getPdfFormGeneration(), filter)
        
        except Exception as err:
            App_logger.error(err)

if __name__ == "__main__":
    msg_param = {
        "operation" : "delete wallet data",
        "wallet" : "0x5125e63cdb4e171921a1664831fcaaf1fb85bfff"
    }
    operator = DBOperater(msg_param)
    operator.completeOperation()