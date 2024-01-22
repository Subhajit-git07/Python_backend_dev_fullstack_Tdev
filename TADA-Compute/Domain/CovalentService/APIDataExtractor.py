import requests
import json
import time
import numpy as np

from Domain.CovalentService.covalentConfig import config

from Config import EnvSettings

from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet
from Infrastructure.blobMgmt import blobSet
from Infrastructure.ThirdPartyMgmt import ThirdPartySet

from LoggerUtils import App_logger

class CovalentTransactionExtractor:
    def __init__(self, chainID:str , chainName:str, clientID: str, pageSize:int = None):
        # Set class variables which will be reused frequently later
        self.key = ThirdPartySet.CovalentKey
        self.chainID = chainID
        self.chainName = chainName
        self.clientID = clientID
        # return required information to configure covalentq api parameters 
        # Here we only use page size only
        if pageSize:
            self.pageSize = pageSize
        else:
            self.pageSize = config.get_api_page_size(chainID)
        # Establish connection to blob service client 
        self.queue_client = queueSet.get_queue_client(queueName="bcextractor")
        self.fail_client = queueSet.get_queue_client(queueName="covalentq-poison")
        self.TokenMeta = {
            "Wallet": "",
            "TokenMetaData": []
        }
        self.TokenMetaInfo = ''
        self.failedPage = ''
        self.walletPassed = True
        self.terminate = False

    # HTTPS Request function to get data from Covalentq API 
    def GetTransactionsAPI(self, walletID, page):
        url = EnvSettings.transactionUrl.format(
            self.chainID, walletID, page, self.pageSize, self.key)
        headers = {'Content-Type': 'application/json'}
        try:
            App_logger.info(f'Extracting page {page}')
            response = requests.get(url, headers=headers, timeout=30, verify = False)
            ContentSize = len(response.content)/(1024 * 1024)
            data = json.loads(response.text) 
            if ContentSize > config.maxContentSize:
                self.reducePageSize(walletID)
                data = []
            elif data["error"]:
                App_logger.error(f'Page {page} failed to extract transactions from Covalent API. Data has error')
                if data['error_code'] == 406:
                    App_logger.error(f'Covalent Error: {data["error_code"]}, Error Message: {data["error_msg"]}')
                    # Program gets terminated once the following function is executed
                    self.reducePageSize(walletID)
                if not self.failedPage:
                    self.failedPage = page
                data = []
            else:
                App_logger.info(f'Extracted page {page}')
        except requests.exceptions.RequestException as e:
            App_logger.error(f'Covalent API exception caught: {e}')
            App_logger.error(f'Page {page} failed to extract transactions from Covalent API')
            if not self.failedPage:
                self.failedPage = page
            data = []
        App_logger.info(f"Successfully extracted page: {page}")      
        return data

    def GetOneTransactionAPI(self, walletID, txhash, suffix="test"):
        try:
            tokensMetaInfo = self.GetAllContracts(walletID)
            url = EnvSettings.OnetransactionUrl.format(self.chainID, txhash)
            headers = {'Content-Type': 'application/json'}
            response = requests.get(url, headers=headers, timeout=30, auth=(self.key, ""), verify = False)
            data = json.loads(response.text)
            data["data"]["chain_id"] = 1
            data["data"]["address"] = walletID
            data["data"]["TokenMetaData"] = tokensMetaInfo
            # Cache management
            file_name = "-".join([walletID, self.chainID, str(self.pageSize), suffix, "1"]) + ".json"
            file_path = "/".join(["covalent", self.clientID, file_name])
            blobClient = blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path) 
            blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4), overwrite = True)
            return file_path
        
        except Exception as err:
            App_logger.error(err)
            return ""
    
    def GetBalancesAPI(self, chainID, walletID, page):
        url = EnvSettings.BalancesUrl.format(
            chainID, walletID, page, self.key)
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, timeout=100, verify = False)
        data = json.loads(response.text) 
        if data["error"]:
            time.sleep(2.5)
            return self.GetBalancesAPI(chainID, walletID, page)
        return data 

    def GetAllContracts(self, walletID):
        page = 0
        next_page = True
        AllContracts = dict()
        while True:
            if not next_page:
                break
            data = self.GetBalancesAPI(self.chainID, walletID, page)
            for item in data["data"]["items"]:
                AllContracts[item["contract_ticker_symbol"]] = {
                    "symbol": item["contract_ticker_symbol"],
                    "name": item["contract_name"],
                    "address": item["contract_address"],
                    "type": item["type"],
                    "decimals": item["contract_decimals"]
                }
            page += 1
            if data["data"]["pagination"] is not None:
                next_page = data["data"]["pagination"]["has_more"]
            else:
                next_page = False
        return AllContracts

    # Calls the Covalentq API function but caches the response in storage account
    def Get_Transactions(self, walletID, page, tokensMeta = None):
        # Cache management 
        blobClient, file_path = self.createBlobClient(walletID, page)
        # if present in the cache load from it else call the Covalentq API function
        if blobClient.exists():
            App_logger.info(f'Getting page {page} data from cache')
            streamdownloader = blobClient.download_blob()
            data = json.loads(streamdownloader.readall())
        else:
            App_logger.info(f'Getting page {page} data from API')
            data = self.GetTransactionsAPI(walletID, page)
            if data:
                data["data"]["TokenMetaData"] = tokensMeta
                blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4))
                App_logger.info(f'Successfully uploaded the blob of page {page}')
            else:
                App_logger.info(f'No data found retry')
                App_logger.error(f'Failed to load json')
        return data, {"container": "cache", "blob": file_path}

    # Gets the list of transactions 
    def GetAllTransactionByWallet(self, walletID):
        message_list = []
        self.tokensMetaInfo = self.GetAllContracts(walletID)
        self.TokenMeta["Wallet"] = walletID
        self.TokenMeta["TokenMetaData"] = list(self.tokensMetaInfo.values())
        dbSet.insertOneDB(dbSet.getTokens(), filter=self.TokenMeta)
        next_page = True
        page = 0
        while next_page:
            data, filePath = self.Get_Transactions(walletID, page, self.tokensMetaInfo)
            if data:
                next_page = data["data"]["pagination"]["has_more"]
                page = data["data"]["pagination"]["page_number"] + 1
                message = {
                    "clientID": self.clientID,
                    "chainName": self.chainName,
                    "wallet": walletID
                }
                message.update(filePath)
                message_list.append(message)
            else:
                break
        return message_list
    
    # This function validates the wallet by calling transactions API
    def validateWallet(self, walletID, count = 1):
        url = EnvSettings.validateWallet.format(self.chainID, walletID, 0, 100, self.key)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(url, headers=headers, timeout=30, verify = False)
            data_valid = json.loads(response.text)
            if data_valid["error"]:
                return "Invalid"
            else:
                App_logger.info("Wallet successfully validated")
                return "Valid"
        except:
            if count > config.maxValidationTry:
                App_logger.error("Covalent API errored out 5 times validating wallet")
                return "timeout"
            time.sleep(2)
            return self.validateWallet(walletID, count+1)
        
    def handleFailedPages(self, walletID, msg_list):
        # Wait for 20 seconds before trying the covalent API again
        time.sleep(20)
        page = self.failedPage
        next_page = True
        while next_page:
            data = self.GetTransactionsAPI(walletID, page)
            if data:
                data["data"]["TokenMetaData"] = self.TokenMetaInfo
                # Cache management
                blobClient, file_path = self.createBlobClient(walletID, page)
                blobClient.upload_blob(json.dumps(data, ensure_ascii=False, indent=4))
                next_page = data["data"]["pagination"]["has_more"]
                page = data["data"]["pagination"]["page_number"] + 1
                metaData = {"container": "cache", "blob": file_path}
                message = {
                    "clientID": self.clientID,
                    "chainName": self.chainName,
                    "wallet": walletID
                }
                message.update(metaData)
                msg_list.append(message)
            else:
                App_logger.error(f'Wallet failed to extract transactions on second try for page {page}. Wallet failed')
                self.walletPassed = False
                self.sendFail(walletID)

    # This function updates the number of transactions that calls the API 
    def UpdateStatus(self, taskCount: int):
        filter = {'clientId': self.clientID}
        proj = {'$inc': {'classification': -1 + taskCount}}
        dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, proj)

    # Send message to the queue & Update Cosmos DB status of the wallet to "processing"
    def SendMessage(self, msg_list: list):
        for msg in msg_list:
            self.queue_client.send_message(json.dumps(msg, default=str))
    
    def createBlobClient(self, walletID, page):
        file_name = "-".join([walletID, self.chainID, str(self.pageSize), str(page)]) + ".json"
        file_path = "/".join(["covalent", self.clientID, file_name])
        return blobSet.blob_service_client.get_blob_client(container="cache", blob=file_path), file_path
    
    def sendFail(self, wallet):
        filter = {'clientId': self.clientID}, 
        proj = {'$inc': {'classification': -1}}
        dbSet.findOneUpdateDB(dbSet.getStatuses(), filter, proj)

        filter = {"clientId" : self.clientID, "wallets.address" : wallet}
        proj = {"$set" : {"wallets.$.status" : "Failed"}}
        dbSet.updateOneDB(dbSet.getWallets(), filter, proj)

    def reducePageSize(self, wallet):
        # "chainID", "chainName", "clientId", "wallet", "pageSize" 
        msg = {
            'chainID': self.chainID,
            'chainName': self.chainName, 
            'clientId': self.clientID, 
            'wallet': wallet,
            'pageSize': int(self.pageSize/2)
        }
        App_logger.error(f"ContentSize exceeded: {config.maxContentSize} MB, Reducing the the page size from {self.pageSize} to {msg['pageSize']}")
        queue_client = queueSet.get_queue_client(queueName="covalentq")
        queue_client.send_message(json.dumps(msg, default=str))
        self.terminate = True

    def StartExtraction(self, wallet):
        status = self.validateWallet(wallet)
        if status == "Valid":
            msg_list = self.GetAllTransactionByWallet(wallet)
            if self.terminate:
                return
            if self.failedPage:
                msg_list = self.handleFailedPages(wallet, msg_list)
            if self.walletPassed:
                self.SendMessage(msg_list)
                self.UpdateStatus(taskCount=len(msg_list))
        else:
            App_logger.info("Wallet address invalid, sending to covalentq-poison")
            self.sendFail(wallet)

if __name__ == "__main__":
    ExtractorParam = {"chainID": "1", "chainName": "Ethereum"}
    wallet = "0xfab97682e0b4b1589786382eeba1b758ffae7ff9"
    txhash = "0x917306f0a8c6f5252fac63e3761f0ef4612513ed8cb540d588f5227a4a6395ff"
    cov = CovalentTransactionExtractor(chainID="1", chainName="Ethereum", clientID="test")
    # tokens = cov.GetAllContracts(walletID=wallet)
    print()
    # cov.GetOneTransactionAPI(wallet, txhash)
    msg_list = cov.GetAllTransactionByWallet(wallet)
    print(msg_list)