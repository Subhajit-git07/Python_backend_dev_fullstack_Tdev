
import { Tooltip } from 'antd';
import moment from 'moment';
import React from 'react'
import { classificationDataType, ClassificationOptionType,ClassificationDataResponse } from "../../pages/classification/classifcationInterface";
import { numberIntoCurrency, setImagePath } from "../helper";


const classificationColumns: any = [
    {
        title: () => <Tooltip title='Transaction Direction'>Transaction Direction</Tooltip>,
        dataIndex: 'TxDirection',
        showSorterTooltip: false,
        key: 'TxDirection',
        inputType:"select",
        sorter: (a: { TxDirection: string }, b: { TxDirection: string }) => a.TxDirection.length - b.TxDirection.length,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { TxDirection: string }) => record.TxDirection.indexOf(value) === 0,
        editable: true 
    },
    {
        title: () => <Tooltip title='Wallet Address'>Wallet Address</Tooltip>,
        showSorterTooltip: false,
        dataIndex: 'Wallet',
        inputType:"text",
        key: 'wallet',
        sorter: (a: { wallet: number; },b: { wallet: number; }) => a.wallet - b.wallet,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { wallet: string }) => record.wallet === value,
          editable:true
    },
      {
        title: () => <Tooltip title='Transaction Hash'>Transaction Hash</Tooltip>,
        dataIndex: 'TxHash',
        key: 'TxHash',
        inputType:"text",
        showSorterTooltip: false,
        sorter: (a: { TxHash: number; }, b: { TxHash: number; }) => a.TxHash - b.TxHash,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { TxHash: any; }) => record.TxHash === value,
        editable: true
    },
    {
        title: () => <Tooltip title='From'>From</Tooltip>,
        showSorterTooltip: false,
        dataIndex: 'From',
        inputType:"text",
        key: 'From',
        sorter: (a: { From: number }, b: { From: number }) => a.From - b.From,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { From: string }) => record.From === value,
        editable: true
    },
    {
        title: () => <Tooltip title='To'>To</Tooltip>,
        dataIndex: 'To',
        showSorterTooltip: false,
        inputType:"text",
        key: 'To',
        sorter: (a: { To: number }, b: { To: number }) => a.To - b.To,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { To: string }) => record.To === value,
        editable: true
    },
    {
        title: () => <Tooltip title='Token'>Token</Tooltip>,
        dataIndex: 'Token',
        showSorterTooltip: false,
        inputType:"text",
        key: 'Token',
        sorter: (a: { Token: string; }, b: { Token: string; }) => a.Token.length - b.Token.length,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { Token: any; }) => record.Token == value,
        render: (text: string, row: { Token: string }) => <span><img className="tableTokenIcon" src={setImagePath(`${row.Token!.toLocaleLowerCase()}`)} />{text}</span>,
        editable: true
    },
    {
        title: () => <Tooltip title='Transaction Description'>Transaction Description</Tooltip>,
        dataIndex: 'TransactionDesc',
        showSorterTooltip: false,
        inputType:"text",
        key: 'TransactionDesc',
        sorter: (a: { TransactionDesc: string }, b: { TransactionDesc: string }) => a.TransactionDesc.length - b.TransactionDesc.length,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { TransactionDesc: string }) => record.TransactionDesc.indexOf(value) === 0,
        editable: true
    },
    {
        title: () => <Tooltip title='Date'>Date</Tooltip>,
        dataIndex: 'TimeStamp',
        showSorterTooltip: false,
        inputType:"date",
        key: 'TimeStamp',
        sorter: (a: { TimeStamp: Date }, b: { TimeStamp: Date }) => moment(a.TimeStamp).diff(b.TimeStamp),//.getTime() - b.TimeStamp.getTime(),
        ellipsis: true,
        filterSearch: true,
        render : (value: string)=>moment(value).format("LLL"),
        onFilter: (value: any, record: { TimeStamp: string }) => record.TimeStamp.indexOf(value) === 0,
        editable: true
    },
    {
        title: () => <Tooltip title='Amount'>Amount</Tooltip>,
        dataIndex: 'Amount',
        showSorterTooltip: false,
        inputType:"number",
        key: 'Amount',
        sorter: (a: { Amount: string }, b: { Amount: string }) => a.Amount.length - b.Amount.length,
        ellipsis: true,
        filterSearch: true,
        onFilter: (value: any, record: { Amount: string }) => record.Amount.indexOf(value) === 0,
        editable: true
    },
    {
        title: () => <Tooltip title='Price'>Price</Tooltip>,
        dataIndex: 'Price',
        showSorterTooltip: false,
        inputType:"number",
        key: 'Price',
        sorter: (a: { Price: string }, b: { Price: string }) => a.Price.length - b.Price.length,
        ellipsis: true,
        filterSearch: true,
        render:(text: string,) => <span title={text}>{numberIntoCurrency(Number(text))}</span>,
        onFilter: (value: any, record: { Price: string }) => record.Price.indexOf(value) === 0,
        editable: true
    },
    {
        title: 'Action',
        key: 'Action',
        fixed: 'right',
         width: 100,
        //render: () => ,
    },
];

