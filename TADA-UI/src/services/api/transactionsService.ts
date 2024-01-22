import { axiosClient } from './commonService'
import { serviceEndpoints, apiEndpoints } from '../../utils/apiConfig'
import { transactionDataType, transactionPaginationResponse } from '../../pages/transactions/transactionsInterface';
import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import commonConstants from '../../utils/constants/commonConstants';
import transactionConstant from '../../utils/constants/transactionConstant';

const getAllTransactions = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string, page: number, pageSize: number): Promise<transactionPaginationResponse> => {
    return new Promise<transactionPaginationResponse>((resolve, reject) => {
        try {
            if (!commonConstants.DummyDataUsed.transactionData) {
                axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTransactions}${clientId}?start_index=${page}&size=${pageSize}`, instance, accounts, "GET", clientId).then((response: any) => {
                    resolve(response.data)
                }).catch((err: any) => {
                    reject(err)
                })
            }
            else{
                resolve({
                    "data": transactionConstant.dummyTransactionData,
                    "start_index": 0,
                    "size": 500,
                    "total_count": 8
                })

            }
        }
        catch (ex) {
            reject(ex);
        }
    });
}


export default { getAllTransactions }