from fastapi import APIRouter, Query
from util import *
from loggerUtil import logger
from api.models.request import *
from api.models.response import *
from Domain.transactionsMgmtService import transactionService as transServ
router = APIRouter()

@router.post("/manualupload/{clientId}",response_model=ManualPostTxsResponse)
async def manualupload(clientId: UUID, bulkinfo: ManualUploadsRequest):
	response = transServ.manualuploadFunc(clientId, bulkinfo)
	return response
	
@router.delete("/transactionManual/delete/{clientId}", response_model=StatusResponse)
def deletetransactionManual(clientId : UUID, txId: str = Query(max_length=30)):
	txOut = transServ.deletetransactionManualFunc(clientId, txId)
	return txOut

@router.delete("/transactionManual/bulkdelete/{clientId}", response_model=StatusResponse)
def deletebulktransactionManual(clientId : UUID, wallets: list, txId: list):
	txOut = transServ.deletebulktransactionManualFunc(clientId, wallets, txId)
	return txOut

@router.get("/transactionManual/{clientId}", response_model=ManualGetTxsResponse)
def getTransactionManual(clientId: UUID):
	finallist = transServ.getTransactionManualFunc(clientId)
	return finallist
	
@router.get("/transactionReferenceHash/{clientId}", response_model=PagedTransactionsByHashResponse)
def getTransactionReferenceHash(clientId: UUID, start_index: int = Query(ge=0, le=10**8), size: int = Query(ge=0, le=10**8), transactionCount: int = Query(ge=0, le=10**8)):
	try:
		return_obj = transServ.getTransactionReferenceHashDetails(clientId, start_index, size, transactionCount)
		return return_obj
	except Exception as e:
		logger.exception(e)
    
@router.get("/transactionbyHash/{clientId}", response_model=PagedTransactionsForKeyResponse)
def getTransactionByHash(clientId: UUID, TxHash: str, start_index: int = Query(ge=0, le=10**8), size: int = Query(ge=0, le=10**8)):
	try:
		return_obj = transServ.getTransactionByHashDetails(clientId, TxHash, start_index, size)
		return return_obj
	except Exception as e:
		logger.exception(e)

@router.get("/transactionReferenceAsset/{clientId}", response_model=PagedTransactionsByAssetResponse)
def getTransactionReferenceAsset(clientId: UUID, start_index: int = Query(ge=0, le=10**8), size: int = Query(ge=0, le=10**8), transactionCount: int = Query(ge=0, le=10**8)):
	try:
		return_obj = transServ.getTransactionReferenceAssetDetails(clientId, start_index, size, transactionCount)
		return return_obj
	except Exception as e:
		logger.exception(e)

@router.get("/transactionbyAsset/{clientId}", response_model=PagedTransactionsForKeyResponse)
def getTransactionByAsset(clientId: UUID, Asset: str, start_index: int = Query(ge=0, le=10**8), size: int = Query(ge=0, le=10**8)):
	try:
		return_obj = transServ.getTransactionByAssetDetails(clientId, Asset, start_index, size)
		return return_obj
	except Exception as e:
		logger.exception(e)