const ClassificationOptions: ClassificationOptionType[] = [
    {

        name: 'IN',
        value: 'IN',
    },
    {
        value: 'OUT',
        name: 'OUT',
    },
    {
        value: 'N/A',
        name: 'N/A',
    }
]

const classificationData:any=
{  
    data:
    [
    {
        "Wallet": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "TxHash": "0x8d43806c746a9f489e902990f8be1433b6124e8238e9f5b5940eee038b95a554",
        "From": "0x0000000000000000000000000000000000000000",
        "To": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "Token": "KODA",
        "TransactionDesc": "BUY KODA",
        "TxDirection": "IN",
        "Amount": "1",
        "Price": "59.87",
        "id": "634e42553acef45ca4dd86ad",
        "TimeStamp": "2022-06-14T09:09:10Z",
        "iconName": null,
        "assetType": null
      },
      {
        "Wallet": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "TxHash": "0xd5abb08bfab3e07072ceeba5e81ad749dc8a58a831dda98565f75b6d8b784d2f",
        "From": "0x0000000000000000000000000000000000000000",
        "To": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "Token": "KODA",
        "TransactionDesc": "BUY KODA",
        "TxDirection": "IN",
        "Amount": "1",
        "Price": "129.23",
        "id": "634e42553acef45ca4dd86ae",
        "TimeStamp": "2022-06-07T15:04:34Z",
        "iconName": null,
        "assetType": null
      },
      {
        "Wallet": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "TxHash": "0x395473663573dafd7b06a271fed925c70cbcf7e57449e6329dd10354e6ef17ad",
        "From": "0x0000000000000000000000000000000000000000",
        "To": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "Token": "KODA",
        "TransactionDesc": "BUY KODA",
        "TxDirection": "IN",
        "Amount": "1",
        "Price": "19.79",
        "id": "634e42553acef45ca4dd86af",
        "TimeStamp": "2022-05-29T17:20:09Z",
        "iconName": null,
        "assetType": null
      },
      {
        "Wallet": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "TxHash": "0xdbf7e8249df96c334c8455fda1c66fb5a446647aad31febb07dc851dbf0f6d57",
        "From": "0x28130f3b9abaea65bb960e7ee34a22989fcfca7f",
        "To": "0xb1f44bf437380a01c80645c91d64fb04a69c0919",
        "Token": "ETH",
        "TransactionDesc": "Transfer ETH",
        "TxDirection": "OUT",
        "Amount": "0.0",
        "Price": "291.66",
        "id": "634e42553acef45ca4dd86b0",
        "TimeStamp": "2022-04-26T15:59:19Z",
        "iconName": null,
        "assetType": null
      }
    
]
}


export default { classificationColumns, ClassificationOptions, classificationData}