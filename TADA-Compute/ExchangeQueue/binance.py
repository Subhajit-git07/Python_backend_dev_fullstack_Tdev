import urllib.parse
import hashlib
import hmac
import base64
import requests
import time

api_url = "https://api.binance.us"
# get binanceus signature
def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

# Attaches auth headers and returns results of a POST request
def binanceus_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    params={
        **data,
        "signature": signature,
        }
    req = requests.get((api_url + uri_path), params=params, headers=headers)
    print("REQQQQQQQQQQQQQQ")
    return req.json()




# Calling Mytrades API when we have some data in here 

def callbinanceapi(api_key,secret_key,symbol):
    api_url = "https://api.binance.us"
    finallistofdicts = []
    print(symbol)
    uri_path = "/api/v3/myTrades"
    data = {
            "timestamp": int(round(time.time() * 1000)),
            "symbol": symbol,
            # "startTime" :'1641353200',
            # "endTime" :'1672716400',
            "limit" : '1000'
        }

        
    result = binanceus_request(uri_path, data, api_key, secret_key)
    print(result)
        
        # for element in result:
        #     tempdict = {}
        #     tempdict['symbol'] = element['symbol']
        #     tempdict['id'] = element['id']
        #     tempdict['qty'] = element['qty']
        #     tempdict['price'] = element['price']
        #     if element['isBuyer'] == True:
        #         tempdict['TypeOfTransaction'] = 'Buy'
        #     else:
        #         tempdict['TypeOfTransaction'] = 'Sell'

        #     finallistofdicts.append(tempdict)
    
    return result




def getsymbols():
    listofsymbols = []
    resp = requests.get('https://api.binance.us/api/v3/exchangeInfo')
    print(resp.json())
    result = resp.json()["symbols"]
    for i in result:
        listofsymbols.append(i['symbol'])
    return listofsymbols

def getaccountassets(api_key, secret_key):
    headers = {}
    
    data = {
        "timestamp": int(round(time.time() * 1000)),
    }
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, secret_key)
    params={
        **data,
        "signature": signature,
        }
    uri_path = "/api/v3/account"
    req = requests.get((api_url + uri_path), params=params, headers=headers)
    return req.json()








api_key='bnx4XvW4uFfMYdBewiH85asjIJFsucyLXehvj4LDa8HF5naMtFw4QmxtNs3vWDJb'
secret_key='H1KIjagoN44GywI71tE8E0SayZ967x66xzrIQPst3OvC7DoRTCCf8wmvXNebmQW7'

get_account_result = getaccountassets(api_key, secret_key)

assets = get_account_result['balances']
assetlist = []
for i in assets:
    if float(i['free']) > 0 or float(i['locked'])>0:
        assetlist.append(i['asset'])
print(assetlist)




listofsymbols = getsymbols()
print(listofsymbols)
res = []
for j in assetlist:
    res = [i for i in listofsymbols if j in i]
print(res)
for symbol in res:
    callbinanceapi(api_key,secret_key,symbol)
   



















# if __name__=="__main__":

#     api_url = "https://api.binance.us"
#     api_key='bnx4XvW4uFfMYdBewiH85asjIJFsucyLXehvj4LDa8HF5naMtFw4QmxtNs3vWDJb'
#     secret_key='H1KIjagoN44GywI71tE8E0SayZ967x66xzrIQPst3OvC7DoRTCCf8wmvXNebmQW7'

#     #calling orders api to get symbols first
#     uri_path = "/api/v3/openOrders"
#     data = {
#         "timestamp": int(round(time.time() * 1000))
#     }

#     result = binanceus_request(uri_path, data, api_key, secret_key)
#     print("GET {}: {}".format(uri_path, result))

#     finallistofdicts = []




#     if len(result) == 0 :
#         print('No Data for the Client')

#     elif (len(result)>0):
#         #calling mytrade api
#         listofmytrades = []
#         symbollist = []
#         uri_path = "/api/v3/myTrades"
#         for i in result:
#             symbollist.append(i['symbol'])
#         finalsymbols = set(symbollist)
#         print(finalsymbols)

#         for symbol in finalsymbols:
#             data = {
#                 "timestamp": int(round(time.time() * 1000)),
#                 "symbol": symbol
#             }
            
#             result = binanceus_request(uri_path, data, api_key, secret_key)
            
#             for element in result:
#                 tempdict = {}
#                 tempdict['symbol'] = element['symbol']
#                 tempdict['id'] = element['id']
#                 tempdict['qty'] = element['qty']
#                 tempdict['price'] = element['price']
#                 if element['isBuyer'] == True:
#                     tempdict['TypeOfTransaction'] = 'Buy'
#                 else:
#                     tempdict['TypeOfTransaction'] = 'Sell'

#                 finallistofdicts.append(tempdict)



#     else:
#         print('none')

#     print(finallistofdicts)












