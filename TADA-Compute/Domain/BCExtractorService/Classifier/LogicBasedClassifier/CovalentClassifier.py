import re
from collections import defaultdict
from Domain.BCExtractorService.configBCExtractor import util, model_settting

from LoggerUtils import App_logger

class ClassifierLogic:
    def __init__(self, data, TokenMetaData):
        self.TokenMetaData = TokenMetaData
        self.record = data["record"]
        self.TxSigns = data["TxSigns"]
        self.ContractValuePairs = data["ContractValues"]
        self.DecimalRep = data["DecimalRep"]
        self.DecimalValue = data["DecimalValue"]
        # Should get these keywords from Config database
        self.ignoreSignList = model_settting.chainParam[self.record['Chain']]['IgnoreSigns'] # Regex
        self.AutoClassifySign_list = model_settting.chainParam[self.record['Chain']]['AutoClassify'] # Regex
        self.Flag_TxByWallet = True if self.record["Wallet"] in [self.record["FromAddress"], self.record["ToAddress"]] else False
        self.NativeToken = model_settting.chainParam[self.record['Chain']]['Symbol']
        self.NativeToken_Decimal = 10**model_settting.chainParam[self.record['Chain']]['Decimal']
        self.TxActions = []
        self.TxActions_Unclassified = []
        self.discarded_txs = []
        
    def CalculateFee(self):
        try:
            if not self.Flag_TxByWallet:
                return []
            return [{
                "ChainID": self.record["Chain"],
                "TxHash": self.record["TxHash"],
                "Wallet": self.record["Wallet"],
                "TimeStamp": self.record["TimeStamp"],
                "Status": self.record["Success"],
                "From": self.record["FromAddress"],
                "To": self.record["ToAddress"],
                "Token": self.NativeToken,
                "Amount": str(int(self.record["GasPrice"]) * int(self.record["GasSpent"]) / self.NativeToken_Decimal),
                "TxDirection": "OUT" if self.record["Wallet"] == self.record["FromAddress"] else "IN",
                "TransactionDesc": "Transaction Fee",
                "Price": "",
                "TokenMeta": self.TokenMetaData[self.NativeToken] if self.NativeToken in self.TokenMetaData.keys() else {}
            }]
        
        except Exception as err:
            App_logger.error(err)


    def Classify(self):
        try:
            nft_tx = []
            self.TxSigns['Swap'] = self.TxSigns['Swap'] + self.TxSigns['Fill']
            if "Swap" in self.TxSigns.keys() and self.Flag_TxByWallet:
                clf, unclf = self.SwapTransaction()
                self.TxActions += clf
                self.TxActions_Unclassified += unclf
            else:
                clf, unclf, nfts = self.OtherTransaction()
                self.TxActions_Unclassified += unclf
                self.TxActions += clf
                nft_tx += nfts
            # Get Native Token value at Transaction level if there are no logs or unable to deciper any logs (this logic prevents double counting)
            if len(self.TxSigns) == 0 or len(self.TxActions) + len(self.TxActions_Unclassified) + len(nft_tx) == 0:
                self.TxActions += self.SimpleTransaction()
            # Add Token Amount to NFT transactions
            clf, unclf = self.NFT_TokenAmount(nft_tx)
            self.TxActions += clf
            self.TxActions_Unclassified += unclf
            # !Add Transaction Fee should be added at the end
            self.TxActions += self.CalculateFee()
            return self.TxActions, self.TxActions_Unclassified
        
        except Exception as err:
            App_logger.error(err)

    def NFT_TokenAmount(self, nft_tx):
        App_logger.info("Calculating NFT Token Amount")
        clf = []
        unclf = []
        """
        This logic can accommodate nft_txs > 0 but for simplicity we set nft_txs = 1
        """
        if len(self.TxActions_Unclassified) == 0 and len(nft_tx) == 1:
            Token_Amt_list = self.GetTokenAmount(len(nft_tx))
            for tx in nft_tx:
                tx['Price'] = Token_Amt_list
                if len(Token_Amt_list) > 1 or "Log" in tx.keys():
                    unclf.append(tx)
                    tx['Price'] = ""
                else:
                    if len(Token_Amt_list) == 1:
                        self.TxActions.remove(Token_Amt_list[0])
                        clf.append(tx)
                    elif len(Token_Amt_list) == 0:
                        unclf.append(tx)
                        tx['Price'] = ""
            return clf, unclf
        else:
            return clf, nft_tx
        
    def GetTokenAmount(self, nft_count):
        token_amt_list = []
        for tx in self.TxActions:
            if len(tx['Token']) > 0:
                token_amt_list.append(tx)
        return token_amt_list

    def SimpleTransaction(self):
        txs = []
        tx= {}
        tx["ChainID"] = self.record["Chain"]
        tx["Wallet"] = self.record["Wallet"]
        tx["TimeStamp"] = self.record["TimeStamp"]
        tx["TxHash"] = self.record["TxHash"]
        tx["Status"] = self.record["Success"]
        tx["From"] = self.record["FromAddress"]
        tx["To"] = self.record["ToAddress"]
        tx["Price"] = ""
        if self.record["FromAddress"] == self.record["Wallet"]:
            tx["TxDirection"] = "OUT"
        else:
            tx["TxDirection"] = "IN"
        # Check chain to set Token, Amount, Desc
        tx["Token"] = self.NativeToken
        tx["Amount"] = str(int(self.record["Value"]) / self.NativeToken_Decimal)
        tx["TransactionDesc"] = f"Transfer {self.NativeToken}"
        tx["TokenMeta"] = self.TokenMetaData[tx["Token"]]
        txs.append(tx)
        return txs

    def SwapTransaction(self):
        try:
            App_logger.info("Swap Transaction")
            hashedParam = []
            txsList = []
            for swap in self.TxSigns["Swap"]:
                hashed_dict = {}
                for obj in swap["Param"]:
                    hashed_dict[obj["name"]] = obj["value"]
                hashedParam.append(hashed_dict)
            for i in range(len(self.TxSigns["Swap"])):
                param = hashedParam[i]
                # Test if keys are present for Swap V2 
                KeysNotPresent_v2 = set(["amount0In", "amount1In", "amount0Out", "amount1Out"]).difference(set(param.keys()))
                KeysNotPresent_v3 = set(["amount0", "amount1"]).difference(set(param.keys()))
                KeysNotPresent_Fill_v1 = set(["takerAddress","senderAddress","makerAssetFilledAmount",
                                            "takerAssetFilledAmount","makerFeePaid","takerFeePaid","makerAssetData","takerAssetData"]).difference(set(param.keys()))
                if len(KeysNotPresent_v2) == 0:
                    SumIn = str(int(param["amount0In"]) + int(param["amount1In"]))
                    SumOut = str(int(param["amount0Out"]) + int(param["amount1Out"]))
                    simple_second_cond = sum([param["amount0In"] == "0", param["amount1Out"] == "0"]) != 2
                    # Simple Swap
                    if param["sender"] == param["to"] and simple_second_cond:
                        In_Value = param["amount0In"]
                        Out_Value = param["amount1Out"]
                        txsList += self.SwapCase_Simple(self.TxSigns["Swap"][i], In_Value, Out_Value)
                    else:
                        In_Value = ""
                        Out_Value = ""
                        if "0" in [param["amount0In"], param["amount1In"]] and SumIn != "0":
                            In_Value = SumIn
                        if "0" in [param["amount0Out"], param["amount1Out"]] and SumOut != "0":
                            Out_Value = SumOut
                        if len(In_Value) > 0 and len(Out_Value) > 0:
                            txsList += self.SwapCase_Simple(self.TxSigns["Swap"][i], In_Value, Out_Value)
                        else:
                            txsList += self.SwapExceptionCase(self.TxSigns["Swap"][i])
                elif len(KeysNotPresent_v3) == 0:
                    amount0 = param['amount0']
                    amount1 = param['amount1']
                    In_Value = None
                    Out_Value = None
                    if int(amount0) < 0 and int(amount1) >= 0:
                        Out_Value = str(abs(int(param['amount0'])))
                        In_Value = param['amount1']
                    elif int(amount0) >= 0 and int(amount1) < 0:
                        Out_Value = str(abs(int(param['amount1'])))
                        In_Value = param['amount0']
                    if In_Value == None or Out_Value == None:
                        txsList += self.SwapExceptionCase(self.TxSigns["Swap"][i])
                    else:
                        txsList += self.SwapCase_Simple(self.TxSigns["Swap"][i], In_Value, Out_Value)
                elif len(KeysNotPresent_Fill_v1) == 0:
                    makerAssetFilledAmount = param['makerAssetFilledAmount']
                    takerAssetFilledAmount = param['takerAssetFilledAmount']
                    Out_Value = takerAssetFilledAmount
                    In_Value = makerAssetFilledAmount
                    if len(In_Value) > 0 and len(Out_Value) > 0:
                        txsList += self.SwapCase_Simple(self.TxSigns["Swap"][i], In_Value, Out_Value)
                    else:
                        txsList += self.SwapExceptionCase(self.TxSigns["Swap"][i])
                else:
                    txsList += self.SwapExceptionCase(self.TxSigns["Swap"][i])
            clf = []
            unclf = []
            for txs in txsList:
                if "Log" in txs.keys():
                    unclf.append(txs)
                else:
                    clf.append(txs)
            return clf, unclf
        
        except Exception as err:
            App_logger.info(err)

    def OtherTransaction(self):
        try:
            App_logger.info("Other Transactions")
            clf_txs = []
            unclf_txs = []
            nft_txs = []
            for sign, info_list in self.TxSigns.items():
                for info in info_list:
                    ignoreTxs = False
                    # Extract User defined variables 
                    hasWalletAddress = info['HasWalletAddress'] 
                    direction = info['Direction']
                    values = info['Values']
                    from_to = {"from": info['From_Address'], "to": info['To_Address']}
                    tokens = info['Tokens']
                    # End of User defined variables
                    # Ignore certain TxSigns
                    if sum([re.match(x, sign.lower())!=None for x in self.ignoreSignList]) > 0:
                        ignoreTxs = True
                    from_addr = from_to["from"][0] if len(from_to["from"]) == 1 else ""
                    to_addr =  from_to["to"][0] if len(from_to["to"]) == 1 else ""
                    try:
                        amt = str(values[list(values.keys())[0]][0]/10**info["Decimal"]) if len(values) == 1 else ""
                    except:
                        amt = ""
                    # Figure out Token if it is 'null'
                    if info['Symbol'] == 'null' and len(amt) > 0:
                        temp_val = str(values[list(values.keys())[0]][0])
                        temp_token = self.GetTokenByValue(temp_val)
                        info['Symbol'] = temp_token if temp_token != 'UNK' else ''
                        # When you have both temp_val & temp_token, you will have DecimalRep for the combination
                        if len(info['Symbol']) > 0 and info['Symbol'] in self.DecimalValue.keys():
                            amt = str(values[list(values.keys())[0]][0]/10**self.DecimalValue[info['Symbol']])
                    # Fill out all fields except TxDirection & TxDescription
                    Tx = {
                        "ChainID": self.record["Chain"],
                        "TxHash": self.record["TxHash"],
                        "Wallet": self.record["Wallet"],
                        "TimeStamp": self.record["TimeStamp"],
                        "Status": self.record["Success"],
                        "From": from_addr,
                        "To": to_addr,
                        "Token": info["Symbol"],
                        "Amount": amt,
                        "TxDirection": "",
                        "TransactionDesc": sign,
                        "Price": "",
                        "TokenMeta": self.TokenMetaData[info["Symbol"]] if info["Symbol"] in self.TokenMetaData.keys() else {}
                    }
                    # if we know transaction direction 
                    if len(direction) != 0:
                        # if the direction is not "self", Assign TxDirection
                        if sum(direction) != 0:
                            ValueSign = sum(direction) / abs(sum(direction))
                            Tx["TxDirection"] = "OUT" if ValueSign > 0 else "IN"
                            # if some value/token associated with the transaction
                            if len(values) > 0 or len(tokens) > 0:
                                # if it is an NFT (Token takes priority over Values) because if you have token id, the amount is 1
                                if len(tokens) > 0:
                                    Tx["hasNFT"] = True
                                    # Number of tokens is 1 then extract the information
                                    if len(tokens) == 1:
                                        Tx["TransactionDesc"] += " NFT ID:" + str(tokens[list(tokens.keys())[0]][0])
                                        Tx['NFT_ID'] = str(tokens[list(tokens.keys())[0]][0])
                                        Tx['Amount'] = amt if len(amt) > 0 else '1'
                                    else:
                                        # if there is more than one token, move to unclassified for review
                                        # Presence of this key represents the Tx needs to pushed to Unclassified
                                        Tx["Log"] = {sign: ""}
                                # if this an ERC20 txs, not NFT
                                # number of values is 1, we need not assign amount because it is already assigned above 
                                elif len(values) == 1:
                                    Tx["TransactionDesc"] += " " + info["Symbol"]
                                # if number of values is more than one, send to unclassified for review
                                else:
                                    Tx["Log"] = {sign: ""}
                            # if no values are found, send to unclassified for review
                            else:
                                Tx["Log"] = { sign: "" }
                        # if direction is self
                        else:
                            Tx["Log"] = { sign: "" }
                    # if there no Tx direction, but wallet address is present as one of the addresses
                    elif hasWalletAddress:
                        Tx["Log"] = { sign: "" }
                    else:
                        ignoreTxs = True
                    # if Amount is 0 or either from/to addr are missing, send to unclassified for review by adding a key "Log"
                    if len(Tx["Amount"]) == 0 or from_addr == "" or to_addr == "": Tx["Log"] = {sign: ""}
                    # If no there is no token meta add "Log"
                    if len(Tx["TokenMeta"]) == 0 and 'hasNFT' not in Tx.keys():
                        Tx["Log"] = { sign: "" }
                    # Bucket the transaction to either clf, unclf or discard it
                    if ignoreTxs:
                        self.discarded_txs.append(info_list)
                    elif "hasNFT" in Tx.keys():
                        Tx['Price'] = []
                        nft_txs.append(Tx)
                    elif "Log" in Tx.keys() or sum([re.match(x, sign.lower())!=None for x in self.AutoClassifySign_list]) == 0:
                        unclf_txs.append(Tx)
                    else:
                        clf_txs.append(Tx)
            return clf_txs, unclf_txs, nft_txs
        
        except Exception as err:
            App_logger.info(err)

    def GetTokenByValue(self, qty):
        # Initialize Token as UNK
        Token = "UNK"
        # Try getting exact Token from the value
        for token in self.ContractValuePairs.keys():
            if qty in self.ContractValuePairs[token]:
                Token = token
        # If we couldnt find exact match, look for approximate match
        if Token == "UNK":
            tokenList = []
            # Look for Approximate valued Tokens
            for token, valueList in self.ContractValuePairs.items():
                for value in valueList:
                    if util.CloseValues(int(qty), int(value), threshold=0.0005):
                        tokenList.append(token)
            uniqueTokenList = list(set(tokenList))
            # if there is one unique token that has approximate match
            if len(uniqueTokenList) == 1:
                Token = uniqueTokenList[0]
            # Else just let the Token be "UNK"
        return Token
    
    def SwapCase_Simple(self, TxSign, In_Value, Out_Value):
        try:
            # In_Value = hashedParam["amount0In"]
            In_Token = self.GetTokenByValue(In_Value)
            Out_Token = self.GetTokenByValue(Out_Value)
            remaining_tokens = list(set(self.ContractValuePairs.keys()).difference(set([In_Token, Out_Token])))
            if In_Token == "UNK" and len(remaining_tokens) == 1:
                In_Token = remaining_tokens[0]
            elif Out_Token == "UNK" and len(remaining_tokens) == 1:
                Out_Token = remaining_tokens[0]
            if In_Token != "UNK" and Out_Token != "UNK":
                AmtOut = str(int(In_Value)/10**self.DecimalValue[In_Token]) if In_Token in self.DecimalValue.keys() else ""
                AmtOut = self.DecimalRep[In_Token+In_Value] if len(AmtOut) == 0 else AmtOut
                AmtOut = str(int(In_Value)/10**TxSign["Decimal"]) if len(AmtOut) == 0 else AmtOut
                # Generate two transactions
                OutTx = {
                    "ChainID": self.record["Chain"],
                    "TxHash": self.record["TxHash"],
                    "Wallet": self.record["Wallet"],
                    "TimeStamp": self.record["TimeStamp"],
                    "Status": self.record["Success"],
                    "From": self.record["Wallet"],
                    "To": self.record["ToAddress"],
                    "Token": In_Token,
                    "Amount": AmtOut,
                    "TxDirection": "OUT",
                    "TransactionDesc": "Swap OUT " + In_Token,
                    "Price": "",
                    "TokenMeta": self.TokenMetaData[In_Token] if In_Token in self.TokenMetaData.keys() else {}
                }
                AmtIn = str(int(Out_Value)/10**self.DecimalValue[Out_Token]) if Out_Token in self.DecimalValue.keys() else ""
                AmtIn = self.DecimalRep[Out_Token+Out_Value] if len(AmtIn) == 0 else AmtIn
                AmtIn = str(int(Out_Value)/10**TxSign["Decimal"]) if len(AmtIn) == 0 else AmtIn
                InTx = {
                    "ChainID": self.record["Chain"],
                    "TxHash": self.record["TxHash"],
                    "Wallet": self.record["Wallet"],
                    "TimeStamp": self.record["TimeStamp"],
                    "Status": self.record["Success"],
                    "From": self.record["ToAddress"],
                    "To": self.record["Wallet"],
                    "Token": Out_Token,
                    "Amount": AmtIn,
                    "TxDirection": "IN",
                    "TransactionDesc": "Swap IN "+ Out_Token,
                    "Price": "",
                    "TokenMeta": self.TokenMetaData[Out_Token] if Out_Token in self.TokenMetaData.keys() else {}
                }
                if len(InTx["Amount"]) == 0 or len(InTx["TokenMeta"]) == 0: InTx["Log"] = {"Swap": ""}
                if len(OutTx["Amount"]) == 0 or len(OutTx["TokenMeta"]) == 0: OutTx["Log"] = {"Swap": ""}
                return [InTx, OutTx]
            else:
                # Record this transaction
                return self.SwapExceptionCase(TxSign)
        
        except Exception as err:
            App_logger.error(err)

    def SwapExceptionCase(self, TxSign):
        InTx = {
            "ChainID": self.record["Chain"],
            "TxHash": self.record["TxHash"],
            "Wallet": self.record["Wallet"],
            "TimeStamp": self.record["TimeStamp"],
            "Status": self.record["Success"],
            "From": self.record["ToAddress"],
            "To": self.record["Wallet"],
            "Token": "",
            "Amount": "",
            "TxDirection": "IN",
            "TransactionDesc": "Swap IN (?)",
            "Price": "",
            "TokenMeta": {},
            "Log": {"Swap": ""}
            }
        OutTx = {
            "ChainID": self.record["Chain"],
            "TxHash": self.record["TxHash"],
            "Wallet": self.record["Wallet"],
            "TimeStamp": self.record["TimeStamp"],
            "Status": self.record["Success"],
            "From": self.record["Wallet"],
            "To": self.record["ToAddress"],
            "Token": "",
            "Amount": "",
            "TxDirection": "OUT",
            "TransactionDesc": "Swap Out (?)",
            "Price": "",
            "TokenMeta": {},
            "Log": {"Swap": ""}
        }
        return [InTx, OutTx]

