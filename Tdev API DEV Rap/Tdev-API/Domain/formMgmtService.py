from Infrastructure.dbMgmt import dbSet
from Infrastructure.blobMgmt import blobSet
from Infrastructure.queueMgmt import queueSet
from util import *
from loggerUtil import logger
from Domain.domainModels.domainRequest import *
from Domain.domainModels.domainResponse import *
import re
import json
import base64
import uuid

class formManagement:
	def getFormConfigDetails(self, form : int, year : int):
		try:
			form = str(form)
			year = str(year)
			filter = {"form" : form, "year" : year}
			proj = {"_id" : 0}
			return dbSet.findOneDB(dbSet.getFormConfigs(), filter, proj)
		except Exception as e:
			logger.exception(e)

	def getCheckBoxData(self, clientId: UUID, sectionId: UUID):
		try:
			clientId = str(clientId)
			sectionId = str(sectionId)
			filter = {"clientId" : clientId, "sectionId" : sectionId, "checkboxData" : {"$exists" : True}}
			checkboxData = dbSet.findOneDB(dbSet.getFormData(), filter)
			if not checkboxData:
				return {
					"sectionId" : sectionId,
					"checkboxData" : []
				}
			else:
				return checkboxData
		except Exception as e:
			logger.exception(e)
						
	def getSavedTableDataDict(self, clientId: UUID, sectionId: UUID, mode: str, start_index: int, size: int):
		try:
			clientId = str(clientId)
			sectionId = str(sectionId)
			skips = start_index - 1
			filter = {"clientId" : clientId,"sectionId" : sectionId, "mode" : mode, "isActive" : True}
			if(skips > 0):
				rows = list(dbSet.findManyDB(dbSet.getFormData(), filter).skip(skips).limit(size))
			else:
				rows = list(dbSet.findManyDB(dbSet.getFormData(), filter).limit(size))
			totalCount = dbSet.countDB(dbSet.getFormData(), filter)
			tableData = []
			for row in rows:
				rowObj = {
					"rowId" : row["rowId"],
					"columns" : []
				}
				for column in row["columns"]:
					colObj = {
						"column" : column
					}
					rowObj["columns"].append(colObj)
				rowWrapper = {
					"row" : rowObj
				}
				tableData.append(rowWrapper)
			response = {
				"sectionId" : sectionId,
				"tableData" : tableData,
				"total_count" : totalCount
			}
			return response
		except Exception as e:
			logger.exception(e)
			
	def deleteRowDetails(self, rowId: UUID):
		try:
			rowId = str(rowId)
			filter = {"rowId" : rowId}
			proj = {"$set" : {"isActive" : False}}
			return dbSet.findOneUpdateDB(dbSet.getFormData(), filter, proj)
		except Exception as e:
			logger.exception(e)
			
	def saveFormDataDetails(self, clientId: UUID, mode: str, formData: SectionsRequestDomain):
		try:
			clientId = str(clientId)
			# Loop through each secion
			for section in formData.sections:
				# Get checkbox data and save it for upload
				if(section.checkboxData):
					sectionCheckboxData = []
					for checkbox in section.checkboxData:
						checkboxOption = {
							"optionId" : str(checkbox.optionId),
							"optionValue" : checkbox.optionValue
						}
						sectionCheckboxData.append(checkboxOption)
					# Create document, overwrite current data and insert new data into db
					checkboxData = {
						"clientId" : clientId,
						"sectionId" : str(section.sectionId),
						"checkboxData" : sectionCheckboxData    
					}
					filter = {"clientId" : clientId, "sectionId" : str(section.sectionId), "checkboxData" : {"$exists" : True}}
					dbSet.deleteOneDB(dbSet.getFormData(), filter)
					dbSet.insertOneDB(dbSet.getFormData(), checkboxData)
				# Get table data by iterating through rows
				if(section.tableData):
					for rowObj in section.tableData:
						rowId = str(rowObj.row.rowId)
						columns = []
						for column in rowObj.row.columns:
							columns.append(column.column.dict())
						# Update column h, column d - e + g
						if columns[6]["columnValue"]:
							if type(columns[6]["columnValue"]) is float:
								columns[7]["columnValue"] = format(round(columns[3]["columnValue"] - columns[4]["columnValue"] + columns[6]["columnValue"],2), '.2f')
								columns[6]["columnValue"] = format(columns[6]["columnValue"], '.2f')
							elif '(' in columns[6]["columnValue"]:
								adj = str(columns[6]["columnValue"])
								adj = re.sub(r'[()]', '', adj)
								columns[7]["columnValue"] = format(round(columns[3]["columnValue"] - columns[4]["columnValue"] - float(adj),2), '.2f')
								formatted = format(float(adj), '.2f')
								columns[6]["columnValue"] = f'({formatted})'      
						else:
							columns[7]["columnValue"] = format(round(columns[3]["columnValue"] - columns[4]["columnValue"], 2), '.2f')
						# Place paranthesis around negative profit values
						if float(columns[7]['columnValue']) < 0:
							absValue = format(abs(float(columns[7]['columnValue'])), '.2f')
							columns[7]['columnValue'] = f'({absValue})'
						# Check if row is new. If new, insert new document, otherwise update document
						filter = {"rowId" : rowId, "clientId": clientId}
						existingRow = dbSet.findOneDB(dbSet.getFormData(), filter)
						if not existingRow:
							newRowDoc = {
								"clientId" : clientId,
								"form" : "8949",
								"mode" : mode,
								"rowId" : rowId,
								"sectionId" : str(section.sectionId),
								"isActive" : True,
								"columns" : columns
							}
							dbSet.insertOneDB(dbSet.getFormData(), newRowDoc)
						else:
							proj = {"$set" : {"columns" : columns}}
							dbSet.updateOneDB(dbSet.getFormData(), filter, proj)
			return "Table Data Saved"
		except Exception as e:
			logger.exception(e)
			message="exception: {}".format(e)
			return message
			
	def getTotalsObj(self, clientId: UUID, mode: str):
		try:
			clientId = str(clientId)
			filter = {"form" : "8949", "year" : "2022"}
			formConfig = dbSet.findOneDB(dbSet.getFormConfigs(), filter)

			totalObj = []
			for section in formConfig["sections"]:
				filter = {"clientId" : clientId, "form" : "8949", "mode" : mode, "sectionId" : str(section["sectionId"]), "isActive" : True}
				formDocs = list(dbSet.findManyDB(dbSet.getFormData(), filter))
				proceedTotal = 0.0
				costTotal = 0.0
				adjTotal = 0.0
				profitTotal = 0.0
				for doc in formDocs:
					proceedTotal = proceedTotal + doc["columns"][3]["columnValue"]
					costTotal = costTotal + doc["columns"][4]["columnValue"]
					if '(' in doc["columns"][7]["columnValue"]:
						colVal = str(doc["columns"][7]["columnValue"])
						colVal = re.sub(r'[()]', '', colVal)
						profitTotal = profitTotal - float(colVal)
					else:
						profitTotal = profitTotal + float(doc["columns"][7]["columnValue"])
					if doc["columns"][6]["columnValue"]:
						if '(' in doc["columns"][6]["columnValue"]:
							colVal = str(doc["columns"][6]["columnValue"])
							colVal = re.sub(r'[()]', '', colVal)
							adjTotal = adjTotal - float(colVal)
						else:
							adjTotal = adjTotal + float(doc["columns"][6]["columnValue"])
				# Place paranthesis around negative adjustment and profit totals
				adjTotal = format(round(adjTotal, 2), '.2f')
				if float(adjTotal) < 0:
					absValue = format(abs(float(adjTotal)), '.2f')
					adjTotal = f'({absValue})'
				profitTotal = format(round(profitTotal, 2), '.2f')
				if float(profitTotal) < 0:
					absValue = format(abs(float(profitTotal)), '.2f')
					profitTotal = f'({absValue})'
				sectionObj = {
					"sectionId" : str(section["sectionId"]),
					"total" : {
						"columns" : [
							{
								"column": {
									"columnId" : section["tableConfig"][3]["columnId"],
									"columnValue" : format(round(proceedTotal,2), '.2f')

								}
							},
							{
								"column": {
									"columnId" : section["tableConfig"][4]["columnId"],
									"columnValue" : format(round(costTotal, 2), '.2f')

								}
							},
							{
								"column": {
									"columnId" : section["tableConfig"][6]["columnId"],
									"columnValue" : adjTotal

								}
							},
							{
								"column": {
									"columnId" : section["tableConfig"][7]["columnId"],
									"columnValue" : profitTotal

								}
							}
						]
					}
				}
				totalObj.append(sectionObj)
			return totalObj
		except Exception as e:
			logger.exception(e)
			
	def generatePDFAndSave(self, clientId: UUID):
		try:
			clientId = str(clientId)
			filter = {"clientId" : clientId}
			proj = {"$inc" : {"pdfGeneration" : 1}}
			dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
			# Fetch the latest version of PDF generated
			filter = {"clientId" : clientId}
			fetch_userrow = dbSet.findOneDB(dbSet.getPdfFormGeneration(), filter)
			if fetch_userrow is None or not fetch_userrow["8949Form"]:
				latestVersion_incremented = "V1"
			else:
				fetch_latestVersion = fetch_userrow["8949Form"][-1]["version"]
				latestVersion_incremented = fetch_latestVersion[0] + str(int(fetch_latestVersion[1:]) + 1)

			unique_id = uuid.uuid4().hex
			# Get mode from Clients collection
			try:
				filter = {"clientId" : clientId}
				# mode = dbSet.findOneDB("TADADB", "Clients", filter)["taxliability"]["mode"]
				mode = dbSet.findOneDB(dbSet.getClients(), filter)["taxLiability"]["mode"]
			except Exception as e:
				mode = ""

			# Calculate totals and insert to Database
			totalSum = self.getTotalsObj(clientId, mode)
			for terms in totalSum:
				terms.update({"clientId":clientId, "version":latestVersion_incremented})
				dbSet.insertOneDB(dbSet.getFormDataTotals(), terms)

			# Create message and send to queue
			msg = {
				"clientId" : clientId,
				"mode" : mode,
				"uuid" : unique_id,
				"version" : latestVersion_incremented
			}
			queueSet.get_queue_client("pdfgeneration").send_message(json.dumps(msg, default=str))
		except Exception as e:
			logger.exception(e)
			
	def pdfDownload(self, clientId: UUID, year: int, form: int, version: str):
		try:
			# Get file name
			clientId = str(clientId)
			year = str(year)
			form = str(form)
			try:
				filter = {"clientId" : clientId, "year" : year}
				data = dbSet.findOneDB(dbSet.getPdfFormGeneration(), filter)[form + "Form"]
			except KeyError:
				return ("Form {} not present".format(form))
			except TypeError:
				return "Please provide valid year or clientId"
			file_name = None
			for d in data:
				if d['version'] == version:
					file_name = d['fileName']
					break

			if file_name:
				blobClient = blobSet.blob_service_client.get_blob_client(container = "generatedtaxforms", blob = file_name)
				if blobClient.exists():
					#streamdownloader = blobClient.download_blob()
					pdf_content = blobClient.download_blob().readall()
					encoded_string = base64.b64encode(pdf_content)
					#return Response(pdf_content, media_type="application/pdf")
					return encoded_string
				else:
					return "File does not exist"
			return "File does not exist"
		except Exception as e:
			logger.exception(e)
			message="exception: {}".format(e)
			return message
		
	def getAllVersions(self, clientId: UUID, year: int, form: int):
		try:
			year = str(year)
			form = str(form)
			clientId = str(clientId)
			##need to extract list of versions for specific form from mongoDB
			try:
				filter = {"clientId" : clientId, "year":year}
				data = dbSet.findOneDB(dbSet.getPdfFormGeneration(), filter)[form + "Form"]
			except Exception as e:
				return []
			filter = {"clientId" : clientId}
			pdfStatus = dbSet.findOneDB(dbSet.getStatuses(), filter)["pdfGeneration"]
			if pdfStatus==0:
				pdfStatus_latest = 'Processed'
			elif pdfStatus==1:
				pdfStatus_latest = 'Processing'

			allData = []
			for d in data:
				dict1 = {}
				dict1['version'] = d['version']
				dict1['fileName'] = d['fileName']
				dict1['creationDate'] = d['creationDate']
				dict1['pdfstatus'] = 'Processed'
				allData.append(dict1)

			if allData:
				allData[-1].update({"pdfstatus":pdfStatus_latest})
			return allData
		except Exception as e:
			logger.exception(e)
		
		
formService = formManagement()