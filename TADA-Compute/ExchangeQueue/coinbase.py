# Requires python-requests. Install with pip or easy-install
##  Install with pip: pip install requests
##  Install with easy-install: easy_install requests

import json, hmac, hashlib, time, requests, os
from requests.auth import AuthBase

# Before implementation, set environmental variables with the names API_KEY and API_SECRET
# API_KEY = 'tltX56juuirosEZZ'
# API_SECRET = 'Q74F4BcvOtyVmdzrXGrJLh5E7wumyn8s'

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        signature = hmac.new(bytes(self.secret_key, 'utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request

def callcoinbaseapi(api_key,api_secret):


    api_url = 'https://api.coinbase.com/v2/'
    auth = CoinbaseWalletAuth(api_key, api_secret)

    # # Get current user
    r = requests.get(api_url + 'user', auth=auth)
    # print(r.json())

    ID = r.json()['data']['id']
    print(ID)

    # print(api_url + "accounts/" + ID + '/transactions')

    txData = requests.get(api_url + "accounts/:" + ID + '/transactions', auth=auth)

    # print("TX DATA", txData.json())
    print(txData.json())
    return txData.json()
    # {u'data': {u'username': None, u'resource': u'user', u'name': u'User'...

    # # Send funds
    # tx = {
    #     'type': 'send',
    #     'to': 'user@example.com',
    #     'amount': '10.0',
    #     'currency': 'USD',
    # }
    # r = requests.post(api_url + 'accounts/primary/transactions', json=tx, auth=auth)
    # print r.json()
    # # {u'data': {u'status': u'pending', u'amount': {u'currency': u'BTC'...


API_KEY = 'tltX56juuirosEZZ'
API_SECRET = 'Q74F4BcvOtyVmdzrXGrJLh5E7wumyn8s'
callcoinbaseapi(API_KEY,API_SECRET)

