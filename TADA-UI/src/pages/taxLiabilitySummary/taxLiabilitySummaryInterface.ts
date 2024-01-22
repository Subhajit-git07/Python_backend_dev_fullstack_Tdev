export interface TaxLiabilitySummary{
  fifoTotalTax:number,
  lifoTotalTax:number,
  hifoTotalTax:number
}
export interface taxFormDataType {
    year?:string,
    taxFormType?:string
  }

export interface DataTypeBCAT {
      key:string;
      dateAcquired: string,
      exchange: string,
      buy: string,
      sell:string,
      buyQuantity:number,
      sellQuantity:number,
      fee:number,
      feeCurrency:string
  }
 
