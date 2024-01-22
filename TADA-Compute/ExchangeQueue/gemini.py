import requests
import json
import base64
import hmac
import hashlib
import datetime, time


def getsymbols():
    import requests, json

    base_url = "https://api.gemini.com/v1"
    response = requests.get(base_url + "/symbols")
    symbols = response.json()

    return symbols



def getorderhistory(gemini_api_key ,gemini_api_secret,symbol):
    base_url = "https://api.gemini.com"
    endpoint = "/v1/mytrades"
    url = base_url + endpoint



    t = datetime.datetime.now()
    payload_nonce = time.time()

    # payload = {
    #     "nonce": payload_nonce,
    #     "request": "/v1/orders",
    # }
    payload = {
    "nonce": payload_nonce,
    "request": "/v1/mytrades",
    "symbol": symbol
}
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    request_headers = { 'Content-Type': "text/plain",
                        'Content-Length': "0",
                        'X-GEMINI-APIKEY': gemini_api_key,
                        'X-GEMINI-PAYLOAD': b64,
                        'X-GEMINI-SIGNATURE': signature,
                        'Cache-Control': "no-cache" }

    response = requests.post(url,
                            data=None,
                            headers=request_headers)
    
    orderhistory = response.json()
    # print(orderhistory)
    return orderhistory


def callgemniapi(api_key,api_secret):
    # gemini_api_key = "account-7UmM2q3PWGjB8QAvSa9r"
    # gemini_api_secret = "2S676cjhTH8TZxNPEm64oz7pq1N4".encode()
    listofsymbols=getsymbols()
    api_secret = api_secret.encode()
    finallistofdicts = []
    print(listofsymbols)
    for symbol in listofsymbols:
        print(symbol)
        result=getorderhistory(api_key,api_secret,symbol)
        # print(result)
        
        if len(result) == 0:
            print("No transactions in the accoount")
        else:
            for i in result:
                #creating temp dict for all transaction trades
                tempdict = {}
                tempdict['exchange'] = 'gemini'
                tempdict['id'] = i['order_id']
                tempdict['symbol'] = i['symbol']
                if i['type'] is 'sell':
                    tempdict['direction'] = 'out'
                else:
                    tempdict['direction'] = 'in'
                tempdict['timestamp']  = i['timestamp']
                tempdict['price'] = i['price']
                tempdict['amount'] = i['amount']
                tempdict['fees'] = i['fee_amount']


                finallistofdicts.append(tempdict)
        
    # print(finallistofdicts)
    return finallistofdicts

if __name__ == "__main__":
    1
    # gemini_api_key = "account-7UmM2q3PWGjB8QAvSa9r"
    # gemini_api_secret = "2S676cjhTH8TZxNPEm64oz7pq1N4"
    

    # result=callgemniapi(gemini_api_key,gemini_api_secret)
    # print(result)
    # finallistofdicts = []
    # if len(result) == 0:
    #     print("No transactions in the accoount")
    # else:
    #     for i in result:
    #         print(i)
    #         tempdict = {}
    #         tempdict['id'] = i['id']
    #         tempdict['symbol'] = i['symbol']
    #         tempdict['type'] = i['slide']
    #         tempdict['timestamp']  = i['timestamp']
    #         tempdict['price'] = i['price']
    #         tempdict['amount'] = i['original_amount']
    #         finallistofdicts.append(tempdict)
    



    


# data = [   {
#     "order_id": "107421210",
#     "id": "107421210",
#     "symbol": "ethusd",
#     "exchange": "gemini",
#     "avg_execution_price": "0.00",
#     "side": "sell",
#     "type": "exchange limit",
#     "timestamp": "1547241628",
#     "timestampms": 1547241628042,
#     "is_live": True,
#     "is_cancelled": False,
#     "is_hidden": False,
#     "was_forced": False,
#     "executed_amount": "0",
#     "remaining_amount": "1",
#     "options": [],
#     "price": "125.51",
#     "original_amount": "1"
#   },
#   {
#     "order_id": "107421205",
#     "id": "107421205",
#     "symbol": "ethusd",
#     "exchange": "gemini",
#     "avg_execution_price": "125.41",
#     "side": "buy",
#     "type": "exchange limit",
#     "timestamp": "1547241626",
#     "timestampms": 1547241626991,
#     "is_live": True,
#     "is_cancelled": False,
#     "is_hidden": False,
#     "was_forced": False,
#     "executed_amount": "0.029147",
#     "remaining_amount": "0.970853",
#     "options": [],
#     "price": "125.42",
#     "original_amount": "1"
#   } ]



# for i in data:
#     print(i['order_id'])