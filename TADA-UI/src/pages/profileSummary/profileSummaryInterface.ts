export  interface taxValuesDataType {

  "taxLiability"?: number,
  "portfolioValueIn"?: number,
  "portfolioValueOut"?: number,
  "ltcg"?: number,
  "stcg"?: number,

}
export interface ComponentsProps{
  "HighestHoldings":  ()=>JSX.Element,
  "EstimatedTax": ()=> JSX.Element,
  "CurrentPrice":  ()=>JSX.Element,
  "TransactionByWallet": ()=> JSX.Element,
  "TaxSummary":  ()=>JSX.Element,
  "HoldingsByPercentage": ()=> JSX.Element,
  "TaxableHoldings":  ()=>JSX.Element,
  "CurrentHoldings":  ()=>JSX.Element,
  "TotalHoldings":  ()=>JSX.Element,
}



export default taxValuesDataType
