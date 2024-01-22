import json
import azure.functions as func

from Domain.BCExtractorServicefails.BCExtractorfails import BCExtFails

from LoggerUtils import App_logger

def main(msg: func.QueueMessage) -> None:
    App_logger.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    """
    Parameters: chainName, wallet, clientID, container, blob
    """
    msg_param = json.loads(msg.get_body())
    bcfails = BCExtFails(msg_param)
    bcfails.BCfailoperations()
