from fastapi import status, APIRouter
from util import *
from loggerUtil import logger
from api.models.response import *
from api.models.request import *
from Domain.walletsMgmtService import walletService

router = APIRouter()

@router.get("/blockchains/", response_model=List[str])
async def getBlockchains():
	try:
		chains = walletService.getBlockchainsFunc()
		return chains
	except Exception as e:
		logger.exception(e)

@router.get("/{clientId}", response_model=WalletsResponse)
async def getWallets(clientId: UUID):
	try:
		wallets = walletService.getAllWallets(clientId)
		return wallets
	except Exception as e:
		logger.exception(e)

@router.post("/{clientId}", status_code=status.HTTP_201_CREATED, response_model=WalletsResponse)
async def addWallet(clientId: UUID, walletInfo: WalletsRequest):
	try:
		walletsResArr = walletService.addWalletDetails(clientId, walletInfo)
		return walletsResArr
	except Exception as e:
		logger.exception(e)

@router.delete("/{clientId}", response_model=StatusResponse)
async def deleteWallet(clientId: UUID, item: WalletRequest):
	try:
		response = walletService.deleteWalletDetails(clientId, item)
		return response
	except Exception as e:
		logger.exception(e)
