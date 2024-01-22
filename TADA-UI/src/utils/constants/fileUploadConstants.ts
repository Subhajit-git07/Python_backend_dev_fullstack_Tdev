
import { DataTypeFileUpload, DataTypeOptions } from "../../components/fileUpload/fileUploadInterface";
import type { ColumnsType } from 'antd/lib/table/interface';
import moment from "moment";

const columnsTransactions: ColumnsType<DataTypeFileUpload> = [

  {
    title: 'Wallet',
    dataIndex: 'Wallet',
    key: 'Wallet',
    sorter: (a, b) => a.Wallet!.length - b.Wallet!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Wallet!.indexOf(value) === 0,
  },
  {
    title: 'TxHash',
    dataIndex: 'TxHash',
    key: 'TxHash',
    sorter: (a, b) => a.TxHash!.length - b.TxHash!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TxHash!.indexOf(value) === 0,
  },
  {
    title: 'From',
    dataIndex: 'From',
    key: 'From',
    sorter: (a, b) => a.From!.length - b.From!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.From!.indexOf(value) === 0,
  },
  {
    title: 'To',
    dataIndex: 'To',
    key: 'To',
    sorter: (a, b) => a.To!.length - b.To!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.To!.indexOf(value) === 0,
  },
  {
    title: 'Token',
    dataIndex: 'Token',
    key: 'Token',
    sorter: (a, b) => a.Token!.length - b.Token!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Token!.indexOf(value) === 0,
  },
  {
    title: 'TransactionDesc',
    dataIndex: 'TransactionDesc',
    key: 'TransactionDesc',
    sorter: (a, b) => a.TransactionDesc!.length - b.TransactionDesc!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TransactionDesc! == value,
  },
  {
    title: 'Transaction Direction',
    dataIndex: 'TxDirection',
    key: 'TxDirection',
    sorter: (a, b) => a.TxDirection!.length - b.TxDirection!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.TxDirection! == value,
  },
  {
    title: 'Amount',
    dataIndex: 'Amount',
    key: 'Amount',
    sorter: (a, b) => a.Amount!.length - b.Amount!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Amount! == value,
  },
  {
    title: 'Price',
    dataIndex: 'Price',
    key: 'Price',
    sorter: (a, b) => a.Price!.length - b.Price!.length,
    ellipsis: true,
    filterSearch: true,
    onFilter: (value: any, record) => record.Price == value,
  },
  {
    title: 'Date',
    dataIndex: 'TimeStamp',
    showSorterTooltip: false,
    key: 'TimeStamp',
    sorter: (a, b) => moment(a.TimeStamp).diff(b.TimeStamp),
    ellipsis: true,
    filterSearch: true,
    render: (value: string) => moment(value).format("LLL"),
    onFilter: (value: any, record) => record.TimeStamp == value,
  }
]

export default { columnsTransactions }
