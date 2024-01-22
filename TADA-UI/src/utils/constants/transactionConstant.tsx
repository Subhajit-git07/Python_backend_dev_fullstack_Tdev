import { ColumnsType } from 'antd/lib/table';
import { Tooltip } from 'antd';
import React from 'react';
import {transactionDataType,dataTypeOptions} from '../../pages/transactions/transactionsInterface'
import moment from 'moment';


const transactionsColumns: ColumnsType<transactionDataType> = [
  {
    title: () => <Tooltip title='Token'>Token</Tooltip>,
    dataIndex: 'Token',
    key: 'Token',
    showSorterTooltip: false,
    sorter: (a, b) => a.Token.length -b.Token.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Token.indexOf(value) === 0,
  
  },
  {
    title: () => <Tooltip title='Wallet Address'>Wallet Address</Tooltip>,
    dataIndex: 'Wallet',
    showSorterTooltip: false,
    key: 'Wallet',
    sorter: (a, b) => a.Wallet-b.Wallet,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Wallet === value,
  },
  {
    title: () => <Tooltip title='Transaction Hash'>Transaction Hash</Tooltip>,
    dataIndex: 'TxHash',
    key: 'TxHash',
    showSorterTooltip: false,
    sorter: (a, b) => a.TxHash - b.TxHash,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TxHash === value,
  },
  {
    title: () => <Tooltip title='From'>From</Tooltip>,
    dataIndex: 'From',
    key: 'From',
    showSorterTooltip: false,
    sorter: (a, b) => a.From - b.From,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.From === value,
  },

  {
    title: () => <Tooltip title='To'>To</Tooltip>,
    dataIndex: 'To',
    key: 'To',
    showSorterTooltip: false,
    sorter: (a, b) => a.To - b.To,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.To === value,
  },
  

  {
    title: () => <Tooltip title='Transaction Description'>Transaction Description</Tooltip>,
    dataIndex: 'TransactionDesc',
    key: 'TransactionDesc',
    showSorterTooltip: false,
    sorter: (a, b) => a.TransactionDesc.length -b.TransactionDesc.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TransactionDesc.indexOf(value) === 0,
  
  },
  {
    title: () => <Tooltip title='Transaction Direction'>Transaction Direction</Tooltip>,
    dataIndex: 'TxDirection',
    key: 'TxDirection',
    showSorterTooltip: false,
    sorter: (a, b) => a.TxDirection.length -b.TxDirection.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TxDirection.indexOf(value) === 0,
  
  },
  {
    title: () => <Tooltip title='Amount'>Amount</Tooltip>,
    dataIndex: 'Amount',
    key: 'Amount',
    showSorterTooltip: false,
    sorter: (a, b) => a.Amount.length -b.Amount.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Amount.indexOf(value) === 0,
  
  },
  {
    title: () => <Tooltip title='Price'>Price</Tooltip>,
    dataIndex: 'Price',
    key: 'Price',
    showSorterTooltip: false,
    sorter: (a, b) => a.Price.length - b.Price.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Price == value,
  },
  {
    title: () => <Tooltip title='Date'>Date</Tooltip>,
    dataIndex: 'TimeStamp',
    showSorterTooltip: false,
    key: 'TimeStamp',
    sorter: (a, b) =>moment(a.TimeStamp).diff(b.TimeStamp),
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TimeStamp == value,
    render : (value: string)=>value?moment(value).format("LLL"):"",
  }
]


