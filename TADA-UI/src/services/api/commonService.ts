import { AccountInfo, IPublicClientApplication } from '@azure/msal-browser';
import axios from 'axios';
import getAccessToken from '../azure/accessToken'
/**
 * Call to server is abstracted by the below function. It
 * uses Fetch API to call the API server, the below method
 * returns Promises only.
 */

function axiosClient(endpoint: string, instance: IPublicClientApplication, accounts: AccountInfo[], type: string, body?: any): any {
    return new Promise<any>((resolve, reject) => {
        try {
            let headers = {
                "Content-Type": "application/json",
                Accept: body ? "application/json" : "",
                "Authorization": ""
            };
            getAccessToken(instance, accounts).then((accessToken) => {
                headers.Authorization = `Bearer ${accessToken}`;
                if (type == "GET") {
                    resolve(axios.get(endpoint, { headers }))
                }
                else if (type == "POST") {
                    resolve(axios.post(endpoint, body, { headers }))
                }
                else if (type == "PUT") {
                    resolve(axios.put(endpoint, body, { headers }))
                }
                else if (type == "DELETE") {
                    resolve(axios.delete(endpoint,{headers:headers,data:body}))
                }
            }).catch(error => {
                reject([]);
            });
        }
        catch (ex) {
            reject(ex);
        }
    });
}

export { axiosClient };