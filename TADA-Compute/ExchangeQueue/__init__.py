import logging
import json
import logging
import azure.functions as func
from ExchangeQueue.ExchangesApi import * 




def main(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    """
    Parameters:
    "name", "clientid","apikey","api_Secret"
    """ 
    msg_param = json.loads(msg.get_body())
    logging.info(msg_param)
    #making the exchange name to lower
    name = msg_param["name"].lower()
    print(MasterExchangesAPI(name,msg_param["api_key"],msg_param["api_secret"],msg_param["api_passphrase"]))




# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )






