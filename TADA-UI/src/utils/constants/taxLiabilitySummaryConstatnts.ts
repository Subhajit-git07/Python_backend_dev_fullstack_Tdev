import barChartDataType from '../../components/common/charts/barChart/barChartInterface'
import {TaxLiabilitySummary} from '../../pages/taxLiabilitySummary/taxLiabilitySummaryInterface';

let barChartData = {
  "fifoTotalTax": 90.00056,
  "lifoTotalTax": 195.88368022839998,
  "hifoTotalTax": 340.82669677240006
}

const options = {
  indexAxis: 'y' as const,
  elements: {
    bar: {
      borderWidth: 2,
    },
  },
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: true,
      text: 'Tax Liability Summary',
    },
  },
}

export default { barChartData, options,}
