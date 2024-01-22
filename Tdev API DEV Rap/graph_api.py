
# Define imports
import msal
import requests

# Enter the details of your AAD app registration
client_id = '8f0c13d7-94a5-48dc-be09-5f1952794af7'
client_secret = 'cQ78Q~PqUP~RRo303tZIG53WXoUIFyzsErKGEcek'
authority = 'https://login.microsoftonline.com/adb53b4f-b05f-4dcb-a2e1-9111380568c3'
scope = ['https://graph.microsoft.com/.default']

# Create an MSAL instance providing the client_id, authority and client_credential parameters
client = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)

# First, try to lookup an access token in cache
token_result = client.acquire_token_silent(scope, account=None)

# If the token is available in cache, save it to a variable
if token_result:
  access_token = 'Bearer ' + token_result['access_token']
  print('Access token was loaded from cache')

# If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
if not token_result:
  token_result = client.acquire_token_for_client(scopes=scope)
  access_token = 'Bearer ' + token_result['access_token']
  print('New access token was acquired from Azure AD')

print(access_token)

url = 'https://graph.microsoft.com/v1.0/groups'
headers = {
  'Authorization': access_token
}

# Make a GET request to the provided url, passing the access token in a header
graph_result = requests.get(url=url, headers=headers)

# Print the results in a JSON format
print(graph_result.json())