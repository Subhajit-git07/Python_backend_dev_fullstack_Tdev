from Infrastructure.dbMgmt import dbSet
from util import *
from loggerUtil import logger
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
from uuid import uuid4

class exchangesManagement:
	def addExchangeTask(self, clientId: UUID, item: ExchangeInRequestDomain):
		try:
			clientId = str(clientId)
			exchangeAdd = {
				"id" : str(uuid4()),
				"name" : item.name,
				"apiKey" : item.apiKey,
				"apiPass" : item.apiPass,
				"status" : "incomplete"
			}
			exchangeOutObj = ExchangeOutRequestDomain(id=exchangeAdd["id"], name=exchangeAdd["name"], apiKey = exchangeAdd["apiKey"], apiPass=exchangeAdd["apiPass"], status=exchangeAdd["status"])
			filter = {"clientId" : clientId}
			proj = {"$push" : {"exchanges" : exchangeAdd}}
			dbSet.updateOneDB(dbSet.getClients(), filter, proj)
			return exchangeOutObj
		except Exception as e:
			logger.exception(e)
		
	def getExchangesDetails(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			exchanges = dbSet.findOneDB(dbSet.getClients(), filter)["exchanges"]
			return exchanges
		except Exception as e:
			logger.exception(e)

	def deleteExchangeTask(self, clientId: UUID, exchangeId: str):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			proj = {"$pull" : {"exchanges" : {"id" :  exchangeId}}}
			dbSet.updateOneDB(dbSet.getClients(), filter, proj)
			return "Exchange successfully deleted from TADADB."
		except Exception as e:
			logger.exception(e)
			message="exception: {}.format(e)"
			return message
		
	def getAllExchangesNames(self):
		try:
			exchanges = dbSet.findOneDB(dbSet.getExchanges(), {})["exchanges"]
			return exchanges
		except Exception as e:
			logger.exception(e)
			
exchangeService = exchangesManagement()