const transactionsColumnsDownload: any = [
  {
   // title: () => <Tooltip title='Token'>Token</Tooltip>,
    title:"Token",
    dataIndex: 'Token',
    key: 'Token',
    showSorterTooltip: false,
    sorter: (a: { Token: string | any[]; }, b: { Token: string | any[]; }) => a.Token.length -b.Token.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { Token: string | any[]; }) => record.Token.indexOf(value) === 0,
  
  },
  {
    title:"Wallet Address",
   // title: () => <Tooltip title='Wallet Address'>Wallet Address</Tooltip>,
    dataIndex: 'Wallet',
    showSorterTooltip: false,
    key: 'Wallet',
    sorter: (a: { Wallet: number; }, b: { Wallet: number; }) => a.Wallet-b.Wallet,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { Wallet: any; }) => record.Wallet === value,
  },
  {
    title:"Wallet Address",
    //title: () => <Tooltip title='Transaction Hash'>Transaction Hash</Tooltip>,
    dataIndex: 'TxHash',
    key: 'TxHash',
    showSorterTooltip: false,
    sorter: (a: { TxHash: number; }, b: { TxHash: number; }) => a.TxHash - b.TxHash,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { TxHash: any; }) => record.TxHash === value,
  },
  {
    title:"From",
    //title: () => <Tooltip title='From'>From</Tooltip>,
    dataIndex: 'From',
    key: 'From',
    showSorterTooltip: false,
    sorter: (a: { From: number; }, b: { From: number; }) => a.From - b.From,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { From: any; }) => record.From === value,
  },

  {
    title:"To",
    //title: () => <Tooltip title='To'>To</Tooltip>,
    dataIndex: 'To',
    key: 'To',
    showSorterTooltip: false,
    sorter: (a: { To: number; }, b: { To: number; }) => a.To - b.To,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { To: any; }) => record.To === value,
  },
  

  {
    title:"Transaction Description",
   // title: () => <Tooltip title='Transaction Description'>Transaction Description</Tooltip>,
    dataIndex: 'TransactionDesc',
    key: 'TransactionDesc',
    showSorterTooltip: false,
    sorter: (a: { TransactionDesc: string | any[]; }, b: { TransactionDesc: string | any[]; }) => a.TransactionDesc.length -b.TransactionDesc.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { TransactionDesc: string | any[]; }) => record.TransactionDesc.indexOf(value) === 0,
  
  },
  {
    title:"Transaction Direction",
   // title: () => <Tooltip title='Transaction Direction'>Transaction Direction</Tooltip>,
    dataIndex: 'TxDirection',
    key: 'TxDirection',
    showSorterTooltip: false,
    sorter: (a: { TxDirection: string | any[]; }, b: { TxDirection: string | any[]; }) => a.TxDirection.length -b.TxDirection.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { TxDirection: string | any[]; }) => record.TxDirection.indexOf(value) === 0,
  
  },
  {
    title:"Amount($)",
   // title: () => <Tooltip title='Amount'>Amount</Tooltip>,
    dataIndex: 'Amount',
    key: 'Amount',
    showSorterTooltip: false,
    sorter: (a: { Amount: string | any[]; }, b: { Amount: string | any[]; }) => a.Amount.length -b.Amount.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { Amount: string | any[]; }) => record.Amount.indexOf(value) === 0,
  
  },
  {
    title:"Price($)",
   // title: () => <Tooltip title='Price'>Price</Tooltip>,
    dataIndex: 'Price',
    key: 'Price',
    showSorterTooltip: false,
    sorter: (a: { Price: string | any[]; }, b: { Price: string | any[]; }) => a.Price.length - b.Price.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { Price: any; }) => record.Price == value,
  },
  {
    title:"Date",
    //title: () => <Tooltip title='Date'>Date</Tooltip>,
    dataIndex: 'TimeStamp',
    showSorterTooltip: false,
    key: 'TimeStamp',
    sorter: (a: { TimeStamp: moment.MomentInput; }, b: { TimeStamp: moment.MomentInput; }) =>moment(a.TimeStamp).diff(b.TimeStamp),
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record: { TimeStamp: any; }) => record.TimeStamp == value,
    render : (value: string)=>value?moment(value).format("LLL"):"",
  }
]
const typeOptions: dataTypeOptions[] = [
  {
    value: 'Price',
    name: 'Price',
  },
  {
    value: 'Amount',
    name: 'Amount',
  },
]
const dummyTransactionData:transactionDataType[]=
[
  {
      "Wallet": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "TxHash": 0xfb40d61fffe44c02625ae6f29314afdccbbeed0b83169f30591f8796702ea5da,
      "From": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "To": 0x4df4ea4b23875b4b81ba0e20fd99702f2c90faa9,
      "Token": "ETH",
      "TransactionDesc": "D-Transfer ETH",
      "TxDirection": "OUT",
      "Amount": "0.030004294759398756",
      "Price": "138.7",
      "TimeStamp": new Date("2022-07-21T01:49:52Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "TxHash": 0x4a541bad396f526df6641014b798f4bcd36aba8055c4740e173f75324dbe4327,
      "From": 0xf66852bc122fd40bfecc63cd48217e88bda12109,
      "To": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "Token": "ETH",
      "TransactionDesc": "Transfer ETH",
      "TxDirection": "IN",
      "Amount": "0.02960315",
      "Price": "146.8",
      "TimeStamp": new Date("2022-07-14T11:40:27Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "TxHash": 0x70465383954a18abee983ec97d2c6b16854456c021d4d44d22a0c20896131395,
      "From": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "To": 0x243c18573ae24213d5ea7b7a859a11a92f8ab56e,
      "Token": "USDT",
      "TransactionDesc": "TRANSFER OUT USDT",
      "TxDirection": "OUT",
      "Amount": "4558.369927",
      "Price": "104.66",
      "TimeStamp": new Date("2022-06-09T07:05:31Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "TxHash": 0xdba61192214feacfeb34e0f38d29acb1215552b4bdf83aa3e0eb55a2d530d5c2,
      "From": 0xd0451f62be92c2e45dbafbf0a9aa5fd42f1798ea,
      "To": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "Token": "ETH",
      "TransactionDesc": "Transfer ETH",
      "TxDirection": "IN",
      "Amount": "0.001812504330529875",
      "Price": "260.94",
      "TimeStamp": new Date("2022-06-08T05:53:39Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "TxHash": 0x4b03ddb6251e701629d6b715f9dddbe2a4b380832d88f5f1bc00c7cd4a4931ca,
      "From": 0x00f27d7678d7fe5c2b21a5310811deed3873ff6e,
      "To": 0x7aeed6182c01bfc9c47e8b03b48e58c38491dc54,
      "Token": "USDT",
      "TransactionDesc": "TRANSFER IN USDT",
      "TxDirection": "IN",
      "Amount": "4558.369927",
      "Price": "138.72",
      "TimeStamp": new Date("2022-06-08T00:55:12Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0xac584d7bc8d89d61f8d5617a547db1c95ac69d0c,
      "TxHash": 0xd688586a40eb8d3477b3b87d0f35de262ac51e45451d1a7222aba7321fdd9ef8,
      "From": 0xac584d7bc8d89d61f8d5617a547db1c95ac69d0c,
      "To": 0x4df4ea4b23875b4b81ba0e20fd99702f2c90faa9,
      "Token": "ETH",
      "TransactionDesc": "Transfer ETH",
      "TxDirection": "OUT",
      "Amount": "0.688097196231389",
      "Price": "183.88",
      "TimeStamp": new Date("2022-07-21T01:49:52Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0xac584d7bc8d89d61f8d5617a547db1c95ac69d0c,
      "TxHash": 0xade3e25c1cea825536a170fc829a71dc3ec074b34c742225ca62a7d9b82333ac,
      "From": 0x1b72e17551c8d76a6c7ea2967dc421838f6b9099,
      "To": 0xac584d7bc8d89d61f8d5617a547db1c95ac69d0c,
      "Token": "ETH",
      "TransactionDesc": "Transfer ETH",
      "TxDirection": "IN",
      "Amount": "0.67904234",
      "Price": "151.07",
      "TimeStamp":new Date( "2022-07-21T00:48:27Z"),
      "iconName": "",
      "assetType": ""
  },
  {
      "Wallet": 0xac584d7bc8d89d61f8d5617a547db1c95ac69d0c,
      "TxHash": 0x2f38f8c6a093638ff963c907321009fec6ad981615772ed983380f71da11c70e,
      "From": 0x9092a2df5a6eb23da6b8044e0e35cba366bb9643,
      "To": 0xac584d7bc8d89d61f8d5617a547db1c95ac69d0c,
      "Token": "ETH",
      "TransactionDesc": "Transfer ETH",
      "TxDirection": "IN",
      "Amount": "0.0092433",
      "Price": "55.12",
      "TimeStamp": new Date("2022-05-09T21:48:31Z"),
      "iconName": "",
      "assetType": ""
  }
]
export default {  transactionsColumns,typeOptions,transactionsColumnsDownload,dummyTransactionData}
