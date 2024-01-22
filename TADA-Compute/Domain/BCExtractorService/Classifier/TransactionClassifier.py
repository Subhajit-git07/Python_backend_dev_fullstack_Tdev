from Domain.BCExtractorService.Classifier.LogicBasedClassifier.EthereumLogic import EtherClassifier
from Domain.BCExtractorService.Classifier.LogicBasedClassifier.AvalancheLogic import AvaxClassifier
from Domain.BCExtractorService.Classifier.LogicBasedClassifier.RoninLogic import RoninClassifier
import datetime

from LoggerUtils import App_logger

class TxClassifier:
    def __init__(self, chainID: str, dataList: list, dataDict: dict, TokenList: list, TokenMetaData: list):
        self.classifierObj = None
        self.LogicData = dataList
        self.MLData = dataDict
        self.TokenPrices = dict()
        self.TokenMetaData = TokenMetaData
        if chainID == "1":
            self.classifierObj = EtherClassifier
            TokenList.append("ETH")
        elif chainID == "43114":
            self.classifierObj = AvaxClassifier
            TokenList.append("AVAX")
        elif chainID == "2020":
            self.classifierObj = RoninClassifier
            TokenList.append("RON")
        # print(self.TxActions)
    
    def GroupByTokens(self, txs, logTag = ''):
        token_txs = dict()
        no_token_txs = []
        TokenDateRanges = dict()
        for x in txs:
            oneTx = x.copy()
            oneTx['TokenList'] = list(self.TokenMetaData.keys())
            if ('hasNFT' not in oneTx.keys() and len(oneTx["TokenMeta"]) == 0):
                no_token_txs.append(oneTx)
            elif ('hasNFT' in oneTx.keys() and len(oneTx['Price']) != 1):
                oneTx['TokenList'] = [oneTx['Token']]
                no_token_txs.append(oneTx)
            else:
                # Get Token Addr and update TokenList for NFT
                if 'hasNFT' in oneTx.keys():
                    nft_amt_meta = oneTx['Price'][0]['TokenMeta']
                    tokenAddr = nft_amt_meta["address"]
                    oneTx['TokenList'] = [oneTx['Token']]
                else:
                    tokenAddr = oneTx["TokenMeta"]["address"]
                if tokenAddr not in TokenDateRanges.keys():
                    token_txs[tokenAddr] = []
                    TokenDateRanges[tokenAddr] = {"TimeStamp-Min": datetime.datetime.max.strftime('%Y-%m-%dT%H:%M:%SZ'), 
                                                    "TimeStamp-Max":datetime.datetime.min.strftime('%Y-%m-%dT%H:%M:%SZ')}
                timeStamp = oneTx["TimeStamp"]
                TokenDateRanges[tokenAddr]["TimeStamp-Min"] = min(TokenDateRanges[tokenAddr]["TimeStamp-Min"], timeStamp)
                TokenDateRanges[tokenAddr]["TimeStamp-Max"] = max(TokenDateRanges[tokenAddr]["TimeStamp-Max"], timeStamp)
                token_txs[tokenAddr].append(oneTx)
        # For logging: 
        log_count = [len(x) for x in token_txs.values()]
        App_logger.info(f"{logTag} Txs w/ token count: {sum(log_count)} Txs w/o token count: {len(no_token_txs)}")
        return TokenDateRanges, token_txs, no_token_txs

    def StartClassification(self, group_by_token = False):
        clfTxsList = []
        unclfTxsList = []
        for data in self.LogicData:
            classifierObjInit = self.classifierObj(data, self.TokenMetaData)
            clf, unclf = classifierObjInit.Classify()
            clfTxsList += clf
            unclfTxsList += unclf
        App_logger.info(f"Initial: clf count: {len(clfTxsList)}, unclf count: {len(unclfTxsList)}")
        if group_by_token:
            clf_tokens_date_ranges, clf_token_txs, clf_no_token_txs = self.GroupByTokens(clfTxsList, "clf")
            unclf_tokens_date_ranges, unclf_token_txs, unclf_no_token_txs = self.GroupByTokens(unclfTxsList, "unclf")
            TokenTxs = {
                "classified": {
                    "TokenDateRanges": clf_tokens_date_ranges,
                    "Transactions": clf_token_txs
                },
                "unclassified": {
                    "TokenDateRanges": unclf_tokens_date_ranges,
                    "Transactions": unclf_token_txs
                }
            }
            return TokenTxs, clf_no_token_txs + unclf_no_token_txs
        return clfTxsList, unclfTxsList
    

        
        
