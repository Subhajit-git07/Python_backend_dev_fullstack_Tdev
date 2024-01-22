import getAccessToken from '../../services/azure/accessToken'
import { useMsal } from '@azure/msal-react'
import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux';
import { profileStore } from '../../utils/store/store';
import Logger from '../../services/azure/appInsights/Logger/logger'
import { TaxLiabilitySummary, DataTypeBCAT,taxFormDataType } from './taxLiabilitySummaryInterface'
import { SeverityLevel } from '@microsoft/applicationinsights-web'
import messages from '../../utils/constants/messages';
import { message } from 'antd';
import taxLiabilitySummary from "../../services/api/taxLiabilitySummaryService";
import commonConstatnt from "../../utils/constants/commonConstants";
import { useNavigate } from 'react-router-dom'
import bcatTemplateService from '../../services/api/bcatTemplateServices';
import { Excel } from 'antd-table-saveas-excel';
import bcatTemplateConstants from '../../utils/constants/bcatTemplateConstants';

const useTaxLiabilitySummary = () => {
  let { instance, accounts } = useMsal();
  const currentProfile = useSelector(profileStore);
  const [taxSummaryData, setTaxSummaryData] = useState<TaxLiabilitySummary[]>(
    [],
  )
  const [bcatTemplateData, setbcatTemplateData] = useState<DataTypeBCAT[]>(
    [],
  )
  const [loader,setLoader]=useState(false);
  const [loaderMessage,setloaderMessage]=useState("");
  const [taxFormData,setTaxFormData]=useState<taxFormDataType>({
    year:(new Date().getFullYear()).toString(),
    taxFormType:""
  })
  const navigate = useNavigate();

  useEffect(() => {
    currentProfile.clientId ? getTaxSummaryStatus() : setTaxSummaryData([])
    getBCATTemplateData();
  }, [currentProfile])

  const bcatColumns=bcatTemplateConstants.BCATColumns;

  const downloadBcatReport = () => {
    const excel = new Excel()
    excel
      .setTHeadStyle({background:"bcbcbc",fontName:"Calibri",fontSize:11})
      .setRowHeight(8)
      .setTBodyStyle({fontName:"Calibri",fontSize:11})
      .addSheet('BCA-Tax-Template')
      .addColumns(bcatColumns)
      .addDataSource(bcatTemplateData, {
        str2Percent: true,
      })
      .saveAs('BCA-Tax-Template.xlsx')
  }
 

  let getTaxSummaryStatus = () => {
    setLoader(true)
    setloaderMessage('Tax summary data is loading Please wait...')
    Logger.trackEvent({
      message: 'Get Tax Summary satus',
      data: `id =${String(currentProfile.clientId)}`,
    })
    Logger.trackTrace({
      message: 'Get tax summary status',
      data: `id =${String(currentProfile.clientId)}`,
      severityLevel: SeverityLevel.Information,
    })
    taxLiabilitySummary
      .getTaxSummaryStatus(instance, accounts, currentProfile.clientId!)
      .then(function (response) {
        if (response == commonConstatnt.status.taxSummaryStatus) {
          Logger.trackTrace({
            message: 'Successfully get tax liability summary status',
            data: `response =${JSON.stringify(response)}`,
            severityLevel: SeverityLevel.Information,
          })
          getTaxSummaryData();
        }
        else{
          message.info(messages.taxSummaryStatus,5)
          .then(() => navigate('/TADA/addtransactions/wallet'))
         
        }
      })
      .catch((err) => {
        Logger.trackException({ message: err })
        if (err !== undefined) {
          message.error(err)
        } else {
          message.error(messages.getExchangeError)
        }
        setLoader(false)
        setloaderMessage('')
      })
  }

  let getTaxSummaryData = () => {
   // setLoader(true)
    setloaderMessage('Tax summary data is loading Please wait...')
    Logger.trackEvent({
      message: 'Get Tax Summary',
      data: `id =${String(currentProfile.clientId)}`,
    })
    Logger.trackTrace({
      message: 'Get Exchanges',
      data: `id =${String(currentProfile.clientId)}`,
      severityLevel: SeverityLevel.Information,
    })
    taxLiabilitySummary
      .getTaxLiabilitySummary(instance, accounts, currentProfile.clientId!)
      .then(function (response) {
        if (response != null) {
          // message.success(messages.addExchange)
          Logger.trackTrace({
            message: 'Successfully get tax liability summary data',
            data: `response =${JSON.stringify(response)}`,
            severityLevel: SeverityLevel.Information,
          })
          setTaxSummaryData(response)
          setLoader(false)
          setloaderMessage('')
        }
      })
      .catch((err) => {
        Logger.trackException({ message: err })
        if (err !== undefined) {
          message.error(err)
        } else {
          message.error(messages.getExchangeError)
        }
        setLoader(false)
        setloaderMessage('')
      })
  }

  let getBCATTemplateData = () => {
     Logger.trackEvent({
       message: 'Get BCAT Template data',
       data: `id =${String(currentProfile.clientId)}`,
     })
     Logger.trackTrace({
       message: 'Get BCAT Template data',
       data: `id =${String(currentProfile.clientId)}`,
       severityLevel: SeverityLevel.Information,
     })
     bcatTemplateService
       .getBCATTemplateData(instance, accounts, currentProfile.clientId!)
       .then(function (response) {
         if (response != null) {
          setbcatTemplateData(response)
           // message.success(messages.addExchange)
           Logger.trackTrace({
             message: 'Successfully get BCAT Template data',
             data: `response =${JSON.stringify(response)}`,
             severityLevel: SeverityLevel.Information,
           })
          
         }
       })
       .catch((err) => {
         Logger.trackException({ message: err })
         if (err !== undefined) {
           message.error(err)
         } else {
           message.error("error in BCAT template data")
         }
       })
   }


  return {
    taxSummaryData,loader,loaderMessage,setTaxFormData,taxFormData,downloadBcatReport
  }
}
export default useTaxLiabilitySummary
