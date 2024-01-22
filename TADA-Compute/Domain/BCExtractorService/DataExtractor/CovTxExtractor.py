import re
from collections import defaultdict

from Domain.BCExtractorService.configBCExtractor import model_settting, util
from LoggerUtils import App_logger

class TransactionExtractor:
    def __init__(self, item, metaData):
        # Fill out basic info
        self.TokenMetaData = metaData["TokenMetaData"]
        self.record = {}
        self.record["Wallet"] = metaData["wallet"]
        self.record["Chain"] = metaData["chain_id"]
        self.record["TimeStamp"] = item["block_signed_at"]
        self.record["TxHash"] = item["tx_hash"]
        self.record["Success"] = item["successful"]
        self.record["FromAddress"] = item["from_address"]
        self.record["ToAddress"] = item["to_address"]
        self.record["Value"] = item["value"]
        self.record["GasSpent"] = str(item["gas_spent"])
        self.record["GasPrice"] = str(item["gas_price"])
        self.logEvent = item["log_events"]
        # should get these keywords from config database
        self.fromKeyWords = model_settting.fromKeyWords
        self.toKeyWords = model_settting.toKeyWords
        self.QuantKeyWords = model_settting.quantKeyWords
        self.NFTKeyWords = model_settting.NFTKeyWords
        self.SwapTokens = model_settting.swapTokens
        
        chainSym = model_settting.chainParam[self.record['Chain']]['Symbol']
        chainDec = model_settting.chainParam[self.record['Chain']]['Decimal']
        # Variables required for classification & Set some default values
        self.TxSigns = defaultdict(list)
        self.ContractValuePairs = defaultdict(set)
        self.ContractValuePairs[chainSym].add(self.record['Value'])
        self.DecimalRep = dict()
        self.DecimalRep[chainSym+self.record['Value']] = int(self.record['Value'])/10**chainDec
        self.DecimalValue = dict()
        self.DecimalValue[chainSym] = chainDec
        # Inputs for ML Classifier & Logic based Classifier
        self.MLBasedClassifierInput  = {
            "hash": self.record["TxHash"],
            "wallet": self.record["Wallet"],
            "ContractValues": defaultdict(list),
            "DecimalValue": self.DecimalValue,
            "data": []
        }
        self.LogicBasedClassifierInput = {
            "record": self.record,
            "ContractValues": defaultdict(list),
            "DecimalValue": self.DecimalValue,
            "DecimalRep": self.DecimalRep,
            "TxSigns": self.TxSigns
        }
        # Extract Signatures
        if self.logEvent is not None:
            if len(self.logEvent) > 0:
                self.ExtractSignatures()
                self.GenerateDataset()
        # Classify by Signatures
        
    def ExtractSignatures(self):
        for log in self.logEvent:
            if log["decoded"] is not None:
                if log["decoded"]["params"] is not None:
                    info = {}
                    # Param is a list of parameters for a signature
                    param = log["decoded"]["params"]
                    # fill gaps if not decoded completely using raw topic logs
                    for i in range(len(param)):
                        if (not param[i]["decoded"]) and (param[i]["value"] is None):
                            param[i]["value"] = log["raw_log_topics"][i + 1]
                    info["LogOffset"] = log["log_offset"] # Not Necessary information i guess
                    info["Decimal"] = log["sender_contract_decimals"] if log["sender_contract_decimals"] != None else 0
                    info["ContractName"] = log["sender_name"]
                    info["ContractAddr"] = log['sender_address']
                    if log["sender_contract_ticker_symbol"] is not None:
                        info["Symbol"] = log["sender_contract_ticker_symbol"]
                        if info["Symbol"] not in self.TokenMetaData.keys() and info['ContractAddr'] is not None:
                            self.TokenMetaData[info["Symbol"]] = {
                                'symbol': info['Symbol'],
                                'name': info['ContractName'],
                                'address': info['ContractAddr'],
                                'decimals': info["Decimal"]
                            }
                        info["Decimal"] = self.TokenMetaData[info["Symbol"]]["decimals"] if info["Symbol"] in self.TokenMetaData.keys() else info["Decimal"]
                    else:
                        info["Symbol"] = "null"
                    self.DecimalValue[info["Symbol"]] = info["Decimal"]
                    # info["Symbol"] = log["sender_contract_ticker_symbol"] if not None else "null"
                    info["Param"] = param
                    direction = []
                    values = {}
                    tokens = {}
                    hasWalletAddress = False
                    from_to = {'from': [], 'to': []}
                    for obj in param:
                        obj_name_list = re.split(r'[^a-zA-Z0-9\s]', obj["name"])
                        if re.match("^address", obj["type"]):
                            addr = util.GetValueList(obj["value"])
                            if self.record["Wallet"] in addr:
                                hasWalletAddress = True
                            if sum([x in obj_name.lower() for x in self.fromKeyWords for obj_name in obj_name_list]) > 0:
                                from_to["from"] += addr
                                if self.record["Wallet"] in addr:
                                    direction.append(1)
                            elif sum([re.match(x, obj_name.lower())!=None for x in self.toKeyWords for obj_name in obj_name_list]) > 0:
                                from_to["to"] += addr
                                if self.record["Wallet"] in addr:
                                    direction.append(-1)
                        # Can be broken down into NFT & ERC20
                        elif sum([x in obj_name.lower() for x in self.QuantKeyWords for obj_name in obj_name_list]) > 0:
                            val = []
                            if re.match("^uint", obj["type"].lower()):
                                val = [int(x, 0) for x in util.GetValueList(obj["value"])]
                            elif re.match("[0-9]*int", obj["type"].lower()):
                                val = [int(x) for x in util.GetValueList(obj["value"])]
                            if len(val) > 0:
                                values[obj["name"]] = val
                                for v in val: 
                                    self.ContractValuePairs[info["Symbol"]].add(str(v))
                                    try:
                                        self.DecimalRep[info["Symbol"]+str(v)] = str(int(v)/10**info["Decimal"])
                                    except Exception as e:
                                        App_logger.warning(f"exception: {e} \nParm: {obj}\nDecimal: {info['Decimal']};")
                        elif sum([x in obj_name.lower() for x in self.NFTKeyWords for obj_name in obj_name_list]) > 0:
                            val = []
                            if re.match("^uint", obj["type"].lower()):
                                val = [int(x, 0) for x in util.GetValueList(obj["value"])]
                            elif re.match("[0-9]*int", obj["type"].lower()):
                                val = [int(x) for x in util.GetValueList(obj["value"])]
                            if len(val) > 0:
                                tokens[obj["name"]] = val
                    info['From_Address'] = from_to["from"]
                    info['To_Address'] = from_to["to"]
                    info['HasWalletAddress'] = hasWalletAddress
                    info['Values'] = values
                    info['Tokens'] = tokens
                    info['Direction'] = direction
                    self.TxSigns[log["decoded"]["name"]].append(info)
        # Add native Token 
        
        # Remove swap contract & null contract 
        contract_keys = list(self.ContractValuePairs.keys())
        [self.ContractValuePairs.pop(x, "not present") for x in contract_keys for key in self.SwapTokens +['null'] if re.match(key, x.lower())]
        decimalVal_keys = list(self.DecimalValue.keys())
        [self.DecimalValue.pop(x, "not present") for x in decimalVal_keys for key in self.SwapTokens +['null'] if re.match(key, x.lower())]
        decimalRep_keys = list(self.DecimalRep.keys())
        [self.DecimalRep.pop(x, "not present") for x in decimalRep_keys for key in self.SwapTokens +['null'] if re.match(key, x.lower())]
        # Saving information for export
        modified_ContractValue = {}
        for key, value in self.ContractValuePairs.items():
            modified_ContractValue[key] = list(value)
        self.LogicBasedClassifierInput = {
            "record": self.record,
            "ContractValues": modified_ContractValue,
            "DecimalValue": self.DecimalValue,
            "DecimalRep": self.DecimalRep,
            "TxSigns": self.TxSigns
        }

    def GenerateDataset(self):
        modified_ContractValue = {}
        for key, value in self.ContractValuePairs.items():
            modified_ContractValue[key] = list(value)
        dataset = {
            "hash": self.record["TxHash"],
            "wallet": self.record["Wallet"],
            "ContractValues": modified_ContractValue,
            "DecimalValue": self.DecimalValue,
            "data": []
        }
        for log in self.logEvent:
            if log["decoded"] is not None:
                if log["decoded"]["params"] is not None:
                    # Param is a list of parameters for a signature
                    param = log["decoded"]["params"]
                    for i in range(len(param)):
                        if (not param[i]["decoded"]) and (param[i]["value"] is None):
                            param[i]["value"] = log["raw_log_topics"][i + 1]
                    dataset["data"].append({
                        "signature": log["decoded"]["name"],
                        "params" : param.copy()
                    })
        self.MLBasedClassifierInput = dataset

if __name__ == "__main__":
    print()
    # status = TransactionExtractor("testuser", "0x5125e63cdb4e171921a1664831fcaaf1fb85bfff")


    

                


                    
                
                

    
