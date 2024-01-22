import json
import azure.functions as func

from Domain.CovalentServicefails.CovalentServicefails import CovalentServicefails

from LoggerUtils import App_logger

def main(msg: func.QueueMessage) -> None:
    App_logger.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8')) 
    """
    Parameters: "chainID", "chainName", "clientId", "wallet"
    """
    msg_param = json.loads(msg.get_body())
    CovFails = CovalentServicefails(msg_param)
    CovFails.Covalentfailoperations()

