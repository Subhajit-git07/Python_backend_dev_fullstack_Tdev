import json

from Domain.BCExtractorService.DataExtractor.FeatureGen import ClassificationFeatureGenerator
from Domain.BCExtractorService.Classifier.TransactionClassifier import TxClassifier
from Domain.BCExtractorService.configBCExtractor import model_settting

from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet
from Infrastructure.blobMgmt import blobSet

class WalletTransactionExtractor:
    def __init__(self, param: dict):
        # Param: chainName, clientID, container, blob
        self.param = param
        # Get Connection strings for CosmosDB & Storage Account
        self.chainName = param["chainName"]
        self.clientID = param["clientID"]
        self.SrcBlob = param["blob"]
        self.SrcContainer = param["container"]
        self.queue_client = queueSet.get_queue_client(queueName="coingeckopricing")
        # Get data from Blob
        FeatureExtractor = ClassificationFeatureGenerator()
        blobJson = FeatureExtractor.load_data_from_blob(param["container"], param["blob"])
        self.chainID = blobJson["data"]["chain_id"]
        self.wallet = blobJson["data"]["address"]
        # Get Extract Features from Covalent data
        TxsForLogicModel, TxsForMLModel, TokenList = FeatureExtractor.ExtractTransactions(blobJson["data"])
        # Classification
        Classifier = TxClassifier(chainID=str(self.chainID), dataList=TxsForLogicModel, dataDict=TxsForMLModel, 
                                    TokenList=TokenList, TokenMetaData=blobJson["data"]["TokenMetaData"])
        self.TokenTxs, self.UnclassifiedTxs = Classifier.StartClassification(group_by_token=True)
        self.dataset = TxsForMLModel
    
    def ExportToDB(self):
        # Update status of the wallet
        if len(self.UnclassifiedTxs) > 0:
            dbSet.insertManyDB(dbSet.getUnclassifiedTxs(), filter = self.UnclassifiedTxs)
            updated_status = "incomplete"
            filter = {"clientId" : self.clientID, "wallets.address" : self.wallet}
            proj = {"$set" : {"wallets.$.status" : updated_status}}
            dbSet.updateOneDB(dbSet.getWallets(), filter, proj)
        
    def BlobOps(self):
        # Dataset Storage path
        datasetName = self.SrcBlob.split("/")[-1]
        file_path_dataset = f"rawdata/{self.chainID}/{self.wallet}/input/{datasetName}"
        # Adding dataset to the blob
        blobClient_dataset = blobSet.blob_service_client.get_blob_client(container = "datasets", blob=file_path_dataset)
        blobClient_dataset.upload_blob(json.dumps(self.dataset, ensure_ascii=False, indent=4), overwrite=True)
        # Delete the source blob from which data is extracted
        blobClient_source = blobSet.blob_service_client.get_blob_client(container = self.SrcContainer, blob = self.SrcBlob)
        blobClient_source.delete_blob()

    def InitiatePricingModule(self):
        # Extract information from self.param for export
        suffix = "".join(self.SrcBlob.split("/")[-1].split("-")[-3:])
        user = self.param["clientID"]
        msg_template = {
            "database": "TADADB",
            "collection": "",
            "blob": "",
            "AssertPlatform": model_settting.chainParam[self.chainID]["AssertPlatform"],
            "Token": "",
            "Address": "",
            "TimeStamp-Max": "",
            "TimeStamp-Min": "",
            "Wallet": self.wallet,
            "ClientID": self.clientID
        }
        msg_list = []
        # For classified Txs Tokens
        clf_TokenTxs = self.TokenTxs["classified"]["Transactions"]
        clf_TokenRanges = self.TokenTxs["classified"]["TokenDateRanges"]
        for addr in clf_TokenRanges.keys():
            token = clf_TokenTxs[addr][0]['Token']
            file_name = "-".join(["pricing", "clf", self.wallet, addr, token, suffix])
            blob_name = "/".join(["covalent", user, file_name])
            data = clf_TokenTxs[addr]
            msg = msg_template.copy()
            msg["collection"] = "ClassifiedTxs"
            msg["blob"] = blob_name
            msg["Token"] = token
            msg["Address"] = addr
            msg["TimeStamp-Max"] = clf_TokenRanges[addr]["TimeStamp-Max"]
            msg["TimeStamp-Min"] = clf_TokenRanges[addr]["TimeStamp-Min"]
            blobClient = blobSet.blob_service_client.get_blob_client(container = "cache", blob=blob_name)
            blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4), overwrite=True)
            msg_list.append(msg)
        # For unclassified Txs Tokens
        unclf_TokenTxs = self.TokenTxs["unclassified"]["Transactions"]
        unclf_TokenRanges = self.TokenTxs["unclassified"]["TokenDateRanges"]
        for addr in unclf_TokenRanges.keys():
            token = unclf_TokenTxs[addr][0]['Token']
            file_name = "-".join(["pricing", "unclf", self.wallet, addr, token, suffix])
            blob_name = "/".join(["covalent", user, file_name])
            data = unclf_TokenTxs[addr]
            msg = msg_template.copy()
            msg["collection"] = "UnclassifiedTxs"
            msg["blob"] = blob_name
            msg["Token"] = token
            msg["Address"] = addr
            msg["TimeStamp-Max"] = unclf_TokenRanges[addr]["TimeStamp-Max"]
            msg["TimeStamp-Min"] = unclf_TokenRanges[addr]["TimeStamp-Min"]
            blobClient = blobSet.blob_service_client.get_blob_client(container = "cache", blob=blob_name)
            blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4), overwrite=True)
            msg_list.append(msg)
        return msg_list

    def SendMessage(self, msg_list: list):
        for msg in msg_list:
            self.queue_client.send_message(json.dumps(msg, default=str))

    def UpdateStatus(self, taskCount):
        filter = {'clientId': self.clientID}
        proj = {'$inc': {'classification': -1 + taskCount}}
        dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, proj)

    def StartExtraction(self):
        # Export Unclassified Data to DB, & save dataset for ML model
        self.ExportToDB()
        # Initiate the CoingGecko pricing module
        msg_list = self.InitiatePricingModule()
        # Send message to Coingecko queue
        self.SendMessage(msg_list)
        # Update the status of 
        self.UpdateStatus(len(msg_list))
        # Complete blob ops
        self.BlobOps()

if __name__ == "__main__":
    param = {"container": "cache", "blob": "covalent/test/0xd65bb53e079e61d1888deec7952ba82bf6bc38cd-1-1000-0.json",
            "clientID": "test", "chainName": "Ethereum"}
    extract = WalletTransactionExtractor(param)
    extract.InitiatePricingModule()
    print(len(extract.UnclassifiedTxs), len(extract.ClassifiedTxs))
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint()