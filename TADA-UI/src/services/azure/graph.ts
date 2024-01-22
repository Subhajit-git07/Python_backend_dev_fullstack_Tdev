import { IPublicClientApplication, AccountInfo } from "@azure/msal-browser";
import axios from "axios";
import { graphConfig } from "../../utils/apiConfig";
import getAccessToken from "./accessToken";


export async function callMsGraphUserPhoto(instance: IPublicClientApplication, accounts: AccountInfo[]) {
    function manageErrors(response:Response) { //input promise by fetch()
    if (!response.ok) {
      throw Error(response.statusText)
       }
    return response;
  }
    return new Promise<any>((resolve, reject) => {
        const headers = {};
        getAccessToken(instance, accounts, ["user.read"]).then((accessToken) => {
            const bearer = `Bearer ${accessToken}`;
            let headers = {
                "Content-Type": "image/jpg",
                 "responseType" : "arraybuffer",
                "Authorization": bearer
            };
            const options = {
                method: "GET",
                headers: headers
            };
            try {
                axios.get(graphConfig.graphMeEndpoint + graphConfig.getPhoto, { headers })

              //  fetch(graphConfig.graphMeEndpoint + graphConfig.getPhoto, options)
              
                  .then(response => {
                        if (!(response.statusText == "Not Found")) {
                            fetch(graphConfig.graphMeEndpoint + graphConfig.getPhotoValue, options)
                                .then(response => {
                                    resolve(response)
                                })
                                .catch(error => {
                                    reject(error)
                                });
                        }
                    })
                    .catch(error => {
                        reject(error)
                    });

            } catch (err) {
                console.log(err)
            }
        }).catch(error => {
            reject(error)
        });
    });
}

