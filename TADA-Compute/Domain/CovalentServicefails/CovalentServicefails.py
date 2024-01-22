from Infrastructure.dbMgmt import dbSet

class CovalentServicefails:

    def __init__(self, msg_param):
        self.user = msg_param["clientId"]
        self.wallet = msg_param["wallet"]

    def Covalentfailoperations(self):
        filter = {'clientId': self.user}
        proj = {'$inc': {'classification': -1}}
        dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, proj)

        filter = {"clientId" : self.user, "wallets.address" : self.wallet}
        proj = {"$set" : {"wallets.$.status" : "Failed"}}
        dbSet.updateOneDB(dbSet.getWallets(), filter, proj)