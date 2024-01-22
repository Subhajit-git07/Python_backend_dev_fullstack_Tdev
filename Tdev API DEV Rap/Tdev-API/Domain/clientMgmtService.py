from Infrastructure.dbMgmt import dbSet
from Infrastructure.queueMgmt import queueSet
from fastapi import status, HTTPException
from util import *
from loggerUtil import logger
from typing import List
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *


class clientManagement:
	def clientLock(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			proj = {"$set" : {"locked" : True}}
			dbSet.updateOneDB(dbSet.getClients(), filter, proj)
			return StatusResponseDomain(status="Complete", message="Client is locked for tax year")
		except Exception as e:
			logger.exception(e)
			return StatusResponseDomain(status="Not Complete", message="exception: {}.format(e)")
	
	def getClientOverallStatus(self, clientId: UUID):
		clientId = str(clientId)
		# If user has wallets, check if classification is active
		# try:
		filter = {"clientId": clientId}
		statusDoc = dbSet.findOneDB(dbSet.getStatuses(), filter)
		if statusDoc["classification"] > 0:
			# Collect all wallets that are processing
			processingWallets = []
			processingWalletsStatus = []
			wallets = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]
			for wallet in wallets:
				if wallet["status"] == "processing":
					processingWallets.append(wallet["address"])
			for wallet in statusDoc["wallets"]:
				if wallet["address"] in processingWallets:
					processingWalletsStatus.append(WalletProcessingStatusDomain(address=wallet["address"], unclassifiedTxs=wallet["stats"]["unclassified"], classifiedTxs=wallet["stats"]["classified"]))
			return StatusResponseDomain(status="Data Processing", message = processingWalletsStatus)
		# If classification is not active, check if tax calculation is active
		filter = {"clientId": clientId}
		taxCalculationStatus = dbSet.findOneDB(dbSet.getStatuses(), filter)["taxCalculation"]
		if taxCalculationStatus > 0:
			return StatusResponseDomain(status="Tax Calculation", message="Tax calculation in progress")
		# If tax calculation is not active, check if pdf form generation process is active
		filter = {"clientId": clientId}
		pdfGenerationStatus = dbSet.findOneDB(dbSet.getStatuses(), filter)["pdfGeneration"]
		if pdfGenerationStatus > 0:
			return StatusResponseDomain(status="PDF Processing", message="PDF form is being generated")
		# filter = {"clientId": clientId}
		# Get form Data
		form8949 = dbSet.findOneDB(dbSet.getPdfFormGeneration(), filter)["8949Form"]
		# Check if user has wallets, if not they are in initial status
		filter = {"clientId": clientId}
		wallets = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]		
		if not wallets:
			return StatusResponseDomain(status="Initial", message="Client created but no wallets added")
		# Then check if client is "locked", this means client is complete for this tax year
		elif dbSet.findOneDB(dbSet.getClients(), filter)["locked"] == True:
			return StatusResponseDomain(status="Complete", message="Client complete for current tax year")
		# If PDF form generation process is not active, check if client has a pdf generated
		# Update SHAQ: 2-8 Form Generation check is after Lock check
		elif form8949:
			return StatusResponseDomain(status="Form Generated", message="At least one Form 8949 generated for client")
		elif wallets: # Wallets added, Classification done
			filter = {"clientId":clientId}
			wallets_status = dbSet.findOneDB(dbSet.getWallets(), filter)["wallets"]
			status_flag = 0
			for wallet_details in wallets_status:
				if wallet_details["status"] in ["complete", "incomplete"]:
					status_flag = 1
					return StatusResponseDomain(status="Tax Ready", message="Tax calculated for client but no form generated")
			if status_flag == 0:
				return StatusResponseDomain(status="Initial", message="Client has wallets but all failed")


		# except Exception as e:
		# 	logger.exception(e)
		# 	return StatusResponseDomain(status="Error", message="exception: {}.format(e)")

	def collectUsersForClient(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			creator = dbSet.findOneDB(dbSet.getClients(), filter)["creator"]

			userList = []
			filter = {"clients" : clientId}
			users = list(dbSet.findManyDB(dbSet.getUsers(), filter))
			for user in users:
				isCreator = False
				if user["emailId"].lower() == creator.lower():
					isCreator = True
				userObj = {
					"emailId" : user["emailId"],
					"isCreator" : isCreator
				}
				userList.append(userObj)
			
			#index = next(i for i, item in enumerate(userList) if item["emailId"] == creator)
			index = 0
			for i, item in enumerate(userList):
				if item["emailId"].lower() == creator.lower():
					index = i
					break
					
			userList[0], userList[index] = userList[index], userList[0]
			return ClientUserListResponseDomain(__root__=userList)
		except Exception as e:
			logger.exception(e)
		
	def addAccessToUsers(self, clientId: UUID, users: UserAccessListRequestDomain):
		try:
			clientId = str(clientId)
			nonAddedUsers = []
			addedUsers = []
			# Loop through all users
			for user in users:
				# Check if the user exists, if not, add them to the DB
				##chcek if it's ey.com or not
				emailId = user.user.lower()
				if len(emailId) > 6 and emailId[len(emailId)-6:] == "ey.com":
					filter = {"emailId" : user.user.lower()}
					userCheck = dbSet.findOneDB(dbSet.getUsers(), filter)
					if not userCheck:
						createUser(emailId)
					# Try to add client to user. if client is not added this means the user already has access
					filter = {"emailId" : user.user.lower()}
					proj = {"$addToSet" : {"clients" : clientId}}
					number = dbSet.updateOneDB(dbSet.getUsers(), filter, proj)
					if number.modified_count == 0:
						nonAddedUsers.append(user.user)
					else:
						addedUsers.append(user.user)
			return AddAccessListResponseDomain(nonAddedUsers=nonAddedUsers, addedUsers=addedUsers)
		except Exception as e:
			logger.exception(e)
			
		
	def removeAccessFromClient(self, clientId: UUID, emailId: str):
		try:
			clientId = str(clientId)
			filter = {"emailId" : emailId.user.lower()}
			proj = {"$pull" : {"clients" : clientId}}
			dbSet.updateOneDB(dbSet.getUsers(), filter, proj)
			return StatusResponseDomain(status="Access Removed", message=f'Removed {emailId.user} from access to client {clientId}')
		except Exception as e:
			logger.exception(e)
			return StatusResponseDomain(status="Error", message="exception:{}".format(e))
			
	def createClientLogic(self, emailId: str, item: ClientRequestDomain):
		item.clientId = str(item.clientId)
		clientResponse = ClientResponseDomain(clientId=item.clientId, name=item.name, formName=item.formName, taxId=item.taxId, addrLn1=item.addrLn1, addrLn2=item.addrLn2,
					city=item.city, state=item.state, zipCode=item.zipCode, country=item.country)
		# Check if this user has a client
		filter = {"emailId" : emailId.lower()}
		# try:
			# Check for duplicate clientIds
		filter = {"clientId" : item.clientId}
		dupClient = dbSet.findOneDB(dbSet.getClients(), filter)
		if dupClient:
			clientResponse.status = StatusResponseDomain(status="Error", message=f'Client with ID {item.clientId} already exists')
			return clientResponse
		else:
			filter = {"emailId" : emailId.lower()}
			user = dbSet.findOneDB(dbSet.getUsers(), filter)
			# If not, create a document in Users collection for this email
			if not user:
				createUser(emailId)
			# Add clientId to the user's client list and call createClientHelper to create client documents
			filter = {"emailId" : emailId.lower()}
			project = {"$push" : {"clients" : item.clientId}}
			dbSet.updateOneDB(dbSet.getUsers(), filter, project)
			createClientHelper(item, emailId)

			clientResponse.status = StatusResponseDomain(status="Client created", message=f'Client {item.clientId} created')
			return clientResponse
		# except Exception as e:
		# 	logger.exception(e)
		# 	clientResponse.status = StatusResponseDomain(status="Error", message="exception: {}.format(e)")
		# 	return clientResponse
		
	def clientDetails(self, clientId: UUID):
		clientId = str(clientId)
		# Find client in Clients collection
		filter = {"clientId" : clientId}
		# try:
		client = dbSet.findOneDB(dbSet.getClients(), filter)
		# Create client object and return
		clientResponse = ClientResponseDomain(clientId=client["clientId"], name=client["name"], formName=client["formName"], taxId=client["taxId"], addrLn1=client["address"]["addressLn1"], addrLn2=client["address"]["addressLn2"],
					city=client["address"]["city"], state=client["address"]["stateProvidence"], zipCode=client["address"]["zipCode"], country=client["address"]["country"])
		return clientResponse
		# except Exception as e:
		# 	logger.exception(e)
		
	def updateClientDetails(self, clientId: UUID, item: ClientRequestDomain):
		clientId = str(clientId)
		clientUpdateObj = {
			"clientId" : clientId,
			"name" : item.name,
			"formName" : item.formName,
			"taxId" : item.taxId,
			"address.addressLn1" : item.addrLn1,
			"address.addressLn2" : item.addrLn2,
			"address.city" : item.city,
			"address.stateProvidence" : item.state,
			"address.zipCode" : item.zipCode,
			"address.country" : item.country
		}
		clientResponse = ClientResponseDomain(clientId=clientId, name=item.name, formName=item.formName, taxId=item.taxId, addrLn1=item.addrLn1, addrLn2=item.addrLn2,
			city=item.city, state=item.state, zipCode=item.zipCode, country=item.country)
		filter = {"clientId": clientId}
		proj = {"$set" : clientUpdateObj}
		try:
			dbSet.updateOneDB(dbSet.getClients(), filter, proj)
			clientResponse.status = StatusResponseDomain(status="Client Updated", message="Successfully updated client")
			return clientResponse
		except Exception as e:
			logger.exception(e)
			clientResponse.status = StatusResponseDomain(status="Error", message="exception: {}.format(e)")
			return clientResponse
		
	def deleteClientDetails(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			client = dbSet.findOneDB(dbSet.getClients(), filter)
			if client:
				# Delete client from user list - do this here so client is removed from home page and drop down immediately
				filter = {"clients": clientId}
				proj = {"$pull" : {"clients" : clientId}}
				dbSet.updateManyDB(dbSet.getUsers(), filter, proj)
				# Send message to DBOps queue to delete other client information
				msg = {"operation": "delete client", "clientId" : clientId}
				queueSet.get_queue_client("dbopsqueue").send_message(json.dumps(msg, default=str))
				return StatusResponseDomain(status="Client Deleted", message="Successfully deleted client")
			else:
				return StatusResponseDomain(status="Client Doesn't Exist", message=f'Client with ID {clientId} does not exist')
		except Exception as e:
			logger.exception(e)
			return StatusResponseDomain(status="Error", message="exception: {}.format(e)")
		
	def getAllCountries(self):
		try:
			result = dbSet.findManyDB(dbSet.getStatesByCountries(), {})
			dataTuple = []
			for d in result:
				dataTuple.append(d["data"])
		
			allCountries = []
			for data in dataTuple[0]:
				allCountries.append(data["name"])
			return allCountries
		except Exception as e:
			logger.exception(e)
		
	def collectCitiesByCountry(self, country: str):
		country = country.lower()
		try:
			result = dbSet.findManyDB(dbSet.getStatesByCountries(), {})
			dataTuple = []
			for d in result:
				dataTuple.append(d["data"])
				
			stateList = []
			for currentCountry in dataTuple[0]:
				if currentCountry["name"].lower() == country:
					states = currentCountry["states"]
					for state in states:
						stateList.append(state["name"])
					return stateList
			return stateList
		except Exception as e:
			logger.exception(e)
		
clientService = clientManagement()