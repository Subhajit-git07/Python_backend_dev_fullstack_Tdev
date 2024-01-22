from fastapi import APIRouter, Query
from api.models.response import *
from api.models.request import *
from loggerUtil import logger
from Domain.formMgmtService import formService
from pydantic import BaseModel

router = APIRouter()

@router.get("/config")
def getFormConfig(form: int = Query(ge=0, le=10000), year: int = Query(ge=0, le=2100)):
	try:
		configDetails = formService.getFormConfigDetails(form, year)
		return configDetails
	except Exception as e:
		logger.exception(e)

@router.get("/checkbox/{clientId}", response_model=SectionCheckboxResponse)
def getSavedCheckboxValues(clientId: UUID, sectionId: UUID):
	try:
		checkboxData = formService.getCheckBoxData(clientId, sectionId)
		return checkboxData
	except Exception as e:
		logger.exception(e)
    
@router.get("/table/{clientId}", response_model=SectionTableDataResponse)
def getSavedTableData(clientId: UUID, sectionId: UUID, mode: str = Query(max_length=4), start_index: int = Query(ge=0, le=10**8), size: int = Query(ge=0, le=10**8)):
	try:
		dataDict = formService.getSavedTableDataDict(clientId, sectionId, mode, start_index, size)
		return dataDict
	except Exception as e:
		logger.exception(e)

@router.delete("/{rowId}", response_model=RowAltResponse)
def deleteRow(rowId: UUID):
	try:
		data = formService.deleteRowDetails(rowId)
		return data
	except Exception as e:
		logger.exception(e)

@router.post("/{clientId}")
def saveFormData(clientId: UUID, formData: SectionsRequest, mode: str = Query(max_length=4)):
	try:
		msg = formService.saveFormDataDetails(clientId, mode, formData)
		return msg
	except Exception as e:
		logger.exception(e)

@router.get('/totals/{clientId}')
def getTotals(clientId: UUID, mode: str = Query(max_length=4)):
	try:
		totalObj = formService.getTotalsObj(clientId, mode)
		return totalObj
	except Exception as e:
		logger.exception(e)

@router.post('/generatePdf/{clientId}')
def generatePDF(clientId: UUID):
	try:
		pdfGen = formService.generatePDFAndSave(clientId)
	except Exception as e:
		logger.exception(e)


@router.get('/downloadPdf/{clientId}')
def getPdf(clientId: UUID, version: str, year: int = Query(ge=0), form: int = Query(ge=0)):
	try:
		msg = formService.pdfDownload(clientId, year, form, version)
		return msg
	except Exception as e:
		logger.exception(e)
		
@router.get('/listOfVersions/{clientId}', response_model=List[VersionDataResponse])
def getversions(clientId: UUID, year: int = Query(ge=0, le=2100), form: int = Query(ge=0, le=10000)):
	try:
		allVersions = formService.getAllVersions(clientId, year, form)
		return allVersions
	except Exception as e:
		logger.exception(e)


