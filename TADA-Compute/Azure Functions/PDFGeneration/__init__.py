import json
import azure.functions as func

from Domain.PDFGenerationService.GeneratePDF import populatePDFvalues

from LoggerUtils import App_logger

def main(msg: func.QueueMessage) -> None:
    App_logger.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
                 
    '''
    msg param : "ClientID" , "mode", "uuid", "version"
    '''

    msg_param = json.loads(msg.get_body())
    generatepdf = populatePDFvalues(msg_param)
    generatepdf.pdf_table_Mapping()