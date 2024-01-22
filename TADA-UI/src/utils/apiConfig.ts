
const Endpoints = {
    local: {
        apiService: "https://api-tada.azurewebsites.net/api/v1/"
    },
    dev: {
        
    }
}
//https://testapiv1.azurewebsites.net/holdings/afd6f3c1-4310-49b7-b5ae-a3dd3f6cbc27
const serviceEndpoints = Endpoints.local

const apiEndpoints = {
    getClientCountries:"client/countries/",
    getClientStates:"client/cities/",
    getClient:"client/",
    putClient:"client/",
    deleteClient:"client/",
    postClient:"client/",
    deleteWallet:"wallets/",
    getExchangeOptions:"exchanges/names/",
    addExchange:"exchanges/exchange/",
    getExchanges:"exchanges/exchange/",
    deleteExchanges:"exchanges/exchange/",
    getBlockChainsOptions:"wallets/blockchains/",
    getCurrentWallets:"wallets/",
    getClients:"profileSummary/clientNames/",
    getTaxValues:"profileSummary/taxValues/",
    getHoldings:"profileSummary/holdings/",
    getTransactions: "transactions/AllTransactions/", 
    startClassification:"classification/start/",
    getClassificationStatus:"classification/status/",
    getUnClassifiedData:"classification/unclassifiedTxs/",
    putUnclassifiedData:"classification/unclassifiedTxs/",
    postManaulTransaction:"transactionsManual/",
    getTaxSummary:"classification/taxSummary/",
    getTaxSummaryStatus:"classification/taxSummaryStatus/",
    getTaxFormConfig:"forms/config",
    getCheckboxData:"forms/checkbox/",
    updateTaxFormData:"taxforms/",
    getSectionTableData:"forms/table/" 
}
const graphConfig = {
    graphMeEndpoint: "https://graph.microsoft.com/v1.0/me",
    getPhoto:"/photo",
    getPhotoValue:"/photo/$value"
};
export {serviceEndpoints,apiEndpoints,graphConfig}