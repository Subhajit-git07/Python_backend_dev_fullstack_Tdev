import { axiosClient } from './commonService'
import { serviceEndpoints, apiEndpoints } from '../../utils/apiConfig'
import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import taxFormConstants from '../../utils/constants/taxFormConstants';
import { taxFormConfigDataType, taxFormDataType, taxformTableDataResponseType } from '../../pages/taxForm/taxFormInterface';
const getTaxFormConfig = (instance: IPublicClientApplication, accounts: AccountInfo[], taxForm: string, year: string): Promise<taxFormConfigDataType> => {
    return new Promise<taxFormConfigDataType>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTaxFormConfig}?form=${taxForm}&year=${year}`, instance, accounts, "GET").then((response: any) => {

                resolve(response.data);
            }).catch(() => {
                reject([]);

            })

        }
        catch (ex) {
            return reject(ex);
        }
    });

}
const getCheckboxData = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string, taxForm: string, year: string): Promise<taxFormDataType> => {
    return new Promise<taxFormDataType>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getCheckboxData}${clientId}?form=8949&year=2022`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data)
            }).catch((err: any)=> {
               reject(err);
            })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const updateFormData = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string, taxFormFinalData: taxFormDataType): Promise<taxFormDataType> => {
    return new Promise<taxFormDataType>((resolve, reject) => {
        try {
            //axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.updateTaxFormData}${clientId}`, instance, accounts, "POST").then((response: any) => {

            resolve(taxFormConstants.checkboxData);

            // }).catch(() => {
            //    resolve([]);

            // })

        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const getSectionTableData = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string, sectionId: string, page: number, pageSize: number): Promise<taxformTableDataResponseType> => {
    return new Promise<taxformTableDataResponseType>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getSectionTableData}${clientId}?form=8949&sectionId=${sectionId}&year=2022&start_index=${page}&size=${pageSize}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data)
            }).catch((err: any)=> {
               reject(err);
            })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
export default { getTaxFormConfig, getCheckboxData, updateFormData, getSectionTableData }