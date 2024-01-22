import { axiosClient } from './commonService'
import { serviceEndpoints, apiEndpoints } from '../../utils/apiConfig'
import profileSummaryConstants from '../../utils/constants/profileSummaryConstants'
import commonConstants from '../../utils/constants/commonConstants';
import DataTypeHoldings from '../../components/holdings/holdingsInterface';

import {taxValuesDataType} from '../../pages/profileSummary/profileSummaryInterface';
import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import profileDataType from '../../pages/profile/profileInterface';

const getClients = (instance:IPublicClientApplication,accounts:AccountInfo[], emailId: string): Promise<profileDataType[]> => {
    return new Promise<profileDataType[]>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClients}${emailId}`, instance,accounts,"GET").then((response:any)=>{
                resolve(response.data);
            }).catch((error:any )=> {
                    reject(error);
                })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const getTaxValues = (instance:IPublicClientApplication,accounts:AccountInfo[], clientId: string): Promise<taxValuesDataType> => {
    return new Promise<taxValuesDataType>((resolve, reject) => {
        try {
            if(commonConstants.DummyDataUsed.taxValues == true){
                resolve(profileSummaryConstants.taxValues);
            }
            else{
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTaxValues}${clientId}`, instance,accounts,"GET").then((response:any)=>{
                resolve(response.data);
            }).catch((error:any )=> {
                reject(error);
            })
        }
        }
        catch (ex) {
             reject(ex);
        }
    });
}
const getHoldings = (instance:IPublicClientApplication,accounts:AccountInfo[],clientId:string): Promise<DataTypeHoldings[]> => {
    return new Promise<DataTypeHoldings[]>((resolve, reject) => {
        try {
            if(commonConstants.DummyDataUsed.holdings == true){
                resolve(profileSummaryConstants.holdingsData);
            }
            else{
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getHoldings}${clientId}`, instance,accounts,"GET").then((response:any) => {
                
                resolve(response.data)
            }).catch((error:any )=> {
                reject(error);
            })
        }
        }

        catch (ex) {
            return reject(ex);
        }
    });
}



export default { getClients, getHoldings, getTaxValues }