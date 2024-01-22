const BCATColumns=[
    {
    title: 'Date - Acquired',
    dataIndex: 'dateAcquired',
      key: 'Date - Acquired',
  },
  {
    title: 'Exchange',
    dataIndex: 'exchange',
      key: 'Exchange',
  },
  {
    title: 'Buy',
    dataIndex: 'buy',
      key: 'Buy',
  },
  {
    title: 'Sell',
    dataIndex: 'sell',
      key: 'Sell',
  },
  {
    title: 'Buy Quantity',
    dataIndex: 'buyQuantity',
      key: 'Buy Quantity',
  },
  {
    title: 'Sell Quantity',
    dataIndex: 'sellQuantity',
      key: 'Sell Quantity',
  },
  {
    title: 'Fee',
    dataIndex: 'fee',
      key: 'Fee',
  },
  {
    title: 'Fee Currency',
    dataIndex: 'feeCurrency',
    key: 'Fee Currency',
  }]
  
  const BCATData=[{
      key: '1',
      dateAcquired: '02/23/2019 04:41:19',
      exchange: 'Kraken',
      buy: 'USD',
      sell:'BTC',
      buyQuantity:5000,
      sellQuantity:0.7,
      fee:0,
      feeCurrency:'USD'
  },
  {
    key: '2',
    dateAcquired: '02/23/2019 04:41:19',
    exchange: 'Coinbase',
    buy: 'USD',
    sell:'BTC',
    buyQuantity:5000,
    sellQuantity:0.7,
    fee:0,
    feeCurrency:'USD'
  },
  {
    key: '3',
    dateAcquired: '02/23/2019 04:41:19',
    exchange: 'Poloniex',
    buy: 'SC',
    sell:'BTC',
    buyQuantity:678.996,
    sellQuantity:0.00196908,
    fee:0.000049,
    feeCurrency:'USD'
  }]

  export default {BCATColumns,BCATData}