from fastapi import status, APIRouter
from api.models.response import *
from api.models.request import *
from loggerUtil import logger
from Domain.exchangesMgmtService import exchangeService

router = APIRouter()

@router.post("/exchange/{clientId}", status_code=status.HTTP_201_CREATED, response_model=ExchangeResponse)
async def addExchange(clientId: UUID, item: ExchangeInRequest):
	try:
		exchangeOutObj = exchangeService.addExchangeTask(clientId, item)
		return exchangeOutObj
	except Exception as e:
		logger.exception(e)

@router.get('/exchange/{clientId}', response_model=ExchangesResponse)
async def getExchanges(clientId: UUID):
	try:
		exchangesDetails = exchangeService.getExchangesDetails(clientId)
		return exchangesDetails
	except Exception as e:
		logger.exception(e)

@router.delete('/exchange/{clientId}')
async def deleteExchange(clientId: UUID, exchangeId: str):
	try:
		msg = exchangeService.deleteExchangeTask(clientId, exchangeId)
		return msg
	except Exception as e:
		logger.exception(e)

@router.get("/names/")
async def getExchangesNames():
	try:
		exchanges = exchangeService.getAllExchangesNames()
		return exchanges
	except Exception as e:
		logger.exception(e)


