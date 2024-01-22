import { useMsal } from '@azure/msal-react'
import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { profileStore } from '../../utils/store/store'
import Logger from '../../services/azure/appInsights/Logger/logger'
import { SeverityLevel } from '@microsoft/applicationinsights-web'
import taxFormConstants from '../../utils/constants/taxFormConstants'
import taxFormServices from '../../services/api/taxFormServices'
import { taxformCheckboxDatatType, taxFormConfigDataType, taxFormDataType, taxformTableDataResponseType } from './taxFormInterface'
import checkboxProps from '../../components/common/checkbox/checkboxInterface'
import { isEmpty, numberIntoCurrency } from '../../utils/helper'
import messages from '../../utils/constants/messages'
import { message } from 'antd'
import { useNavigate } from 'react-router-dom'

var _ = require('lodash')
const taxFormDomain = () => {
  const { instance, accounts } = useMsal()
  const currentProfile = useSelector(profileStore)
  const [taxFormConfig, setTaxFormConfig] = useState<taxFormConfigDataType>(

  )
  const [taxFormData, setTaxFormData] = useState<taxFormDataType>(

  )
  const [taxFormFinalData, setTaxFormFinalData] = useState<taxFormDataType>()
  const [isSubmitData, setIsSUbmitData] = useState(false);

  useEffect(() => {

    getConfigurationData()
  }, [])
  useEffect(() => {
    getCheckboxData()
  }, [taxFormData])
  useEffect(() => {
    if (taxFormConfig) {
      setTaxFormData(_.cloneDeep(taxFormConfig))
      taxFormConfig.sections.map((eachSection) => {
        getSectionTableData(eachSection.sectionId)
      })

    }
  }, [taxFormConfig])

  const onSaveButtonClick = () => {
    if (taxFormFinalData !== undefined) {
      let formData = { ...taxFormFinalData! }
      formData.status = "Progressing";

      setTaxFormFinalData(formData);
      updateformData(formData, "save")
    }
  }

  const onSubmitButtonClick = () => {
    if (taxFormFinalData !== undefined) {
      let formData = { ...taxFormFinalData! }
      formData.status = "Completed";
      setTaxFormFinalData(formData);
      updateformData(formData, "submit")
    }
    sessionStorage.setItem("8949","Form Generated")
    window.location.pathname="/TADA/profileSummary"
    
  }


  const updateFinalData = (data: any, sectionId: string, typeOfData: string) => {
    if (taxFormData !== undefined) {
      let tempData = { ...taxFormData! }
      tempData.sections.map((dataItem) => {
        if (dataItem.sectionId === sectionId) {
          if (typeOfData == "table")
            dataItem.tableData = data;
          else if (typeOfData == "checkbox")
            dataItem.checkBoxData = data;
        }
      })
      setTaxFormFinalData({ ...tempData })

    }
  }

  const getSectionTableData = (sectionId: string) => {

    Logger.trackTrace({
      message: 'getting section table data for the sectionID' + sectionId,
      data: `id =${String(currentProfile.clientId)}`,
      severityLevel: SeverityLevel.Information,
    })
    getSectionTableDataByPagination(sectionId, 0, 500);
  }

  const getSectionTableDataByPagination = (sectionId: string, start: number, end: number) => {
    taxFormServices.getSectionTableData(instance, accounts, currentProfile.clientId!, sectionId, start, end).then(
      (response: taxformTableDataResponseType) => {
        if (response != null) {
          setTaxFormData((prevState) => {
            let sections = [...prevState!.sections];
            sections.map((eachSection) => {
              if (eachSection.sectionId == response.sectionId) {
                eachSection.tableData = [...(eachSection.tableData ? [...eachSection.tableData!] : []), ...response.tableData!]

              }
            });
            return (_.cloneDeep({ ...prevState, sections: [...sections] }))
          })

          if (response.tableData!.length == end) {
            getSectionTableDataByPagination(sectionId, start + end, end)
          }

        }
      }).catch((err) => {

      })
  }

  const getConfigurationData = () => {
    Logger.trackTrace({
      message: 'Get tax form config',
      data: `id =${String('tax form config')}`,
      severityLevel: SeverityLevel.Information,
    })
    taxFormServices
      .getTaxFormConfig(instance, accounts, '8949', '2022')
      .then((response: taxFormConfigDataType) => {
        setTaxFormConfig(response)

        Logger.trackTrace({
          message: 'returned tax form config',
          data: `response =${JSON.stringify(response)}`,
          severityLevel: SeverityLevel.Information,
        })
      })
      .catch((err) => {
        Logger.trackException({ message: err })
      })
  }

  const getCheckboxData = () => {
    Logger.trackTrace({
      message: 'Get checkBox data',
      data: `id =${String('checkBox data')}`,
      severityLevel: SeverityLevel.Information,
    })
    taxFormServices
      .getCheckboxData(
        instance,
        accounts,
        currentProfile.clientId!,
        '8949',
        '2022',
      )
      .then((response: taxFormDataType) => {
        if (response != null) {
          let tempTaxFormData: taxFormDataType = taxFormData!;
          tempTaxFormData.sections.map((eachSection) => {
            response.sections.map((responseItem) => {
              if (eachSection.sectionId == responseItem.sectionId) {
                if (isEmpty(eachSection.checkBoxData)) eachSection.checkBoxData = [];
                eachSection.checkBoxData = responseItem.checkBoxData!
              }
            })

          })
          setTaxFormData({ ...tempTaxFormData! })
          Logger.trackTrace({
            message: 'returned checkBox data',
            data: `response =${JSON.stringify(response)}`,
            severityLevel: SeverityLevel.Information,
          })
        }
        else {
          let tempTaxFormData: taxFormDataType = taxFormData!;
          tempTaxFormData.sections.map((eachSection) => {
            let checkboxData: taxformCheckboxDatatType[] = [];
            if (eachSection.checkBoxConfig) {
              eachSection.checkBoxConfig.map((eachConfig) => {
                checkboxData.push({ name: eachConfig.optionId, optionId: eachConfig.optionId, optionValue: eachConfig.defaultValue })
              })
            }
            eachSection.checkBoxData=checkboxData
          })
        }
      }) 
      .catch((err) => {
        Logger.trackException({ message: err })
      })
  }

  const updateformData = (formData: taxFormDataType, buttonClick: string) => {
    Logger.trackTrace({
      message: 'update form data',
      data: `id =${String('update form data')}`,
      severityLevel: SeverityLevel.Information,
    })
    taxFormServices
      .updateFormData(
        instance,
        accounts,
        currentProfile.clientId!,
        formData!
      )
      .then((response: taxFormDataType) => {
        Logger.trackTrace({
          message: 'returned checkBox data',
          data: `response =${JSON.stringify(response)}`,
          severityLevel: SeverityLevel.Information,
        })
        buttonClick !== "submit" ?
          message.info(messages.saveTaxFormData) :
          setIsSUbmitData(true);
      })
      .catch((err) => {
        Logger.trackException({ message: err })
      })
  }

  return { isSubmitData, updateFinalData, taxFormData, taxFormFinalData, onSaveButtonClick, onSubmitButtonClick }
}
export default taxFormDomain
