
class model_settting:
    fromKeyWords = ["from", "send", "sell", "make", "own", "src"]
    toKeyWords = ["^to", "^receive", "^buy", "^take", "^spend", "^dst", "^recipient"]
    quantKeyWords = ["value", "amount", "price", "total", "wad", "quant"]
    NFTKeyWords = ["token", "id"]
    swapTokens = ["^uni"]
    chainParam = {
        1 : {
            "AssertPlatform": "ethereum",
            "Decimal": 18,
            "Symbol": "ETH",
            "AutoClassify": ["^transfer", "^ordersmatched"], # Regex
            "IgnoreSigns": ["^approval", "^swap", "^fill"] # Regex
        },
        43114: {
            "AssertPlatform": "avalanche",
            "Decimal": 18,
            "Symbol": "AVAX",
            "AutoClassify": ["^transfer"], # Regex
            "IgnoreSigns": ["^approval", "^swap", "^fill"] # Regex
        },
        2020: {
            "AssertPlatform" : "ronin",
            "Decimal" : 18,
            "Symbol" : "RON",
            "AutoClassify": ["^transfer"], # Regex
            "IgnoreSigns": ["^approval", "^swap", "^fill"] # Regex
        }
    }

class util:
    
    @staticmethod
    def CloseValues(x, y, threshold = 0.001):
        x = abs(x)
        y = abs(y)
        delta = abs(y - x)
        den = max(x, y)
        if y != 0:
            delta = delta/den
        if delta < threshold:
            return True
        else:
            return False
            
    @staticmethod
    def GetValueList(obj):
        value_list = []
        if type(obj) == list:
            for x in obj:
                value_list.append(x["value"])
        else:
            value_list.append(obj)
        return value_list
