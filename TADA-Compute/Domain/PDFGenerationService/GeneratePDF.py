from datetime import datetime
import collections
import pandas as pd
import os
import sys

from pprint import pprint
import PyPDF2
import tempfile

from PyPDF2 import PdfReader
from PyPDF2.generic import NameObject, createStringObject

from LoggerUtils import App_logger

from Infrastructure.dbMgmt import dbSet
from Infrastructure.blobMgmt import blobSet

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

class populatePDFvalues:

    def __init__(self, msg_param):
        self.form_name = "8949"
        self.clientId = msg_param["clientId"]
        self.mode = msg_param["mode"]
        self.uuid = msg_param["uuid"]
        self.version = msg_param["version"]
        self.today = datetime.now().strftime("%d-%m-%YT%H:%M:%SZ")
        self.client_name, self.client_ssn = self.fetch_client_details(self.clientId)
        self.client_details = {"clientName":self.client_name, "SSN":self.client_ssn}
        self.section = self.map_sections()
        self.ROOT_DIR = tempfile.gettempdir()
        self.source_PDF = self.download_template_from_blob(self.ROOT_DIR)
        self.output_PDF = '{}_{}_{}_{}.pdf'.format(self.clientId, self.form_name, self.uuid, self.version)
        self.dest_PDF = os.path.join(self.ROOT_DIR, self.output_PDF)
        self.pdf_reader = PyPDF2.PdfReader(open(self.source_PDF, 'rb'))
        self.pdf_writer = PyPDF2.PdfWriter()
        self.filter = {"clientId" : self.clientId}
        self.proj = {"$inc" : {"pdfGeneration" : 1}}
        dbSet.updateOneDB(dbSet.getStatuses(), self.filter, self.proj)
    

    def fetch_client_details(self, clientId):
        ''' Fetch Client name & SSN '''
        filter = {"clientId": clientId}
        fetchUser = dbSet.findOneDB(dbSet.getClients(), filter)
        if fetchUser is not None:
            try:
                users_name = fetchUser["name"]
            except Exception:
                users_name = ""
            try:
                users_taxId = fetchUser["taxId"]
            except Exception:
                users_taxId = ""
            return users_name, users_taxId
        else:
            users_name = ""
            users_taxId = ""
            return users_name, users_taxId
    

    def map_sections(self):
        SectionDict = {}
        FormConfig_section = dbSet.metaDB.FormConfigs.find({
            "form" : self.form_name
        })
        for sections in FormConfig_section:
            for s in range(len(sections["sections"])):
                SectionDict.update({
                    sections["sections"][s]["sectionName"] : sections["sections"][s]["sectionId"]
                })
        return SectionDict


    def download_template_from_blob(self, root_dir):
        ''' Download the form present in blob '''
        download_file_path = ""
        try:
            download_file_path = os.path.join(root_dir, '{}.pdf'.format(self.form_name))
            container_client = blobSet.blob_service_client.get_container_client("pdftemplates")
            blob_client = container_client.get_blob_client('{}.pdf'.format(self.form_name))
            if blob_client.exists():
                with open(download_file_path, "wb") as my_blob:
                    download_stream = blob_client.download_blob()
                    my_blob.write(download_stream.readall())
                    my_blob.close()
            else:
                App_logger.info("No PDF template found for:",self.form_name)
                return ""
        
        except Exception as err:
            App_logger.info("Cannot download the template from blob for form:", self.form_name)
            App_logger.error(err)

        return download_file_path
    

    def pdf_suffix_fields(self, page, sfx, formDict):
        ''' Rename form fields in PDF '''
        formList = []
        sfx_pgNo = sfx.split("_")[1]
        for j in range(0, len(page['/Annots'])):
            writer_annot = page['/Annots'][j].get_object()
            writer_annot.update({
                NameObject("/T"): createStringObject(writer_annot.get('/T')+sfx)
            })
            formList.append(writer_annot[NameObject("/T")])
        formDict.update({sfx_pgNo: formList})
        return formDict


    def addPages(self, st_rowcount, lt_rowcount):
        ''' Add required No. of pages for Short-term & Long-term'''
        try:
            st_formDict = collections.defaultdict(dict)
            lt_formDict = collections.defaultdict(dict)
            st_pgcount = (st_rowcount // 14) + 1
            lt_pgcount = (lt_rowcount // 14) + 1

            if st_pgcount > 0:
                for stpgs in range(st_pgcount):
                    reader1 = PdfReader(self.source_PDF)
                    getPage_short_term = reader1.pages[0]
                    self.pdf_writer.add_page(getPage_short_term)
                    stpg_renamed = self.pdf_suffix_fields(getPage_short_term, f"pg_{stpgs}", st_formDict)
                self.pdf_writer.write(self.dest_PDF)
            else:
                stpgs = 0
                reader11 = PdfReader(self.source_PDF)
                getPage_short_term_empty = reader11.pages[0]
                self.pdf_writer.add_page(getPage_short_term_empty)
                stpg_renamed = self.pdf_suffix_fields(getPage_short_term_empty, f"pg_{stpgs}", st_formDict)
                self.pdf_writer.write(self.dest_PDF)

            if lt_pgcount > 0:
                for ltpgs in range(lt_pgcount):
                    reader2 = PdfReader(self.source_PDF)
                    getPage_long_term = reader2.pages[1]
                    self.pdf_writer.add_page(getPage_long_term)
                    ltpg_renamed = self.pdf_suffix_fields(getPage_long_term, f"pg_{ltpgs + stpgs + 1}", lt_formDict)
                self.pdf_writer.write(self.dest_PDF)
            else:
                ltpgs = 0
                reader22 = PdfReader(self.source_PDF)
                getPage_long_term_empty = reader22.pages[1]
                self.pdf_writer.add_page(getPage_long_term_empty)
                ltpg_renamed = self.pdf_suffix_fields(getPage_long_term_empty, f"pg_{ltpgs + stpgs + 1}", lt_formDict)
                self.pdf_writer.write(self.dest_PDF)
            
            st_lastPage_no = list(stpg_renamed.keys())[-1]
            lt_lastPage_no = list(ltpg_renamed.keys())[-1]
        
        except Exception as err:
            App_logger.info("Error while adding pages to the PDF file")
            App_logger.error(err)

        return st_lastPage_no, lt_lastPage_no, stpg_renamed, ltpg_renamed


    def extract_data_from_DB(self):
        ''' Extract data from mongoDB '''
        try:
            st_rowcount = -1
            lt_rowcount = -1
            st_ValueDict = collections.defaultdict(dict)
            lt_ValueDict = collections.defaultdict(dict)
            
            FormConfig_checkbox = dbSet.tadaDB.FormData.find({
                "checkboxData" : {"$exists" : True},
                "clientId" : self.clientId
            })
            
            st_checkboxes = []
            lt_checkboxes = []
            if FormConfig_checkbox is not None:
                for checkboxes in FormConfig_checkbox:
                    if checkboxes["sectionId"] == self.section["Short-Term"]:
                        for stbox in checkboxes["checkboxData"]:
                            st_checkboxes.append(stbox["optionValue"])
                    elif checkboxes["sectionId"] == self.section["Long-Term"]:
                        for ltbox in checkboxes["checkboxData"]:
                            lt_checkboxes.append(ltbox["optionValue"])
            
            FormConfig_data = dbSet.tadaDB.FormData.find({"clientId":self.clientId, "mode":self.mode, "isActive":True})
            for data in FormConfig_data:
                if data["sectionId"] == self.section["Short-Term"]:
                    st_rowcount+=1
                    st_Valuelist = []
                    for col_vals in data["columns"]:
                        st_Valuelist.append(col_vals["columnValue"])
                    st_ValueDict.update({st_rowcount : st_Valuelist})
                elif data["sectionId"] == self.section["Long-Term"]:
                    lt_rowcount+=1
                    lt_Valuelist = []
                    for col_vals in data["columns"]:
                        lt_Valuelist.append(col_vals["columnValue"])
                    lt_ValueDict.update({lt_rowcount : lt_Valuelist})
        
        except Exception as err:
            App_logger.info("Error extracting FormData from database")
            App_logger.info(err)

        return st_rowcount, lt_rowcount, st_checkboxes, lt_checkboxes, st_ValueDict, lt_ValueDict


    def mapping_helper(self, key):
        ''' Maps client details '''
        return self.client_details[key]

    
    def client_details_checkbox_Mapping(self, details_renamed, checkboxes_marked):
        ''' Mapping DB data with Client details fields and CheckBox fields '''
        try:
            for detailkey, detailvalue in details_renamed.items():
                dpg_no = int(detailkey)
                dpg_no_value = detailvalue[0:5]

                for dfield in dpg_no_value:
                    if dfield.startswith("f"):
                        if dfield[3] == '1':
                            self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(dpg_no)], {dfield: self.client_name})
                        elif dfield[3] == '2':
                            self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(dpg_no)], {dfield: self.client_ssn})    
                    elif dfield.startswith("c"):
                        if len(checkboxes_marked) != 0:
                            if dfield[5] == '0' and checkboxes_marked[0] == True:
                                self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(dpg_no)], {dfield: "/1"})
                            elif dfield[5] == '1' and checkboxes_marked[1] == True:
                                self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(dpg_no)], {dfield: "/2"})
                            elif dfield[5] == '2' and checkboxes_marked[2] == True:
                                self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(dpg_no)], {dfield: "/3"})
        
        except Exception as err:
            App_logger.info("Issue in mapping Checkbox data")
            App_logger.error(err)


    def pdf_table_Mapping(self):
        st_rowcount, lt_rowcount, st_checkboxes, lt_checkboxes, st_ValueDict, lt_ValueDict = self.extract_data_from_DB()
        st_lastPage_no, lt_lastPage_no, stpg_renamed, ltpg_renamed = self.addPages(st_rowcount, lt_rowcount)
        self.client_details_checkbox_Mapping(stpg_renamed, st_checkboxes)
        self.client_details_checkbox_Mapping(ltpg_renamed, lt_checkboxes)

        ''' Mapping DB data with PDF table fields '''
        # Page 1 -Short term
        rowc = 0
        c = 0

        if bool(stpg_renamed):
            for spageKey, spageValue in stpg_renamed.items():
                spg_no = int(spageKey)
                spageValue = spageValue[5:-5]
                for field in spageValue:
                    try:
                        if isinstance(st_ValueDict[rowc][c], float) and c!=0:
                            st_ValueDict[rowc][c] = round(st_ValueDict[rowc][c],2)
                            st_ValueDict[rowc][c] = "$ " + str(st_ValueDict[rowc][c])
                        self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[spg_no], {field: st_ValueDict[rowc][c]})
                        c+=1

                        if c==8:
                            rowc+=1
                            c=0

                    except KeyError:
                        break
                    except Exception as e:
                        App_logger.error(e)

        # Page 2 - Long term
        rowc = 0
        c = 0

        if bool(ltpg_renamed):
            for lpageKey, lpageValue in ltpg_renamed.items():
                lpg_no = int(lpageKey)
                lpageValue = lpageValue[5:-5]
                for field in lpageValue:
                    try:
                        if isinstance(lt_ValueDict[rowc][c], float) and c!=0:
                            lt_ValueDict[rowc][c] = round(lt_ValueDict[rowc][c],2)
                            lt_ValueDict[rowc][c] = "$ " + str(lt_ValueDict[rowc][c])
                        self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[lpg_no], {field: lt_ValueDict[rowc][c]})
                        c+=1

                        if c==8:
                            rowc+=1
                            c=0

                    except KeyError:
                        break
                    except Exception as e:
                        App_logger.error(e)
        
        filter = {"clientId":self.clientId,"version":self.version,"sectionId":self.section["Short-Term"]}
        st_TotalSum = dbSet.findOneDB(dbSet.getFormDataTotals(), filter)
        filter = {"clientId":self.clientId,"version":self.version,"sectionId":self.section["Long-Term"]}
        lt_TotalSum = dbSet.findOneDB(dbSet.getFormDataTotals(), filter)

        st_Totalaggregation = self.write_total_to_pdf(st_TotalSum, stpg_renamed, st_lastPage_no)
        lt_Totalaggregation = self.write_total_to_pdf(lt_TotalSum, ltpg_renamed, lt_lastPage_no)
        self.pdf_writer.write(self.dest_PDF)
        templateUpload = self.upload_to_blob()

        filter = {"clientId" : self.clientId}
        proj = {"$inc" : {"pdfGeneration" : -1}}
        dbSet.updateOneDB(dbSet.getStatuses(), filter, proj)
        App_logger.info("PDF Generation successful.")
    

    def write_total_to_pdf(self, TotalSum, pg_renamed, lastPage_no):
        ''' Calculate totals for both long and short term pages '''
        try:
            TotalFields = pg_renamed[str(lastPage_no)][-5:]
            if TotalSum is not None:
                for tfield in TotalFields:
                    if tfield[3:6] == '115':
                        self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(lastPage_no)], {tfield: TotalSum["total"]["columns"][0]["column"]["columnValue"]})
                    elif tfield[3:6] == '116':
                        self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(lastPage_no)], {tfield: TotalSum["total"]["columns"][1]["column"]["columnValue"]})
                    elif tfield[3:6] == '118':
                        self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(lastPage_no)], {tfield: TotalSum["total"]["columns"][2]["column"]["columnValue"]})
                    elif tfield[3:6] == '119':
                        self.pdf_writer.update_page_form_field_values(self.pdf_writer.pages[int(lastPage_no)], {tfield: TotalSum["total"]["columns"][3]["column"]["columnValue"]})

        except Exception as err:
            App_logger.info("PDF generation - Issue with calculating Total Sum")
            App_logger.error(err)


    def upload_to_blob(self):
        ''' Upload generated template to blob '''
        try:
            blob_client = blobSet.blob_service_client.get_blob_client(container="generatedtaxforms", blob=self.output_PDF)
            with open(self.dest_PDF, "rb") as upload_data:
                blob_client.upload_blob(upload_data, overwrite=True)
                upload_data.close()
                App_logger.info("Uploaded to blob storage container as version No:"+self.version)
            return 1
        
        except Exception as err:
            App_logger.info("Issue while uploading generated template to Blob storage")
            App_logger.error(err)
            return 1
    

