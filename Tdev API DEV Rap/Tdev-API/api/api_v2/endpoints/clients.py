from fastapi import status, APIRouter
from fastapi import Depends
from JwtAuthentication import has_access
from util import *
from loggerUtil import logger
from api.models.request import *
from api.models.response import *
from typing import List
from Domain.clientMgmtService import clientService 

router = APIRouter()

@router.put("/lock/{clientId}", response_model=StatusResponse)
async def lockClient(clientId: UUID):
	try:
		status = clientService.clientLock(clientId)
		return status
	except Exception as e:
		logger.exception(e)

@router.get("/status/{clientId}", response_model=StatusResponse)
async def getClientStatus(clientId: UUID):
		clientStatus = clientService.getClientOverallStatus(clientId)
		return clientStatus
	# except Exception as e:
	# 	logger.exception(e)

# Returns all users that have access to the given client
@router.get("/users/{clientId}", response_model=ClientUserListResponse)
async def getUsersForClient(clientId: UUID):
	try:
		userList = clientService.collectUsersForClient(clientId)
		return userList
	except Exception as e:
		logger.exception(e)

# Shares a client with the given users
@router.post("/addAccess/{clientId}", response_model= AddAccessListResponse)
async def addAccess(clientId: UUID, users: UserAccessListRequest):
	try:
		accessResponse = clientService.addAccessToUsers(clientId, users)
		return accessResponse
	except Exception as e:
		logger.exception(e)

# Removes a user from client access
@router.delete("/removeAccess/{clientId}", response_model=StatusResponse)
async def removeAccess(clientId: UUID, emailId: UserRemoveAccessRequest):
	try:
		status = clientService.removeAccessFromClient(clientId, emailId)
		return status
	except Exception as e:
		logger.exception(e)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientResponse)
async def createClient(item: ClientRequest, emailId:str=Depends(has_access)):
	status = clientService.createClientLogic(emailId, item)
	return status

@router.get("/{clientId}", response_model=ClientResponse)
async def getClient(clientId: UUID):
	# try:
	clientObj = clientService.clientDetails(clientId)
	return clientObj
	# except Exception as e:
	# 	logger.exception(e)
    
@router.put("/{clientId}", response_model=ClientResponse)
async def updateClient(clientId: UUID, item: ClientRequest):
	try:
		status = clientService.updateClientDetails(clientId, item)
		return status
	except Exception as e:
		logger.exception(e)

@router.delete("/{clientId}", response_model=StatusResponse)
async def deleteClient(clientId: UUID):
	try:
		status = clientService.deleteClientDetails(clientId)
		return status
	except Exception as e:
		logger.exception(e)

@router.get("/countries/", response_model=List[str])
async def getCountries():
	try:
		countries = clientService.getAllCountries()
		return countries
	except Exception as e:
		logger.exception(e)

@router.get("/cities/{country}", response_model=List[str])
async def getCitiesByCountry(country: str):
	try:
		stateList = clientService.collectCitiesByCountry(country)
		return stateList
	except Exception as e:
		logger.exception(e)
