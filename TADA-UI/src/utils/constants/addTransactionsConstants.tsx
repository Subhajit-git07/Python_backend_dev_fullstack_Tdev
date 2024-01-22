import { Tooltip } from 'antd';
import React from 'react'
import type { ColumnsType } from 'antd/lib/table/interface';
import DataTypeWallets from '../../components/walletAddress/addWalletAddressInterface';
import { DataTypeExchanges } from "../../components/addExchange/addExchangeInterface";
import addManualllyDataType from "../../components/addManually/addManuallyInterface";
import moment from 'moment';

const columnsWallets: ColumnsType<DataTypeWallets> = [
  {
    title: 'Blockchain',
    showSorterTooltip: false,
    dataIndex: 'chain',
    key: 'chain',
    sorter: (a, b) => a.chain!.length - b.chain!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.chain!.indexOf(value) === 0,
  },
  {
    title: 'Wallet Address',
    showSorterTooltip: false,
    dataIndex: 'address',
    key: 'address',
    sorter: (a, b) => a.address!.length - b.address!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.address!.indexOf(value) === 0,
  },
  {
    title: 'Status',
    showSorterTooltip: false,
    dataIndex: 'status',
    key: 'status',
    sorter: (a, b) => a.status!.length - b.status!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.status!.indexOf(value) === 0,
  },
  {
    title: 'Action',
    dataIndex: '',
    key: 'action',
    //render: (text: string, row) => (row.status == "Empty" ? <span></span> : <DeleteOutlined style={{ fontSize: "150%"}} />)
  }
]

const exchangeOptions = [
  'Karken','Ethereum'
]

const addManuallyColumns: ColumnsType<addManualllyDataType> = [

  {
    title: () => <Tooltip title='Wallet Address'>Wallet Address</Tooltip>,
    showSorterTooltip: false,
    dataIndex: 'Wallet',
    key: 'Wallet',
    sorter: (a, b) => a.Wallet!.length - b.Wallet!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Wallet!.indexOf(value) === 0,
  },
  {
    title: () => <Tooltip title='Transaction Hash'>Transaction Hash</Tooltip>,
    showSorterTooltip: false,
    dataIndex: 'TxHash',
    key: 'TxHash',
    sorter: (a, b) => a.TxHash!.length - b.TxHash!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TxHash!.indexOf(value) === 0,
  },
  {
    title: () => <Tooltip title='From'>From</Tooltip>,
    showSorterTooltip: false,
    dataIndex: 'From',
    key: 'From',
    sorter: (a, b) => a.From!.length - b.From!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.From!.indexOf(value) === 0,
  },
  {
    title: () => <Tooltip title='To'>To</Tooltip>,
    dataIndex: 'To',
    showSorterTooltip: false,
    key: 'To',
    sorter: (a, b) => a.To!.length - b.To!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.To!.indexOf(value) === 0,
  },
  {
    title: () => <Tooltip title='Token'>Token</Tooltip>,
    dataIndex: 'Token',
    showSorterTooltip: false,
    key: 'Token',
    sorter: (a, b) => a.Token!.length - b.Token!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Token!.indexOf(value) === 0,
  },
  {
    title: () => <Tooltip title='Transaction Description'>Transaction Description</Tooltip>,
    dataIndex: 'TransactionDesc',
    showSorterTooltip: false,
    key: 'TransactionDesc',
    sorter: (a, b) => a.TransactionDesc!.length - b.TransactionDesc!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TransactionDesc! == value,
  },
  {
    title: () => <Tooltip title='Transaction Direction'>Transaction Direction</Tooltip>,
    dataIndex: 'TxDirection',
    showSorterTooltip: false,
    key: 'TxDirection',
    sorter: (a, b) => a.TxDirection!.length - b.TxDirection!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TxDirection! == value,
  },
  {
    title: () => <Tooltip title='Amount'>Amount</Tooltip>,
    dataIndex: 'Amount',
    showSorterTooltip: false,
    key: 'Amount',
    sorter: (a, b) => a.Amount!.length - b.Amount!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Amount! == value,
  },
  {
    title: () => <Tooltip title='Price'>Price</Tooltip>,
    dataIndex: 'Price',
    showSorterTooltip: false,
    key: 'Price',
    sorter: (a, b) => a.Price!.length - b.Price!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Price == value,
  },
  {
    title: () => <Tooltip title='Date'>Date</Tooltip>,
    dataIndex: 'TimeStamp',
    showSorterTooltip: false,
    key: 'TimeStamp',
    sorter: (a, b) => moment(a.TimeStamp).diff(b.TimeStamp),
    ellipsis: true,
    filterSearch: true,
    render: (value: string) => moment(value).format("LLL"),
    onFilter: (value: any, record) => record.TimeStamp == value,
  }
];

const columnsExchange: ColumnsType<DataTypeExchanges> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    sorter: (a, b) => a.name!.length - b.name!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.name!.indexOf(value) === 0,
  },
  {
    title: 'Api Key',
    showSorterTooltip: false,
    dataIndex: 'apiKey',
    key: 'apiKey',
    sorter: (a, b) => a.apiKey!.length - b.apiKey!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.apiKey!.indexOf(value) === 0,
  },

  // {
  //   title: 'Api Password',
  //   showSorterTooltip: false,
  //   dataIndex: 'apiPass',
  //   key: 'apiPass',
  //   sorter: (a, b) => a.apiPass!.length - b.apiPass!.length,
  //   ellipsis: true,
  //   filterSearch: true,
  //   onFilter: (value: any, record) => record.apiPass!.indexOf(value) === 0,
  // },
  {
    title: 'Status',
    showSorterTooltip: false,
    dataIndex: 'status',
    key: 'status',
    sorter: (a, b) => a.status!.length - b.status!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.status!.indexOf(value) === 0,
  },
  {
    title: 'Action',
    dataIndex: '',
    key: 'action',
  }
]

const walletsData=[
  {
    address:"test1",
    chain: "Ethereum",
    status: "complete",
},

{
  address:"test2",
  chain: "Avalanche",
  status: "complete",
},
]

const exchangeData=[
  {
    apiKey: "test1234",
    apiPass: "test123",
    name: "Bitcoin",
    status: "incomplete"
  },
  {
    apiKey: "test546",
    apiPass: "test123",
    name: "Binance",
    status: "incomplete"
  },
]

const walletOptions=[
  "Ethereum","Avalanche"
]


export default { exchangeOptions, addManuallyColumns, columnsExchange,
   columnsWallets,walletsData,exchangeData,walletOptions }
