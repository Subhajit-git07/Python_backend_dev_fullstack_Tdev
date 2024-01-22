import { AccountInfo, IPublicClientApplication } from "@azure/msal-browser";
import profileDataType from "../../pages/profile/profileInterface";
import { apiEndpoints, serviceEndpoints } from "../../utils/apiConfig";
import profileConstants from "../../utils/constants/profileConstants";
import { axiosClient } from "./commonService";


const getCountries = (instance: IPublicClientApplication, accounts: AccountInfo[]): Promise<string[]> => {
    return new Promise<string[]>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClientCountries}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data);
            }).catch((err: any) => {
                reject(err)
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}

const getStates = (instance: IPublicClientApplication, accounts: AccountInfo[],country:string): Promise<string[]> => {
    return new Promise<string[]>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClientStates}${country}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data);
            }).catch((err: any) => {
                reject(err)
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}

const getProfile = (instance: IPublicClientApplication, accounts: AccountInfo[], id: string): Promise<profileDataType> => {
    return new Promise<profileDataType>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClient}${id}`, instance, accounts, "GET").then((response: any) => {
                resolve(response.data);
            }).catch((err: any) => {
                reject(err)
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}
const addNewProfile = (instance: IPublicClientApplication, accounts: AccountInfo[], newProfile: profileDataType,email:string): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClient}${email}`, instance, accounts, "POST", newProfile).then((response: any) => {
                resolve(response.data)
            }).catch((err: any) => {
                reject(err)
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}
const updateProfile = (instance: IPublicClientApplication, accounts: AccountInfo[], currentProfile: profileDataType): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClient}${currentProfile.clientId}`, instance, accounts, "PUT", currentProfile).then((response: any) => {
                resolve(response.data)
            }).catch((err: any) => {
                reject(err)
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}
const deleteProfile = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId:string): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getClient}${clientId}`, instance, accounts, "DELETE").then((response: any) => {
                resolve(response.data)
            }).catch((err: any) => {
                reject(err)
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}

export default {getCountries,getStates, getProfile, addNewProfile, updateProfile, deleteProfile }