from ExchangeQueue.binance import *
from ExchangeQueue.coinbase import *
from ExchangeQueue.gemini import *
from ExchangeQueue.kraken import * 
from ExchangeQueue.kucoin import *

#master function returns output from exchanges as a list of dictionaries where a dictionary is a representation of one transaction 
def MasterExchangesAPI(exchangetype,apikey,apisecret,apipassphrase):
    if exchangetype is 'binance':
        return callbinanceapi(apikey,apisecret)
    elif exchangetype is 'coinbase':
        return callcoinbaseapi(api_key=apikey,api_secret=apisecret)
    elif exchangetype is 'gemini':
        return callgemniapi(api_key=apikey,api_secret=apisecret)
    elif exchangetype is 'kraken':
        return callkrakenapi(api_key=apikey,api_secret=apisecret)
    elif exchangetype is 'kucoin':
        return callkucoinAPI(apikey,apisecret,apipassphrase)
    else:
        return 'The Exchange you entered is not supported as of now'



   
if __name__ == "__main__":
    # Binance_api_key='bnx4XvW4uFfMYdBewiH85asjIJFsucyLXehvj4LDa8HF5naMtFw4QmxtNs3vWDJb'
    # Binance_secret_key='H1KIjagoN44GywI71tE8E0SayZ967x66xzrIQPst3OvC7DoRTCCf8wmvXNebmQW7'

    # gemniapi_key = "account-7UmM2q3PWGjB8QAvSa9r"
    # gemniapi_secret = "2S676cjhTH8TZxNPEm64oz7pq1N4"

    # Coinbase_API_KEY = 'tltX56juuirosEZZ'
    # Coinbase_API_SECRET = 'Q74F4BcvOtyVmdzrXGrJLh5E7wumyn8s'

    kucoin_api_key = '636d4f4d2316ea00013052a6'
    kucoin_api_secret = 'f5722d27-b0d1-46ce-baca-aa7903850169'
    kucoin_api_passphrase ='Winter@2023!'

    # kraken_api_key = 'PYbeAMkzJd1RNa6xywm5t51PdQspp3UlhP22OhgGxpkOvO1qWJ6LAaqW'
    # kraken_api_sec = '2UG3l+naRSO/QgsQN8glTr8Nky1ESzgktFtSY6CZhub6+jsOkA78uLGVAPNJgVtWgXUi2oAXdmJQwI20rSflGw=='

    print(MasterExchangesAPI("kucoin",kucoin_api_key,kucoin_api_secret,kucoin_api_passphrase))
    # extractor.ExportWalletToCSV("0x71CF4Af25Def08C74A9eed3460EEd3bE36ac9Cff")
