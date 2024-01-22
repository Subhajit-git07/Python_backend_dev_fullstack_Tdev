
import type { ColumnsType, SorterResult } from 'antd/lib/table/interface';
import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { profileStore } from "../../utils/store/store";
import {taxValuesDataType} from "./profileSummaryInterface";
import profileSummaryService from "../../services/api/profileSummaryService";
import { useMsal } from '@azure/msal-react';
import { SeverityLevel } from '@microsoft/applicationinsights-web';
import Logger from '../../services/azure/appInsights/Logger/logger';
import {message} from 'antd';

const profileSummaryDomain = () => {
  const currentProfile = useSelector(profileStore)
  const { instance, accounts } = useMsal();
  const [taxValues, setTaxValues] = useState<taxValuesDataType>({})
  const[loaderTaxValue,setLoader]=useState(false);
  const [psYear,setPSYear]=useState({
    year:(new Date().getFullYear()).toString(),
  })
  useEffect(() => {
    if (currentProfile.clientId) {
      getTaxValues();
    }
    else {
      setTaxValues({})
      setTimeout(function() { //Start the timer
        message.info("Please select client to see the detail information.")
    }.bind(this), 3000)
    }
  }, [currentProfile])

  const getTaxValues = () => {
    setLoader(true)
    Logger.trackTrace({message:"Get Tax Values",data:`id =${String(currentProfile.clientId)}`, severityLevel:SeverityLevel.Information})
    profileSummaryService.getTaxValues(instance, accounts, currentProfile.clientId!).then(function (response) {
      Logger.trackTrace({message:"returned Tax Values",data:`response =${JSON.stringify(response)}`, severityLevel:SeverityLevel.Information})
      setTaxValues(response)
      setLoader(false)
    }).catch((err)=>{
      setLoader(false)
      Logger.trackException({message:err})
      Logger.trackTrace({message:"error in getting Tax Values",data:`response =${JSON.stringify(err)}`, severityLevel:SeverityLevel.Error})
    })
  }
  return { taxValues, loaderTaxValue,setPSYear,psYear}
}
export default profileSummaryDomain