
import bcatTemplateConstants from '../../utils/constants/bcatTemplateConstants'
import {DataTypeBCAT} from '../../pages/taxLiabilitySummary/taxLiabilitySummaryInterface';
import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import { axiosClient } from './commonService';
import { serviceEndpoints, apiEndpoints } from '../../utils/apiConfig';

const getBCATTemplateData = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string): Promise<DataTypeBCAT[]> => {
    return new Promise<DataTypeBCAT[]>((resolve, reject) => {
        try {
           // axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTaxSummary}${clientId}`, instance, accounts, "GET").then((response: any) => {
                resolve(bcatTemplateConstants.BCATData)
            // }).catch(() => {
            //     resolve([]);
            // })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}



export default { getBCATTemplateData}