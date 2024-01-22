import { AccountInfo, IPublicClientApplication } from "@azure/msal-browser";
import {ClassificationDataResponse, classificationDataType }from "../../pages/classification/classifcationInterface";
import { apiEndpoints, serviceEndpoints } from "../../utils/apiConfig";
import { axiosClient } from "./commonService";
import commonConstants from "../../utils/constants/commonConstants";
import classificationConstants from "../../utils/constants/classificationConstants";

const getClassificationStatus=(instance:IPublicClientApplication,accounts:AccountInfo[], clientId: string):Promise<{status:string,message:string}>=>{
    return new Promise<{status:string,message:string}>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClassificationStatus}${clientId}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data)
            }).catch((err: any)=> {
                reject(err);
            })
          //  resolve({status:Math.random()>0.6?"Completed":"In Progress",message:""})
        }
        catch (ex) {
            return reject(ex);
        }
    });
}

const getClassificationData = (instance:IPublicClientApplication,accounts:AccountInfo[], clientId: string,page:number,pageSize:number): Promise<ClassificationDataResponse> => {
    return new Promise<ClassificationDataResponse>((resolve, reject) => {
        try {
            if(commonConstants.DummyDataUsed.classification == true){
                resolve(classificationConstants.classificationData)
            }else{
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getUnClassifiedData}${clientId}?start_index=${page}&size=${pageSize}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data)
            }).catch((err: any)=> {
               reject(err);
            })
        }
        }
        catch (ex) {
            return reject(ex);
        }
    });
}

const saveClassifiedData = (instance:IPublicClientApplication,accounts:AccountInfo[], clientId: string,classifiedData:classificationDataType): Promise<classificationDataType> => {
    return new Promise<classificationDataType>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.putUnclassifiedData}${clientId}`, instance, accounts, "PUT",classifiedData).then((response: any) => {
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
export default { getClassificationData,saveClassifiedData,getClassificationStatus}


