import { transactionByTokenDataType, transactionDataType, transactionPaginationResponse } from './transactionsInterface'
import React, { useEffect, useState } from 'react'
import getAccessToken from '../../services/azure/accessToken'
import { useMsal } from '@azure/msal-react'
import TransactionService from '../../services/api/transactionsService'
import commonConstants from '../../utils/constants/commonConstants'
import { ColumnsType, TablePaginationConfig } from 'antd/lib/table'
import { profileStore } from "../../utils/store/store";
import { useSelector } from 'react-redux'
import { ColumnFilterItem } from 'antd/lib/table/interface'
import Logger from '../../services/azure/appInsights/Logger/logger';
import { SeverityLevel } from '@microsoft/applicationinsights-web'
import { message, TableProps } from 'antd'
import { numberIntoCurrency, paginate, setImagePath } from '../../utils/helper'
import messages from '../../utils/constants/messages';
import { paginationClasses } from '@mui/material'
import transactionConstant from '../../utils/constants/transactionConstant';
import moment from 'moment'

const transactionsDomain = () => {
  const currentProfile = useSelector(profileStore);
  const [transactionTableLoader, setTransactionTableLoader] = useState<boolean>(false);
  let { instance, accounts } = useMsal()
  const [selectedTab, setSelectedTab] = useState("5");
  const [uniqueTokens, setUniqueTokens] = useState<string[]>();
  const [selectedToken, setSelectedToken] = useState<string>();
  const [allTransactions, setAllTransactions] = useState<transactionDataType[]>(
    [],
  )
  const [paginatedTransactions, setPaginatedTransactions] = useState<transactionByTokenDataType[]>([])
  const [tableTransactions, setTableTransactions] = useState<transactionByTokenDataType[]>()
  const [pagination, setPagination] = useState<TablePaginationConfig>(commonConstants.defaultPagination)
  const [selectedType, setSelectedType] = useState("Price");
  const [financialYear, setfinancialYear] = useState((new Date().getFullYear()).toString(),);
  useEffect(() => {
    currentProfile.clientId ? getTransactions(0, 500) : setAllTransactions([]);
  }, [currentProfile])
  useEffect(() => {
    getUniqueTokens();
  }, [allTransactions])
  useEffect(() => {
    getTransactionsByToken();
  }, [uniqueTokens])
  const handleChangeTransactions: TableProps<transactionDataType>['onChange'] =
    (newPagination) => {
      // getClassificationData(newPagination.current!, newPagination.pageSize!)
      setPagination({ ...newPagination })
    }
  let getTransactions = (start_index: number, size: number) => {
    setTransactionTableLoader(true);
    Logger.trackTrace({ message: "Getting transaction of selected Client", data: `id =${String(currentProfile.clientId)}`, severityLevel: SeverityLevel.Information })
    getTransactionsByPagination(start_index, size)
  }

  let transactionData: any[] = [];
  let getTransactionsByPagination = async (start: number, end: number) => {
    TransactionService.getAllTransactions(instance, accounts, currentProfile.clientId!, start, end).then(
      (response: transactionPaginationResponse) => {
        if (response != null) {
          transactionData.push(...response.data);
          setAllTransactions((prevState) => [...prevState, ...response.data])
          if (response.data.length == end) {
            getTransactionsByPagination(start + end, end)
          }
          else {
            setTransactionTableLoader(false);
            setFilters(transactionData);
          }
        }
      }).catch((err) => {
        message.warning(messages.getTransactionsError)
        Logger.trackTrace({ message: messages.getTransactionsError, data: `response =${JSON.stringify(err)}`, severityLevel: SeverityLevel.Error })
        Logger.trackException({ message: err })
        setTransactionTableLoader(false);
      })
  }
  const getUniqueTokens = () => {
    let uniquetokens = Array.from(new Set(allTransactions.map((item) => item.Token)));
    setUniqueTokens(uniquetokens);
    setSelectedToken(uniquetokens[0]);
  }

  const getTransactionsByToken = () => {
    let Transactions: transactionByTokenDataType[] = [];
    uniqueTokens && uniqueTokens!.forEach((eachToken: string) => {
      let TransactionByToken: transactionDataType[] = allTransactions.filter(eachTransaction => { return eachTransaction.Token == eachToken })
      let inPrice = TransactionByToken.filter(item => { return item.TxDirection == "IN" }).map(item => item.Price).reduce((prev, next) => (Number(prev) + Number(next)).toString(), "")
      let outPrice = TransactionByToken.filter(item => { return item.TxDirection == "OUT" }).map(item => item.Price).reduce((prev, next) => (Number(prev) + Number(next)).toString(), "")
     let inAmount=TransactionByToken.filter(item => { return item.TxDirection == "IN" }).map(item => item.Amount).reduce((prev, next) => (Number(prev) + Number(next)).toString(), "")
     let outAmount= TransactionByToken.filter(item => { return item.TxDirection == "OUT" }).map(item => item.Amount).reduce((prev, next) => (Number(prev) + Number(next)).toString(), "")
      Transactions.push({
        Token: eachToken,
        key: eachToken,
        inAmount:inAmount ,
        outAmount:outAmount,
        inPrice: inPrice,
        outPrice: outPrice,
        total: Number(inPrice) - Number(outPrice),
        totalAmount:Number(inAmount) - Number(outAmount),
        currentRate:Math.random(),
        children: TransactionByToken
      })
    })
    setTableTransactions(Transactions)
    setPaginatedTransactions(paginate(Transactions, 1, 5))
  }
  const paginationChange = (current: number, size: number) => {
    setPaginatedTransactions(paginate(tableTransactions!, current, size))
  }

  const tokenCollapseChange = (selected: string | string[]) => {
    if (selected) {
      setSelectedToken(selected.toString())
      setPagination(commonConstants.defaultPagination)
    }
    else {
      setSelectedToken("");
    }
  }
  const transactionsColumnsDownload=transactionConstant.transactionsColumnsDownload;
  const transactionsColumns = transactionConstant.transactionsColumns;
  function setFilters(response: transactionDataType[]) {
    transactionsColumns.map((eachColumn) => {
      
      let currentSet: Set<string> = new Set(response.map((data) => String(data[eachColumn.key as keyof transactionDataType])))
      let filterObj: ColumnFilterItem[] = [];
      currentSet.forEach((item: string) => {
        filterObj.push({
          text: item,
          value: item,
        })
      });
     
      eachColumn.filters = [...filterObj];
      if (eachColumn.key == commonConstants.columnName.token) {
        eachColumn.render = (text: string, row) => <span><img className="img-icon" src={setImagePath(`${row.Token!.toLocaleLowerCase()}`, row.Token)} />{text}</span>
      }
      if (eachColumn.key == commonConstants.columnName.Price) {
        eachColumn.render = (text: string, row) => text ? <span title={numberIntoCurrency(Number(text))}>{numberIntoCurrency(Number(text))}</span> : ""
      }

    })
  }
  const typeOptions = transactionConstant.typeOptions;
  return {
    allTransactions, tableTransactions, paginatedTransactions,tokenCollapseChange, paginationChange, transactionsColumns, handleChangeTransactions, transactionTableLoader,
    pagination, selectedTab, setSelectedTab, typeOptions, setSelectedType, selectedType, uniqueTokens, selectedToken, setSelectedToken,
    financialYear, setfinancialYear,transactionsColumnsDownload
  }
}
export default transactionsDomain
