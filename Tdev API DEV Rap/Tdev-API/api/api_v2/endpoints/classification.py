from fastapi import APIRouter, Query
from util import *
from loggerUtil import logger
from api.models.request import *
from api.models.response import *
from Domain.classificationMgmtService import classificationService as classifiServ
from Domain.clientMgmtService import clientService as clientServ

router = APIRouter()

@router.post("/retryFailedTransactions/{clientId}")
async def retryFailedTransactions(clientId: UUID):
	response = classifiServ.retryFailedTransactionTask(clientId)
	return response

@router.post("/start/{clientId}", response_model=StatusResponse)
async def commitClassification(clientId: UUID):
	try:
		msg_list = classifiServ.commitClassificationTask(clientId)
		if len(msg_list) > 0:
			return clientServ.getClientOverallStatus(clientId)
		else:
			return StatusResponse(status="empty", message="No new wallets to process. Please enter at least one new wallet")
	except Exception as e:
		logger.exception(e)
		return StatusResponse(status="Error occured", message="exception: {}.format(e)")

@router.delete("/unclassifiedTxs/{clientId}", response_model=StatusResponse)
def deleteUnclassifiedTxs(clientId : UUID, txId: str = Query(max_length=30)):
	try:
		output = classifiServ.deleteUnclassifiedTxsTask(clientId, txId)
		return output
	except Exception as e:
		logger.exception(e)

@router.put("/unclassifiedTxs/{clientId}", response_model=UnclassifiedTxPutResponse)
def updateUnclassifiedTxs(clientId: UUID, item: TransactionRequest):
	try:
		output = classifiServ.updateUnclassifiedTxsTask(clientId, item)
		return output
	except Exception as e:
		logger.exception(e)
	
@router.get("/taxSummary/{clientId}", response_model=TaxSummaryResponse)
def getTaxSummary(clientId: UUID):
	try:
		output = classifiServ.getTaxSummaryDetails(clientId)
		return output
	except Exception as e:
		logger.exception(e)

@router.get("/testTaxCalculation/{clientId}")
def testTaxCalculation(clientId: UUID):
	try:
		task = classifiServ.testTaxCalculationTask(clientId)
	except Exception as e:
		logger.exception(e)
    




