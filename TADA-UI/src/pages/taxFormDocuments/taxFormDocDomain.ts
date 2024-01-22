import getAccessToken from '../../services/azure/accessToken'
import { useMsal } from '@azure/msal-react'
import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux';
import { profileStore } from '../../utils/store/store';
import { useNavigate } from 'react-router-dom'
import taxFormDataType from './taxFormDocInterface';

const useTaxLiabilitySummary = () => {
  let { instance, accounts } = useMsal();
  const currentProfile = useSelector(profileStore);

  const [taxFormData,setTaxFormData]=useState<taxFormDataType>({
    year:(new Date().getFullYear()).toString(),
    taxFormType:""
  })
  const navigate = useNavigate();

 
  return {
    setTaxFormData,taxFormData
  }
}
export default useTaxLiabilitySummary
