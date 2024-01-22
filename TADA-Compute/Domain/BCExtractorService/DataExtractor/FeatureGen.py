import json
import pprint
import sys
from Domain.BCExtractorService.DataExtractor.CovTxExtractor import TransactionExtractor

from Infrastructure.blobMgmt import blobSet
from LoggerUtils import App_logger

YEAR_FILTER = ""

class ClassificationFeatureGenerator:
    def load_data_from_blob(self, container, blob):
        blobClient = blobSet.blob_service_client.get_blob_client(container=container, blob=blob)
        if blobClient.exists():
            streamdownloader = blobClient.download_blob()
            data = json.loads(streamdownloader.readall())
        else:
            sys.exit(f"Unable to find blob: {blob}")
        return data

    # Gets the list of transactions 
    def ExtractTransactions(self, data):
        meta_data = {
            "wallet": data["address"],
            "chain_id": data["chain_id"],
            "TokenMetaData": data["TokenMetaData"]
        }
        failed_txs = []
        Transaction_list_Logic = []
        Transaction_dict_ML = {}
        ListOfTokens = []
        for item in data["items"]:
            if item["successful"] is True:
                tranx = TransactionExtractor(item, meta_data)
                if len(tranx.LogicBasedClassifierInput) > 0:
                    Transaction_list_Logic.append(tranx.LogicBasedClassifierInput)
                    ListOfTokens += list(tranx.ContractValuePairs.keys())
                    if "hash" in tranx.MLBasedClassifierInput.keys():
                        Transaction_dict_ML[tranx.MLBasedClassifierInput["hash"]] = tranx.MLBasedClassifierInput
                else:
                    App_logger.warning(f"Input for BCExtractor Logic not found for the item -> {item}")
            else:
                # Store the failed txs in the list 
                failed_txs.append(item)
                # TODO: Write the failed txs to a blob
        token_list = list(set(ListOfTokens))
        token_list = [str(x.encode('utf-8')) for x in token_list]
        # Some token can have weird unicode character, encode them to utf-8
        App_logger.info(f"Wallet({data['address']}) TokenList: {token_list}")
        return Transaction_list_Logic, Transaction_dict_ML, list(set(ListOfTokens))

if __name__ == "__main__":
    extractor = ClassificationFeatureGenerator()
    pp = pprint.PrettyPrinter(indent=4)
    BlobJson = extractor.load_data_from_blob("cache", "covalent/test/0x5125e63cdb4e171921a1664831fcaaf1fb85bfff-1-1000-0.json")
    txList, txDict, tkList = extractor.ExtractTransactions(BlobJson["data"])
    print(len(txList), len(txDict), len(tkList))
    print()
    # extractor.ExportWalletToCSV("0x71CF4Af25Def08C74A9eed3460EEd3bE36ac9Cff")