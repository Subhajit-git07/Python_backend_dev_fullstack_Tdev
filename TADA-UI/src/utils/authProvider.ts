import { authConfig } from "./config";

// Config object to be passed to Msal on creation
export const msalConfig = {
    auth: {
        authority: authConfig.auth.authority,
        clientId: authConfig.auth.clientId,
        postLogoutRedirectUri: window.location.origin,
        redirectUri: window.location.origin+"/TADA",
    }
}