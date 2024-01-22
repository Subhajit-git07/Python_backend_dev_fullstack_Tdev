
# Define imports and config dictionary
import msal
import requests

config = {
  'client_id': '8f0c13d7-94a5-48dc-be09-5f1952794af7',
  'client_secret': 'cQ78Q~PqUP~RRo303tZIG53WXoUIFyzsErKGEcek',
  'authority': 'https://login.microsoftonline.com/adb53b4f-b05f-4dcb-a2e1-9111380568c3',
  'scope': ['https://graph.microsoft.com/.default'] 
}

# Define a function that takes parameter 'url' and executes a graph call.
# Optional parameter 'pagination' can be set to False to return only first page of graph results
def make_graph_call(url, pagination=True):
	# Firstly, try to lookup an access token in cache
	token_result = client.acquire_token_silent(config['scope'], account=None)

	# Log that token was loaded from the cache
	if token_result:
		print('Access token was loaded from cache.')

	# If token not available in cache, acquire a new one from Azure AD
	if not token_result:
		token_result = client.acquire_token_for_client(scopes=config['scope'])
		print('New access token aquired from AAD')
		print("=======token_result===========")
		print(token_result)

	# If token available, execute Graph query
	if 'access_token' in token_result:
		headers = {'Authorization': 'Bearer ' + token_result['access_token']}
		graph_results = []

		while url:
			try:
				graph_result = requests.get(url=url, headers=headers).json()
				graph_results.extend(graph_result['value'])
				if (pagination == True):
				  url = graph_result['@odata.nextLink']
				else:
				  url = None
			except Exception as e:
				print(e)
				break
	else:
		print(token_result.get('error'))
		print(token_result.get('error_description'))
		print(token_result.get('correlation'))

	print(graph_results)
	return graph_results

# Create an MSAL instance providing the client_id, authority and client_credential parameters
client = msal.ConfidentialClientApplication(config['client_id'], authority=config['authority'], client_credential=config['client_secret'])

# Make an MS Graph call
url = 'https://graph.microsoft.com/v1.0/groups'
make_graph_call(url, pagination=False)
