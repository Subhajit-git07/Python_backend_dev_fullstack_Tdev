# import time
# import os
# import requests
# import urllib.parse
# import hashlib
# import hmac
# import base64

# # with open("keys", "r") as f:
# #     lines = f.read().splitlines()
# #     api_key = 'CSe5pV/wcsDGvfyLb9KWgrtue1lz8H0whpjZNip5+3o6lLP/j7coJ6xk'
# #     api_sec = 'DU85okL3cwLasO1kIi/OOkDGvHZhg8jwOAldypyZE9UpPQmz36AZvjc0lS4yikD6+DHbgzJWE8tXgbxQ78Hgfg=='
# #     print(api_key)
# #     print(api_sec)


# # api_key = 'CSe5pV/wcsDGvfyLb9KWgrtue1lz8H0whpjZNip5+3o6lLP/j7coJ6xk'
# # api_sec = 'DU85okL3cwLasO1kIi/OOkDGvHZhg8jwOAldypyZE9UpPQmz36AZvjc0lS4yikD6+DHbgzJWE8tXgbxQ78Hgfg=='


# api_url = "https://api.kraken.com"

# def get_kraken_signature(urlpath, data, secret):
#     postdata = urllib.parse.urlencode(data)
#     encoded = (str(data['nonce']) + postdata).encode()
#     message = urlpath.encode() + hashlib.sha256(encoded).digest()

#     mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
#     sigdigest = base64.b64encode(mac.digest())
#     return sigdigest.decode()

# def kraken_request(url_path, data, api_key, api_sec):
#     headers = {"API-Key": api_key, "API-sign": get_kraken_signature(url_path, data, api_sec)}
#     resp = requests.post((api_url + url_path), headers=headers,data=data)
#     return resp


# def getHistory(api_key, api_sec):
#     resp = kraken_request("/0/private/TradesHistory", {
#         "nonce": str(int(1000 * time.time())),
#         "trades":   True,
#     }, api_key, api_sec)
#     print(resp.json())
#     return resp.json()





# def callkrakenapi(api_key,api_secret):
#     trade = getHistory(api_key,api_secret)['result']['trades']
#     # print(trade)
#     return trade














import time
import os
import requests
import urllib.parse
import hashlib
import hmac
import base64




# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"


# Attaches auth headers and returns results of a POST request
def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

# Construct the request and print the result




def callkrakenapi(api_key,api_secret):
    # api_key = 'PYbeAMkzJd1RNa6xywm5t51PdQspp3UlhP22OhgGxpkOvO1qWJ6LAaqW'
    # api_sec = '2UG3l+naRSO/QgsQN8glTr8Nky1ESzgktFtSY6CZhub6+jsOkA78uLGVAPNJgVtWgXUi2oAXdmJQwI20rSflGw=='
    resp = kraken_request('/0/private/Ledgers', {
    "nonce": str(int(1000*time.time()))
    # "asset": "GBP",
    # "start": 1610124514
    }, api_key, api_secret)

    print(resp.json())

#     print(resp.json())    

