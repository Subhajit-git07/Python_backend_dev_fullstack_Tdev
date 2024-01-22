const authConfiguration = {
    local: {
        auth: {
            authority: "https://login.microsoftonline.com/adb53b4f-b05f-4dcb-a2e1-9111380568c3",
            clientId: "a12876c5-a488-4e30-a6e7-de8ff640bbf5", 
        },
        scopes: ["api://857af365-fa74-4da2-a45b-9a99361cf23e/.default"],
        appInsightKey:"661fc6a8-cb2e-4a64-aaf3-da8816862397"
    },
    dev: {
        auth: {
            authority: "https://login.microsoftonline.com/adb53b4f-b05f-4dcb-a2e1-9111380568c3",
            clientId: "a12876c5-a488-4e30-a6e7-de8ff640bbf5", 
        },
        scopes: ["api://857af365-fa74-4da2-a45b-9a99361cf23e/.default"],
        appInsightKey:"661fc6a8-cb2e-4a64-aaf3-da8816862397"
    
    },

}
const authConfig = authConfiguration.local

export{ authConfig}