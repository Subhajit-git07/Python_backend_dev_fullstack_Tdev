import json
import azure.functions as func

from Domain.PriceMgmtService.coinGeckoDataExtractorApp import pricingDataManagement

from LoggerUtils import App_logger

def main(msg:func.QueueMessage) -> None:
	App_logger.info('Python queue trigger function processed a queue item: %s',
				 msg.get_body().decode('utf-8'))
	"""
	msg_param: "database", "collection", "blob", "AssertPlatform", "Token", "Address", "TimeStamp-Max", "TimeStamp-Min"
	"""
	msg_param = json.loads(msg.get_body())
	pricing = pricingDataManagement(msg_param)
	pricing.ExportDataToDB()
	pricing.UpdateStatus()