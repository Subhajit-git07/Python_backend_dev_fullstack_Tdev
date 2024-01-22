import json
import azure.functions as func

from Domain.CovalentService.APIDataExtractor import CovalentTransactionExtractor

from LoggerUtils import App_logger

def main(msg: func.QueueMessage) -> None:
    App_logger.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    """
    Parameters:
    "chainID", "chainName", "clientId", "wallet", "pageSize" (optional)
    """
    msg_param = json.loads(msg.get_body())
    chain_id = msg_param["chainID"]
    chain_name = msg_param["chainName"]
    client_id = msg_param["clientId"]
    wallet = msg_param["wallet"]
    App_logger.info(msg_param)
    if "pageSize" in msg_param.keys():
        extractor = CovalentTransactionExtractor(chain_id, chain_name, client_id, int(msg_param["pageSize"]))
    else:
        extractor = CovalentTransactionExtractor(chain_id, chain_name, client_id)
    extractor.StartExtraction(wallet=wallet)