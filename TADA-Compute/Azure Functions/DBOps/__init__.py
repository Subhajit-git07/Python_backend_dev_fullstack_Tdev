import json
import azure.functions as func
from Domain.DBOpsService.operations import DBOperater

from LoggerUtils import App_logger

def main(msg: func.QueueMessage) -> None:
    App_logger.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    msg_param = json.loads(msg.get_body())
    App_logger.info(msg_param)
    operator = DBOperater(msg_param)
    operator.completeOperation()