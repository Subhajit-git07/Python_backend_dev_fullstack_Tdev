
import taxLiabilitySummaryConstant from '../../utils/constants/taxLiabilitySummaryConstatnts'
import barChartDataType from '../../components/common/charts/barChart/barChartInterface';
import { TaxLiabilitySummary } from '../../pages/taxLiabilitySummary/taxLiabilitySummaryInterface';
import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import { axiosClient } from './commonService';
import { serviceEndpoints, apiEndpoints } from '../../utils/apiConfig';
import commonConstants from '../../utils/constants/commonConstants';

const getTaxLiabilitySummary = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string): Promise<TaxLiabilitySummary[]> => {
    return new Promise<TaxLiabilitySummary[]>((resolve, reject) => {
        try {
            if(commonConstants.DummyDataUsed.taxSummaryData == true){
                resolve([taxLiabilitySummaryConstant.barChartData])
              }
              else{
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTaxSummary}${clientId}`, instance, accounts, "GET").then((response: any) => {
                resolve([response.data])
            }).catch(() => {
                resolve([]);
            })
        }
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const getTaxSummaryStatus = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTaxSummaryStatus}${clientId}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data.status)
            }).catch(() => {
                resolve("Error in tax summary status");
            })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}


export default { getTaxLiabilitySummary,getTaxSummaryStatus}