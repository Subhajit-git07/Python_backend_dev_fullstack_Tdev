import { AccountInfo, InteractionRequiredAuthError, IPublicClientApplication } from "@azure/msal-browser";
import { useMsal } from "@azure/msal-react";
import { authConfig } from "../../utils/config";

function getAccessToken(instance:IPublicClientApplication,accounts:AccountInfo[], scope?:string[]) {
    return new Promise<string>((resolve, reject)=>{
    if (accounts.length > 0) {
        const request = {
            scopes: scope ? scope : authConfig.scopes,
            account: accounts[0]
        };
        try {
             instance.acquireTokenSilent(request).then((token)=>{
                 resolve(token.accessToken)
             });
        }
        catch (error) {
            // acquireTokenSilent can fail for a number of reasons, fallback to interaction
            if (error instanceof InteractionRequiredAuthError) {
                 instance.acquireTokenPopup(request).then((token)=>{
                     resolve(token.accessToken)
                 });
            }
        };
    }
})
}

export default getAccessToken