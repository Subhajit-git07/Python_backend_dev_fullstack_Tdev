from fastapi import APIRouter
from fastapi import Depends
from JwtAuthentication import has_access
from api.models.request import *
from api.models.response import *
from util import *
from loggerUtil import logger
from Domain.profileSummaryMgmtService import profileSummaryService as pSummaryServ

router = APIRouter()
@router.get("/clientNames", response_model=ClientInfoListResponse)
async def getClientNames(emailId:str=Depends(has_access)):
	clientNames = list(pSummaryServ.getAllClientNames(emailId))
	return clientNames

@router.get("/taxValues/{clientId}", response_model=TaxValuesResponse)
async def getTaxValues(clientId: UUID):
	try:
		taxValues = pSummaryServ.getTaxValuesDetails(clientId)
		return taxValues
	except Exception as e:
		logger.exception(e)

@router.get("/holdings/{clientId}", response_model=HoldingsResponse)
def getHoldings(clientId: UUID):
	try:
		holdings = pSummaryServ.getHoldingsDetails(clientId)
		return holdings
	except Exception as e:
		logger.exception(e)

@router.get("/userPreferences/{clientId}", response_model=UserPreferencesResponse)
def getUserPreferences(clientId: UUID):
	try:
		userPreferences = pSummaryServ.getUserPreferencesDetails(clientId)
		return userPreferences
	except Exception as e:
		logger.exception(e)

@router.post("/userPreferences/{clientId}", response_model=UserPreferencesResponse)
def setUserPreferences(clientId: UUID, userPreferences: UserPreferencesRequest):
	try:
		user_Preferences = pSummaryServ.setUserPreferencesDetails(clientId, userPreferences)
		return user_Preferences
	except Exception as e:
		logger.exception(e)
