from webbrowser import get
import requests
import time
import base64
import hashlib
import hmac

url = 'https://api.kucoin.com'



#account info / authentication 

def accountinfo(api_key,api_secret,api_passphrase):
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/orders'
    signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    url = 'https://api.kucoin.com/api/v1/orders'
    #url = 'https://openapi-sandbox.kucoin.com/api/v1/accounts'

    response = requests.request('get', url, headers=headers)
    print(response.status_code)
    return response.json()



#api call and getting the history

def callkucoinAPI(api_key,api_secret,api_passphrase):
    
    # api_key = '636d4f4d2316ea00013052a6'
    # api_secret = 'f5722d27-b0d1-46ce-baca-aa7903850169'
    # api_passphrase ='Winter@2023!'
    
    #list of dictionaries we would be returning 
    finallistofdictionary = []


    items = accountinfo(api_key,api_secret,api_passphrase)
    # ['data']['items']
    print(items)
    #item returns json with item = {..,data{,,.{items{trades we need}}}}
    # result=items['data']['items']
    # print(result)
    # if len(result) == 0:
    #     #if no trades i.e. length of result = 0 then return empty
    #     print('Account does not have any transactions')
    #     return finallistofdictionary
    # else:
    #     for i in result:
    #         print(i)
    #         #making temporary dictionary for each iteration of transaction 
    #         tempdict = {}
    #         tempdict['exchange'] =  'kucoin'
    #         tempdict['id'] = i['id']
    #         tempdict['symbol'] = i['symbol']
    #         if i['side'] is 'sell':
    #             tempdict['direction'] = 'out'
    #         else:
    #             tempdict['direction'] = 'in'

    #         tempdict['timestamp'] = i['createdAt']
    #         tempdict['price'] = i['price']
    #         tempdict['amount'] = i['dealSize']
    #         tempdict['quantity'] = i['size']
    #         finallistofdictionary.append(tempdict)
    
    
    # return finallistofdictionary
    # # print(accountinfo(api_key,api_secret,api_passphrase)['data']['items'])
    
    
if __name__ == "__main__":


    kucoin_api_key = '636d4f4d2316ea00013052a6'
    kucoin_api_secret = 'f5722d27-b0d1-46ce-baca-aa7903850169'
    kucoin_api_passphrase ='Winter@2023!'

    # kraken_api_key = 'PYbeAMkzJd1RNa6xywm5t51PdQspp3UlhP22OhgGxpkOvO1qWJ6LAaqW'
    # kraken_api_sec = '2UG3l+naRSO/QgsQN8glTr8Nky1ESzgktFtSY6CZhub6+jsOkA78uLGVAPNJgVtWgXUi2oAXdmJQwI20rSflGw=='

    print(callkucoinAPI(kucoin_api_key,kucoin_api_secret,kucoin_api_passphrase))