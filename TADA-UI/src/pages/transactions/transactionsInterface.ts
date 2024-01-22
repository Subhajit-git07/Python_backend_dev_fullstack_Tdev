export interface transactionDataType {
  Amount:string,
  From: number,
  Price:string,
  To: number,
  Token: string,
  TransactionDesc: string,
  TxDirection:string,
  TxHash:number,
  assetType: string,
  iconName: string,
  Wallet: number,
  TimeStamp:Date,
 
}
export interface transactionByTokenDataType{
  Token: string,
        key: string,
        inAmount?:string,
        outAmount?: string,
        inPrice?:string,
        outPrice?:string,
        total ?:Number,    
        totalAmount?:Number,   
        currentRate:Number,  
        // pagination:pagination,
        // From:TransactionByToken.map(item => item.From).reduce((prev, next) => (moment(prev) > moment(next))?prev:next),
        // To:TransactionByToken.map(item => item.To).reduce((prev, next) => (moment(prev) < moment(next))?prev:next),
        children: transactionDataType[]
}

export interface transactionPaginationResponse{
  "data": transactionDataType[],
  "start_index": number,
  "size": number,
  "total_count": number
}
export interface dataTypeOptions {
  name: string
  value: string
}

