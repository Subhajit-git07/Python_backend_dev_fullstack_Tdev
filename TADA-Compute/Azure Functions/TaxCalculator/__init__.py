import json
import azure.functions as func

from Domain.TaxCalculatorService.TaxCalculator import TaxCalculator

from LoggerUtils import App_logger

def main(msg: func.QueueMessage) -> None:
    App_logger.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    """
    Parameters:
    "clientId", "mode"
    """ 
    msg_param = json.loads(msg.get_body())
    App_logger.info(msg_param)
    taxCalculator = TaxCalculator()
    taxCalculator.calculateTaxLiability(msg_param["clientId"], msg_param["mode"])