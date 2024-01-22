import { axiosClient } from './commonService'
import { serviceEndpoints, apiEndpoints } from '../../utils/apiConfig'
import DataTypeWallets, { WalletResponseDataType } from '../../components/walletAddress/addWalletAddressInterface';
import addTransactionsConstants from '../../utils/constants/addTransactionsConstants';
import { transactionDataType } from '../../pages/transactions/transactionsInterface';
import { AnyListenerPredicate } from '@reduxjs/toolkit/dist/listenerMiddleware/types';
import addManualllyDataType from '../../components/addManually/addManuallyInterface';
import { DataTypeExchanges } from '../../components/addExchange/addExchangeInterface';
import { DataTypeFileUpload } from '../../components/fileUpload/fileUploadInterface';
import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import commonConstants from '../../utils/constants/commonConstants';

const getBlockChainsOptions = (instance: IPublicClientApplication, accounts: AccountInfo[]): Promise<string[]> => {
    return new Promise<string[]>((resolve, reject) => {
        try {
            if (commonConstants.DummyDataUsed.addWalletAddress
                || commonConstants.DummyDataUsed.addManual) {
                resolve(addTransactionsConstants.walletOptions)
            } else {
                axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getBlockChainsOptions}`, instance, accounts, "GET").then((response: any) => {
                    resolve(response.data)
                }).catch(() => {
                    resolve([]);
                })
            }
            // resolve(addTransactionsConstants.dataWallets);
        }
        catch (ex) {
            return reject(ex);
        }
    });
}

const getExchangeOptions = (instance: IPublicClientApplication, accounts: AccountInfo[]): Promise<string[]> => {
    return new Promise<string[]>((resolve, reject) => {
        try {
            if (commonConstants.DummyDataUsed.addExchange == true) {
                resolve(addTransactionsConstants.exchangeOptions)
            } else {
                axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getExchangeOptions}`, instance, accounts, "GET").then((response: any) => {
                    resolve(response.data)
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

const getCurrentWallets = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string): Promise<DataTypeWallets[]> => {
    return new Promise<DataTypeWallets[]>((resolve, reject) => {
        try {
            if (commonConstants.DummyDataUsed.addWalletAddress == true) {
                resolve(addTransactionsConstants.walletsData)
            } else {
                axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getCurrentWallets}${clientId}`, instance, accounts, "GET").then((response: any) => {
                    resolve(response.data)
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

const saveAddManuallyData = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string, addManualData: addManualllyDataType): Promise<addManualllyDataType> => {
    return new Promise<addManualllyDataType>((resolve, reject) => {
        try {
            if (commonConstants.DummyDataUsed.addManual) {
                resolve(addManualData)
            }
            else {
                axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.postManaulTransaction}${clientId}`, instance, accounts, "POST", addManualData).then((response: any) => {
                    resolve(response.data)
                }).catch((error: any) => {
                    reject(error);
                })
            }
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const getAllExchanges = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string): Promise<DataTypeExchanges[]> => {
    return new Promise<DataTypeExchanges[]>((resolve, reject) => {
        try {
            if (commonConstants.DummyDataUsed.addExchange == true) {
                resolve(addTransactionsConstants.exchangeData)
            } else {
                axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getExchanges}${clientId}`, instance, accounts, "GET").then((response: any) => {
                    resolve(response.data)
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
const addNewExchange = (instance: IPublicClientApplication, accounts: AccountInfo[], exchangeData: any, clientId: string): Promise<DataTypeExchanges> => {
    return new Promise<DataTypeExchanges>((resolve, reject) => {
        try {
            // return axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTransactions}}`,token)
            // resolve(addTransactionsConstants.dataTransactions);
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.addExchange}${clientId}`, instance, accounts, "POST", exchangeData).then((response: any) => {
                // resolve(response.data)
                resolve(response.data)
            }).catch((err: any) => {
                reject("Error in adding new exchange")
            })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const addTransactionDetails = (token: string, transactionData: DataTypeFileUpload[]): Promise<DataTypeFileUpload[]> => {
    return new Promise<DataTypeFileUpload[]>((resolve, reject) => {
        try {
            // return axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getTransactions}}`,token)
            resolve(transactionData);
        }
        catch (ex) {
            return reject(ex);
        }
    });
}
const addNewWallet = (instance: IPublicClientApplication, accounts: AccountInfo[], newWallet: any, clientId: string): Promise<WalletResponseDataType> => {
    return new Promise<WalletResponseDataType>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.getCurrentWallets}${clientId}`, instance, accounts, "POST", newWallet).then((response: any) => {
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

const deleteWallet = (instance: IPublicClientApplication, accounts: AccountInfo[], deletedWalletData: DataTypeWallets, clientId: string): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            return axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.deleteWallet}${clientId}`, instance, accounts, "DELETE", deletedWalletData).then((response: any) => {
                resolve(response.data.message)
            }).catch((err: any) => {
                reject("Error in delete")
                // resolve(addTransactionsConstants.dataWallets.filter(wallet => wallet.address != deletedWallet.address || wallet.chain != deletedWallet.chain));
            })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}

const deleteExchange = (instance: IPublicClientApplication, accounts: AccountInfo[], exchangeId: string, clientId: string): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            return axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.deleteExchanges}${clientId}?exchangeId=${exchangeId}`, instance, accounts, "DELETE").then((response: any) => {
                resolve(response.data)
            }).catch((err: any) => {
                reject("Error in delete")
                // resolve(addTransactionsConstants.dataWallets.filter(wallet => wallet.address != deletedWallet.address || wallet.chain != deletedWallet.chain));
            })
        }
        catch (ex) {
            return reject(ex);
        }
    });
}

const startClassification = (instance: IPublicClientApplication, accounts: AccountInfo[], clientId: string): Promise<string> => {
    return new Promise<string>((resolve, reject) => {
        try {
            axiosClient(`${serviceEndpoints.apiService}${apiEndpoints.startClassification}${clientId}`, instance, accounts, "POST").then((response: any) => {
                // resolve(response.data)
                resolve(response.data.status)
            }).catch((err: any) => {
                reject("error in start classification")
            })
        }
        catch (ex) {
            reject(ex);
        }
    });
}
export default { getBlockChainsOptions, getExchangeOptions, saveAddManuallyData, getCurrentWallets, addNewWallet, deleteWallet, addTransactionDetails, addNewExchange, startClassification, getAllExchanges, deleteExchange }
