const paginationOptions:string[]= ['5','10','15', '20','25', '30','35', '40']
const defaultPagination={
    current: 1,
    pageSize: 5,
    pageSizeOptions: paginationOptions,
    showSizeChanger: true
  }
const columnName={
    "coin":"coin",
    "asset": "asset",
    "name":"name",
    "chain":"chain",
    "Asset":"Asset",
    "totalValue":"totalValue",
    "Price":"Price",
    "price":"price",
    "amount":"amount",
    "action":"action",
    "token":"Token",
    "exchange":"exchange",
    "apiPass":"apiPass",
    "Action":"Action",
    "Timestamp":"TimeStamp"
}
const status={
    "WalletStatus":"New",
    "startClassificationStatus":"processing",
    "taxSummaryStatus":"completed",
    "walletStatusComplete":"complete",
    "walletStatusIncomplete":"incomplete"
}
const taxform={
    "name":"Client Name",
    "identificationNumber":"Security ID",
    "formType":"Tax Form Type",
    "year":"Year",
    "type":"Type",
}
const DummyDataUsed={
    "taxSummaryData": false,
    "addWalletAddress":false,
    "addExchange":false,
    "taxValues":false,
    "holdings":false,
    "classification":false,
    "transactionData":false,
    "addManual":false,
}
export default{ defaultPagination,paginationOptions,columnName,status,taxform,DummyDataUsed}