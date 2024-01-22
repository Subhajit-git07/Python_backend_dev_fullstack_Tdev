from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
from Domain.clientMgmtService import clientService
from util import *
from loggerUtil import logger
from Infrastructure.dbMgmt import dbSet


class profileSummaryManagement:
	def getAllClientNames(self, emailId: str):
		# Get list of clientIds from Users collection
		filter = {"emailId": emailId.lower()}
		clientList = dbSet.findOneDB(dbSet.getUsers(), filter)
		if clientList is None:
			return []
		clients = list(clientList["clients"])
		# Loop through clientIds, find the names for each client and add to clientNames array
		clientNames = []
		for clientId in clients:
			filter = {"clientId" : clientId}
			name = dbSet.findOneDB(dbSet.getClients(), filter)["name"]
			clientStatus = clientService.getClientOverallStatus(clientId)
			businessStatus= ""
			if clientStatus.status == "Initial":
				businessStatus = "Not Started"
			elif clientStatus.status == "Complete":
				businessStatus = "Complete"
			else:
				businessStatus = "In Progress"
			clientInfo = {
				"clientId" : clientId,
				"name" : name,
				"businessStatus" : businessStatus
			}
			clientNames.append(clientInfo)
		return clientNames

		
	def getTaxValuesDetails(self, clientId: UUID):
		try:
			clientId = str(clientId)
			# Query the client again to pull the necessary tax values to return
			filter = {"clientId" : clientId}
			client = dbSet.findOneDB(dbSet.getClients(), filter)
			taxValues = TaxValuesRequestDomain(taxLiability=client["taxLiability"]["totalTax"], ltcg=client["taxLiability"]["ltcg"], stcg=client["taxLiability"]["stcg"], portfolioValueIn=client["portfolioValues"]["in"], portfolioValueOut=client["portfolioValues"]["out"])
			return taxValues
		except Exception as e:
			logger.exception(e)
		
	def getHoldingsDetails(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			return dbSet.findOneDB(dbSet.getHoldings(), filter)["holdings"]
		except Exception as e:
			logger.exception(e)
		
	def getUserPreferencesDetails(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			return {"diagrams" : dbSet.findOneDB(dbSet.getClients(), filter)["userPreferences"]}
		except Exception as e:
			logger.exception(e)
		
	def setUserPreferencesDetails(self, clientId: UUID, userPreferences: UserPreferencesRequestDomain):
		try:
			clientId = str(clientId)
			newPreferences = []
			for diagram in userPreferences.diagrams:
				newDiagram = {
					"name" : diagram.name,
					"size" : diagram.size
				}
				newPreferences.append(newDiagram)
			filter = {"clientId" : clientId}
			proj = { "$set" : { "userPreferences" : newPreferences}}
			dbSet.updateOneDB(dbSet.getClients(), filter, proj)
			return userPreferences
		except Exception as e:
			logger.exception(e)

	
profileSummaryService = profileSummaryManagement()
	