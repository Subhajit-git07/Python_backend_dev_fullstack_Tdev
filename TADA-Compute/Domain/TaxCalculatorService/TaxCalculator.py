import numpy as np
from datetime import datetime
import traceback
import json
from dateutil import parser
from uuid import uuid4

from Infrastructure.dbMgmt import dbSet

from LoggerUtils import App_logger

def timeConverter(dateInput):
    dObj = datetime.strptime(str(dateInput), '%Y-%m-%d %H:%M:%S')
    totalDays = dObj.year*365.2425 + dObj.month*30.436875 + dObj.day
    return totalDays

def timeRegulator(dateInput2):
    tReplace = str(dateInput2).replace("T"," ")
    zReplace = str(tReplace).replace("Z","")
    return zReplace

def readClassificationJson(fileName):
    with open(fileName, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    return json_object

class TaxCalculator:
    def __init__(self):
        pass
    
    def findMinimumValue(self, clientId):
        try:
            filterDB = {"clientId": clientId}
            proj = { "taxSummary": 1, "_id": 0}
            taxSummary = dbSet.findOneDB(dbSet.getClients(), filterDB,proj)["taxSummary"]

            totalTaxValues = []
            totalTaxValues.append({
                "mode" : "fifo",
                "totalTax" : taxSummary["fifo"]["totalTax"],
                "ltcg" : taxSummary["fifo"]["ltcg"],
                "stcg" : taxSummary["fifo"]["stcg"]

            })
            totalTaxValues.append({
                "mode" : "lifo",
                "totalTax" : taxSummary["lifo"]["totalTax"],
                "ltcg" : taxSummary["lifo"]["ltcg"],
                "stcg" : taxSummary["lifo"]["stcg"]
            })
            totalTaxValues.append({
                "mode" : "hifo",
                "totalTax" : taxSummary["hifo"]["totalTax"],
                "ltcg" : taxSummary["hifo"]["ltcg"],
                "stcg" : taxSummary["hifo"]["stcg"]
            })

            sortedValues = sorted(totalTaxValues, key=lambda d: d["totalTax"])

            filterDB = {"clientId": clientId}
            proj = {"$set": {"taxLiability.totalTax": sortedValues[0]["totalTax"],
            "taxLiability.ltcg": sortedValues[0]["ltcg"],
            "taxLiability.stcg": sortedValues[0]["stcg"],
            "taxLiability.mode" : sortedValues[0]["mode"]
            }}
            dbSet.updateOneDB(dbSet.getClients(), filterDB, proj)
        
        except Exception as err:
            App_logger.error(err)

    def addNFTValues(self, clientId, userWallets, mode): 
        try:
            # Get NFT Calc and Data 
            aggr_filter = [
                {
                    '$match': {
                        'hasNFT': True, 
                        'TxDirection': 'OUT',
                        'Wallet': {"$in" : userWallets},
                        "Amount" : {"$not" : {"$eq" :"0.0"}},
                        "From": {"$in": userWallets}
                    }
                }, {
                    '$lookup': {
                        'from': 'ClassifiedTxs', 
                        'localField': 'NFT_ID', 
                        'foreignField': 'NFT_ID', 
                        'as': 'IN'
                    }
                }, {
                    '$unwind': '$IN'
                }, {
                    '$match': {
                        'IN.hasNFT': True, 
                        'IN.TxDirection': 'IN',
                        "IN.To": {"$in": userWallets}
                    }
                }, {
                    '$addFields': {
                        'Profit': {
                            '$subtract': [
                                {
                                    '$convert': {
                                        'input': '$Price', 
                                        'to': 'double', 
                                        'onError': 0
                                    }
                                }, {
                                    '$convert': {
                                        'input': '$IN.Price', 
                                        'to': 'double', 
                                        'onError': 0
                                    }
                                }
                            ]
                        }, 
                        'HoldingPeriodDays': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$dateFromString': {
                                                'dateString': '$TimeStamp'
                                            }
                                        }, {
                                            '$dateFromString': {
                                                'dateString': '$IN.TimeStamp'
                                            }
                                        }
                                    ]
                                }, 1000 * 60 * 60 * 24
                            ]
                        }, 
                        'stcgVSltcg': {
                            '$cond': {
                                'if': {
                                    '$lte': [
                                        '$HoldingPeriod', 365
                                    ]
                                }, 
                                'then': 'STCG', 
                                'else': 'LTCG'
                            }
                        },
                        'year': {
                            '$year': {
                                '$dateFromString': {
                                    'dateString': '$TimeStamp'
                                }
                            }
                        }
                    }
                }
            ]
            # nftData = self.tadaDB.get_collection("ClassifiedTxs").aggregate()
            nftData = dbSet.aggregateDB(dbSet.getClassifiedTxs(), aggr_filter)
            nftData = list(nftData)
            STCGvsLTCGObj = {
                "stcg": 0,
                "ltcg": 0
            }
            totalTax = 0
            # Add form row
            for nft in nftData:
                if nft['year'] ==  datetime.today().year - 1: # Create row only for Current Tax Year Sales
                    obj = {
                        "buyPrice" : nft['IN']['Price'],
                        "sellPrice" : nft['Price'],
                        "amount" : min(float(nft['IN']['Amount']),float(nft['Amount'])),
                        "buyDate" : nft['IN']['TimeStamp'],
                        "sellDate" : nft['TimeStamp'],
                        "holdDuration" : int(nft['HoldingPeriodDays']),
                        "buyWallet" : nft['IN']['Wallet'],
                        "sellWallet" : nft['Wallet'],
                        "mode" : mode, 
                        "token" : nft['Token']
                    }
                    # Add summarized values 
                    totalTax += nft['Profit'] # Add total tax to mode
                    STCGvsLTCGObj['stcg' if nft['stcgVSltcg'] == 'STCG' else 'ltcg'] += nft['Profit'] # Add total ltcg or stcg depending on period
                    self.createFormRow(clientId, obj)
        except Exception as err:
            App_logger.error(err)        
        return totalTax,STCGvsLTCGObj['ltcg'],STCGvsLTCGObj['stcg']
        # Get current values
        # curClientData = list(self.tadaDB.get_collection("Clients").aggregate([
        #                     {
        #                         '$match': {
        #                             'clientId': clientId
        #                         }
        #                     }, {
        #                         '$project': {
        #                             'taxSummary': 1
        #                         }
        #                     }
        #                 ]))[0]
        # Add NFT to current values 
        # Update NFT values for all modes
        # for m in modes:
        #     curClientData['taxSummary'][m["mode"]]['totalTax'] += m["data"]['totalTax']
        #     curClientData['taxSummary'][m["mode"]]['ltcg'] += m["data"]['ltcg']
        #     curClientData['taxSummary'][m["mode"]]['stcg'] += m["data"]['stcg']
        # Update obj 
        # config.metaDB.get_collection("PdfFormGeneration").update_one({"clientId" : clientId}, {"$set" : {"8949Form" : []}})
        # self.tadaDB.get_collection("Clients").replace_one({"clientId": clientId}, curClientData, upsert=True) # this does not work 

    def calculateTaxLiability(self, clientId, mode):
        try:
            # Get users wallets
            print("reaching here")
            # Get all Addresses for client, Updated Query to unwind array
            filterDB = [
                                        {"$unwind": {"path": "$wallets"}}
                                        ,{"$match": {"clientId": clientId}}
                                        ,{"$group": {"_id": "$wallets.address"}},
                    ]
            wallets = list(dbSet.aggregateDB(dbSet.getWallets(), filterDB))
            # self.tadaDB.get_collection("Wallets").find_one({"clientId": clientId}, {"clientId" : 0, "_id": 0, "wallets.address": 1})["wallets"]
            # add all addresses in lowercase
            userWallets = [x['_id'].lower() for x in wallets]
            # Set starting values
            taxLiability = 0
            ltcg = 0
            stcg = 0
            # If user has wallets
            if wallets: 
                #Commented out as it is handled above 
                # for wallet in wallets: 
                # # if wallet["status"] == "complete": ##INCLUDE LATER
                #     userWallets.append(wallet["address"])           

                # Get unique list of coins from the clients wallets
                filterDB = "Token"
                proj = {"Wallet" : {"$in" : userWallets}}
                uniqueCoinList = dbSet.getDistinctDB(dbSet.getClassifiedTxs(), filterDB, proj)
                # Loop through coins, calculate tax, and add to total values
                for coin in uniqueCoinList:
                    # Updated Query Filter out NFTs, only use TXs where To or From is in client wallets
                    # Amount is not 0 and Token = Coin
                    # added year column based on timestamp
                    filterDB = [
                        {"$match":
                            {
                                "Token" : coin, 
                                "Wallet": {"$in" : userWallets}, 
                                "Amount" : {"$not" : {"$eq" :"0.0"}},
                                "hasNFT": {"$not":{"$eq": True}},
                                # "TransactionDesc": {"$not" : {"$eq" :"Transaction Fee"}},
                                "$or": [
                                    {"To": {"$in": userWallets}},
                                    {"From": {"$in": userWallets}}
                                ]
                            }
                        },
                        {
                            "$addFields": {
                                "buyRemaining": "$Amount",
                                "year": {"$year": 
                                                    {"$dateFromString": 
                                                            {"dateString": "$TimeStamp"}
                                                    }
                                            }
                            }
                        }
                        
                    ]
                    data = dbSet.aggregateDB(dbSet.getClassifiedTxs(), filterDB)
                    txs = list(data)
                    App_logger.log(3,"Compute TaxCalc, client: "+str(clientId)+", Length of TX Array: "+str(len(txs)))
                    # Not needed here as it s handled above 
                    # Check that for every transaction, the to and from address are both not in the clients wallets
                    # updateddata = []
                    # for transaction in txs:
                    #     if not all(x in userWallets for x in [transaction["To"], transaction["From"]]):
                    #         updateddata.append(transaction)
                    # get min and Max year for Coin's Txs
                    minYear = 0 if len(txs) == 0 else min(txs, key=lambda x:x['year'])['year']
                    maxYear = 0 if len(txs) == 0 else max(txs, key=lambda x:x['year'])['year']
                    # Initialize variables
                    txsBuyRemaining = []
                    coinTaxLiability = 0
                    coinltcg = 0
                    coinstcg = 0
                    # loop through every year and calc the Tax liability and rollover amount 
                    for y in range(minYear,maxYear+1):
                        coinTaxLiability, coinltcg, coinstcg, txsModified = self.basisCalc(
                                                                        txsBuyRemaining + list(filter(lambda t: t['year'] == y,txs))
                                                                        ,mode
                                                                        ,clientId
                                                                        ,y)
                        # Get Txs that have non 0 buyRemaining and are IN TXs
                        txsBuyRemaining = list(filter(lambda t: t['buyRemaining'] != 0 and t['TxDirection'] == 'IN',txsModified))
                        # Change BuyRemaining to amount for next year
                        for t in txsBuyRemaining:
                            t['Amount'] = t['buyRemaining']
                        # Add tax liability for coin to totals
                        # Don't add if Latest Taxable Year is not CurrentYear -1
                        if y == datetime.today().year - 1: 
                            taxLiability += coinTaxLiability
                            ltcg += coinltcg
                            stcg += coinstcg
            # Add log TaxLiability Values
            App_logger.log(3,"Compute TaxCalc, client: "+str(clientId)+", TaxLiability: "+str(taxLiability)+", "+str(ltcg)+", "+str(stcg))
            # Get Nft values for mode, Basis calc done, add NFT To all modes
            nftTaxLiability, nftltcg, nftstcg = self.addNFTValues(clientId, userWallets, mode)
            # Add tax values for this mode to the DB
            # Add log TaxLiability Values
            App_logger.log(3,"Compute TaxCalc, client: "+str(clientId)+", NFT TaxLiability: "+str(nftTaxLiability)+", "+str(nftltcg)+", "+str(nftstcg))
            # Upload tax values to db
            # TODO NFTs here and add to totals
            filterDB = {"clientId": clientId}
            proj = {"$set": {"taxSummary." + mode + ".totalTax": round(float(np.float32(taxLiability))+nftTaxLiability,2), "taxSummary." + mode + ".ltcg": round(float(np.float32(ltcg))+nftltcg,2), "taxSummary." + mode + ".stcg": round(float(np.float32(stcg))+nftstcg,2)}}
            dbSet.updateOneDB(dbSet.getClients(), filterDB, proj)

            # Update taxCalculation status
            filterDB = {"clientId" : clientId}
            proj = {"$inc" : {"taxCalculation" : -1}}
            dbSet.updateOneDB(dbSet.getStatuses(), filterDB, proj)

            # If Tax Calculation is complete, find mode with minimum tax and set to clients tax liability value
            filterDB = {"clientId" : clientId}
            if dbSet.findOneDB(dbSet.getStatuses(), filterDB)["taxCalculation"] == 0:
                # Find MinValue including NFT's
                self.findMinimumValue(clientId)
        
        except Exception as err:
            App_logger.error(err)

    def createFormRow(self, clientId, obj):
        try:
            # Get 8949 form config
            filterDB = {"form" : "8949", "year" : "2022"}
            sections = dbSet.findOneDB(dbSet.getFormConfigs(), filterDB)["sections"]
            # Select section based on the pair hold duration
            if (obj["holdDuration"]) <= 365:
                section = [section for section in sections if section["sectionName"] == "Short-Term"]
            else:
                section = [section for section in sections if section["sectionName"] == "Long-Term"]
            # Get column information
            description = f'{obj["amount"]} {obj["token"]}'
            aquiredDateObj = parser.parse(obj["buyDate"])
            dateAquired = aquiredDateObj.strftime('%m-%d-%Y')
            soldDateObj = parser.parse(obj["sellDate"])
            dateSold = soldDateObj.strftime('%m-%d-%Y')
            proceeds = round(float(obj["amount"]) * float(obj["sellPrice"]), 2)
            cost = round(float(obj["amount"]) * float(obj["buyPrice"]), 2)
            profit = format(round(proceeds - cost, 2), '.2f')
            # Place paranthesis around negative profit values
            if float(profit) < 0:
                profit = abs(float(profit))
                profit = f'({profit})'
            # Generate GUIDs for cell Ids
            uuidList = [str(uuid4()) for x in range(9)]
            # Create row object and push to FormData collection
            row = {
                "clientId" : clientId,
                "form" : "8949",
                "buyWallet" : obj["buyWallet"],
                "sellWallet" : obj["sellWallet"],
                "mode" : obj["mode"],
                "rowId" : uuidList[0],
                "sectionId" : section[0]["sectionId"],
                "isActive" : True,
                "columns" : [
                    {
                        "columnId" : section[0]["tableConfig"][0]["columnId"],
                        "columnValue" : description,
                        "cellId" : uuidList[1]
                    },
                    {
                        "columnId" : section[0]["tableConfig"][1]["columnId"],
                        "columnValue" : dateAquired,
                        "cellId" : uuidList[2]               
                    },
                    {
                        "columnId" : section[0]["tableConfig"][2]["columnId"],
                        "columnValue" : dateSold,
                        "cellId" : uuidList[3]               
                    },
                    {
                        "columnId" : section[0]["tableConfig"][3]["columnId"],
                        "columnValue" : proceeds,
                        "cellId" : uuidList[4]               
                    },
                    {
                        "columnId" : section[0]["tableConfig"][4]["columnId"],
                        "columnValue" : cost,
                        "cellId" : uuidList[5]               
                    },
                    {
                        "columnId" : section[0]["tableConfig"][5]["columnId"],
                        "columnValue" : "",
                        "cellId" : uuidList[6]               
                    },
                    {
                        "columnId" : section[0]["tableConfig"][6]["columnId"],
                        "columnValue" : "",
                        "cellId" : uuidList[7]               
                    },
                    {
                        "columnId" : section[0]["tableConfig"][7]["columnId"],
                        "columnValue" : profit,
                        "cellId" : uuidList[8]               
                    }
                ],
            }
            dbSet.insertOneDB(dbSet.getFormData(), filter=row)
        
        except Exception as err:
            App_logger.error(err)

    def basisCalc(self, json_object, mode, clientId, year):
        #====LOAD JSON FILE END===== 

        # print(len(json_object))
        # print(json_object[0]["TxHash"])

        i = 0
        numpyArray = np.empty((0,10))

        fifoBuy = np.empty((0,11))
        fifoSell = np.empty((0,11))
        print(fifoBuy)
        print(fifoSell)


        while (i < len(json_object)):
            hashCurrent = json_object[i]["TxHash"] 
            txFromCurrent = json_object[i]["From"]
            txToCurrent = json_object[i]["To"]
            amountCurrent = json_object[i]["Amount"]
            confirmationCurrent = "NA"
            dateCurrent = timeRegulator(json_object[i]["TimeStamp"])
            priceCurrent = json_object[i]["Price"]
            serialNumber = i #array index
            txType = json_object[i]["TxDirection"]
            tokenCurrent = json_object[i]["Token"]
            txWallet = json_object[i]["Wallet"]
            token = tokenCurrent

            # numpyArray = np.append(numpyArray, [[hashCurrent, txFromCurrent, txToCurrent , amountCurrent, confirmationCurrent, dateCurrent, tokenCurrent, priceCurrent, serialNumber, txType]], axis = 0)
            # i = i+1

            
            if (txType == "OUT"):
                fifoSell = np.append(fifoSell, [[hashCurrent, txFromCurrent, txToCurrent , amountCurrent, confirmationCurrent, dateCurrent, tokenCurrent, priceCurrent, serialNumber, txType, txWallet]], axis = 0)

            else:
                fifoBuy = np.append(fifoBuy, [[hashCurrent, txFromCurrent, txToCurrent , amountCurrent, confirmationCurrent, dateCurrent, tokenCurrent, priceCurrent, serialNumber, txType, txWallet]], axis = 0)
                # print(len(fifoBuy))
                # if len(fifoBuy) > 0 :
                #     print(fifoBuy[i])

            i = i + 1


        pool = 0

        if mode == 'fifo':
            fifoSell = fifoSell[fifoSell[:,5].argsort()]
            fifoBuy = fifoBuy[fifoBuy[:,5].argsort()]
            print(fifoBuy.shape)
            #print(fifoBuy)
        elif mode == 'lifo':
            fifoSell = fifoSell[fifoSell[:,5].argsort()]
            fifoBuy = fifoBuy[fifoBuy[:,5].argsort()[::-1]]
        elif mode == 'hifo':
            fifoSell = fifoSell[fifoSell[:,3].argsort()]
            fifoBuy = fifoBuy[fifoBuy[:,3].argsort()]


        # print(fifoBuy.shape)
        # print(fifoSell.shape)

        #note x - June 24 2022
        #Why do they 
        # if(token == "AXS"):
        #     print(fifoBuy)
        #     print(fifoSell)
        #note x - END

        sellLength = fifoSell.shape[0]

        buyRemaining = 0
        sellRemaining = 0
        timeBuy = 0
        timeSell = 0
        totalTax = 0
        ltcg = 0
        stcg = 0
        coinPool = 0
        coinAmount = 0
        longShortValue = 1
        isFee = False
        isPrevFee = False
        i2 = 0
        i3 = 0 
        f = 2
        try:
            while (sellLength -1) >= (i2 and i3):
                print(i2, "Count of i2") # fifo index for Sell
                print(i3, "count of i3") # fifo index for buy
                # print(coinPool == 0)
                if (fifoSell[i2, 1] == "Mint" or fifoSell[i2, 1] == "Fees" or fifoSell[i2, 1] == "Royalties"):
                    isFee = True
                    QuantSell = fifoSell[i2,3]  #Removes first sell array and takes 3rd field (value)
                    QuantBuy = 0
                    sellPrice = fifoSell[i2,7]
                    buyPrice = 0
                    timeSell = fifoSell[i2, 5]
                    timeBuy = fifoSell[i2,5]
                    serialBuy = fifoSell[i2,8]
                    serialSell = fifoSell[i2,8]
                    token = fifoSell[i2, 6]
                    walletSell = fifoSell[i2, 10]
                    walletBuy = fifoSell[i2, 10]
                elif coinPool == 0:                   #If both bins are empty, need to refill
                    QuantSell = fifoSell[i2,3]  #Removes first sell array and takes 3rd field (value)
                    QuantBuy = fifoBuy[i3,3]   #Removes first buy array and takes 3rd field (value)
                    sellPrice = fifoSell[i2,7]
                    buyPrice = fifoBuy[i3,7]
                    timeBuy = fifoBuy[i3,5]
                    timeSell = fifoSell[i2,5]
                    serialBuy = fifoBuy[i3,8]
                    serialSell = fifoSell[i2,8]
                    token = fifoBuy[i3, 6]
                    walletSell = fifoSell[i2, 10]
                    walletBuy = fifoBuy[i3, 10]
                    print(sellPrice)
                    print(QuantSell)
                elif coinPool > 0:
                    #i2 = i2 + 1
                    QuantBuy = fifoBuy[i3,3]
                    buyPrice = fifoBuy[i3,7]
                    if isPrevFee:
                        QuantSell = fifoSell[i2,3]
                    else:
                        QuantSell = sellRemaining
                    timeBuy = fifoBuy[i3,5]
                    timeSell = fifoSell[i2,5]
                    serialBuy = fifoBuy[i3,8]
                    serialSell = fifoSell[i2,8]
                    token = fifoBuy[i3, 6]
                    walletSell = fifoSell[i2, 10]
                    walletBuy = fifoBuy[i3, 10]

                else:
                    #i3 = i3 + 1
                    QuantSell = fifoSell[i2,3]
                    sellPrice = fifoSell[i2,7]
                    QuantBuy = buyRemaining
                    timeBuy = fifoBuy[i3,5]
                    timeSell = fifoSell[i2,5]
                    serialBuy = fifoBuy[i3,8]
                    serialSell = fifoSell[i2,8]
                    token = fifoBuy[i3, 6]
                    walletSell = fifoSell[i2, 10]
                    walletBuy = fifoBuy[i3, 10]

                if float(QuantSell) > float(QuantBuy):
                    if isFee:
                        coinAmount = float(QuantSell)
                    else:
                        coinAmount = float(QuantBuy)
                else:
                    coinAmount = float(QuantSell)
                sellRemaining = 0
                buyRemaining = 0
                coinPool = float(QuantSell) - float(QuantBuy)
                #print("coin Pool:", coinPool)
                if coinPool > 0:
                    sellRemaining = coinPool
                    # sell Amount remaining Buy Coin at i3 is used
                    json_object[int(fifoBuy[i3,8])]['buyRemaining'] = 0
                    if isFee:
                        i2 = i2 + 1
                    else:
                        i3 = i3 + 1
                elif coinPool < 0:
                    buyRemaining = -coinPool
                    # Sell Qty used up, Buy amount remaining
                    # add BuyRemaining amount to JSON at index fifoBuy[i3,8] => JSON index
                    json_object[int(fifoBuy[i3,8])]['buyRemaining'] = -coinPool
                    i2 = i2 + 1
                else:
                    # CoinPool = 0 => Sell and buy amount used => BuyRemaining = 0 
                    json_object[int(fifoBuy[i3,8])]['buyRemaining'] = 0
                    i2 = i2 + 1
                    i3 = i3 + 1


                Profit = (float(coinAmount)*(float(sellPrice)-float(buyPrice)))
                if (token == "ETH"):
                    print("coin amount: ", coinAmount)
                    print("buyRemaining: ", buyRemaining)


                if isFee:
                    sellDays = int(timeConverter(timeSell))
                    buyDays = sellDays - 1
                    holdDuration = sellDays - buyDays
                else:
                    holdDuration = int(timeConverter(timeSell))-int(timeConverter(timeBuy))

                if (holdDuration) <= 365:
                    stcg = stcg + Profit
                    longShortValue = 1
                else:
                    ltcg = ltcg + Profit
                    longShortValue = 1

                # print(fifoSell(i2,2)) #figure out what  spaces looks like
                
                taxRequired = Profit*longShortValue
                totalTax = totalTax + taxRequired      

                f = f + 1
                if isFee:
                    isPrevFee = True
                    isFee = False
                    coinPool = 0
                else:
                    isPrevFee = False


                ##Call createFormRow() here
                if year ==  datetime.today().year - 1: #create row only for Current Tax Year
                    obj = {
                        "buyPrice" : buyPrice,
                        "sellPrice" : sellPrice,
                        "amount" : coinAmount,
                        "buyDate" : timeBuy,
                        "sellDate" : timeSell,
                        "holdDuration" : holdDuration,
                        "buyWallet" : walletBuy,
                        "sellWallet" : walletSell,
                        "mode" : mode,
                        "token" : token
                    }
                    self.createFormRow(clientId, obj)

        except Exception as err: 
            print("OHHHHHHHH YEAHHH TOTAL Tax FIFO", totalTax)
            traceback.print_exc()
            App_logger.error(err)

        print(totalTax, ltcg, stcg)
        return(totalTax, ltcg, stcg, json_object)

if __name__ == "__main__":
    taxCalculator = TaxCalculator()
    # taxCalculator.basisCalc(readClassificationJson('TaxCalculationInput.json'), 'fifo')
    taxCalculator.calculateTaxLiability("8a0b1981-bae1-48a9-8073-653ffa7f8f12", "fifo")
