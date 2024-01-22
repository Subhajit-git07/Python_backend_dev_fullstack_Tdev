from Infrastructure.dbMgmt import dbSet
from Infrastructure.blobMgmt import blobSet

class BCExtFails:

    def __init__(self, msg_param):
        self.container = msg_param["container"]
        self.blob = msg_param["blob"]
        self.user = msg_param["clientID"]
        self.wallet = msg_param["wallet"]
        self.chainName = msg_param["chainName"]

    def BCfailoperations(self):
        blobClient = blobSet.blob_service_client.get_blob_client(container=self.container, blob=self.blob)
        if blobClient.exists():
            blobClient.delete_blob()
        
        filter = {'clientId': self.user}
        proj = {'$inc': {'classification': -1}}
        dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, proj)

        filter = {"clientId" : self.user, "wallets.address" : self.wallet}
        proj = {"$set" : {"wallets.$.status" : "Failed"}}
        dbSet.updateOneDB(dbSet.getWallets(), filter, proj)

        filter = {"Wallet": {"$eq": self.wallet}}
        dbSet.deleteManyDB(dbSet.getClassifiedTxs(), filter)
        
        filter = {"Wallet": {"$eq": self.wallet}}
        dbSet.deleteManyDB(dbSet.getUnclassifiedTxs(), filter)