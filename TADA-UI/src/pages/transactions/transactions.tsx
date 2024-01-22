import React, { useState, useEffect } from 'react'
import {
  Breadcrumb,
  Button,
  Card,
  Col,
  Collapse,
  Pagination,
  Row,
  Select,
  Table,
  Tabs,
} from 'antd'
import transactionsDomain from './transactionsDomain'
import { Link } from 'react-router-dom'
import LineChart from '../../components/common/charts/lineChart/lineChart'
import { ArrowDownOutlined, ArrowUpOutlined, DownloadOutlined, LoadingOutlined } from '@ant-design/icons'
import { Spin } from 'antd'
import LoadingOverlay from 'react-loading-overlay-ts'
import { isEmpty, numberIntoCurrency, setImagePath } from '../../utils/helper'
import { Excel } from 'antd-table-saveas-excel'
import { transactionDataType } from './transactionsInterface'
import { height } from '@mui/system'

const { Option } = Select
const { Panel } = Collapse

const antIcon = (
  <LoadingOutlined
    style={{
      fontSize: 30,
    }}
    spin
  />
)
const Transaction = () => {
  const [transactionsData, setTransactionsData] = useState<transactionDataType[]>([])
  const [functionCount, setFunctionCount] = useState(0)

  const {
    allTransactions,
    tableTransactions,
    paginatedTransactions,
    tokenCollapseChange,
    paginationChange,
    transactionsColumns,
    handleChangeTransactions,
    transactionTableLoader,
    pagination,
    selectedTab,
    setSelectedTab,
    typeOptions,
    setSelectedType,
    selectedType,
    uniqueTokens,
    selectedToken,
    setSelectedToken,
    financialYear,
    setfinancialYear,
    transactionsColumnsDownload
  } = transactionsDomain()

  useEffect(() => {
    if (paginatedTransactions.length > 0) {
      if (functionCount == 0) {
        paginatedTransactions.map((items: { children: any }) => {
          setTransactionsData((prevState) => [...prevState, ...items.children])
        })
        setFunctionCount(functionCount + 1)
      }
    }
  }, [paginatedTransactions])

  const downloadExcelReport = () => {
    const excel = new Excel()
    excel
      .setTHeadStyle({ background: "bcbcbc", fontName: "Calibri", fontSize: 11 })
      .setRowHeight(8)
      .setTBodyStyle({ fontName: "Calibri", fontSize: 11 })
      .addSheet('TransactionsReport')
      .addColumns(transactionsColumnsDownload)
      .addDataSource(transactionsData, {
        str2Percent: true,
      })
      .saveAs('TransactionsReport.xlsx')
  }
  return (
    <>
      <LoadingOverlay
        active={transactionTableLoader}
        spinner={
          <Spin
            tip="Transaction details are loading please wait..."
            indicator={antIcon}
            style={{ color: '#FFE600' }}
          />
        }
      >
        <div className="container content-wrapper">
          <div className="mb-2 row">
            <div className="col-12 p-0 align-items-center">
              <div aria-label="Breadcrumb" className="d-flex breadcrumb-item ">
                <Breadcrumb separator="›" aria-label="breadcrumb">
                  <Breadcrumb.Item>
                    {' '}
                    <Link color="inherit" to="/TADA/profileSummary">
                      Profile Summary
                    </Link>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item> Transactions</Breadcrumb.Item>
                </Breadcrumb>
              </div>
            </div>
            <div className="col-md-12 p-0">
              {/*grid-margin*/}
              <div className="d-flex mb-3  align-items-center">
                <div className="col-7 pl-0 mt-3">
                  <h4 className="font-weight-bold mb-0">Transactions</h4>
                </div>
                <div className="col-1 dropdown dropdown--single-select yearDropdon fyTransaction" style={{ margin: '17px' }}>
                  <Select
                    showSearch
                    defaultValue={financialYear}
                    onChange={(value) => {
                      setfinancialYear(value)
                    }}
                    placeholder="Financial Year"
                    allowClear
                    className="dropdown-toggle"
                  >
                    <Option key="2022">2022</Option>
                    <Option key="2021">2021</Option>
                    <Option key="2020">2020</Option>
                  </Select>
                </div>
                <div className="col-4 float-right">
                  <button
                    className="m-2 btn btn--progress btn--progress-secondary"
                    title="Button"
                    onClick={downloadExcelReport}
                    style={{ verticalAlign: 'initial' }}
                  >
                    Get Report
                    <DownloadOutlined style={{ fontSize: '14px', padding: '7px', verticalAlign: 'initial' }} />
                  </button>
                  <Link to="/TADA/addtransactions/wallet">
                    {' '}
                    <button
                      className="btn btn--progress btn--primary"
                      title="Button"
                      style={{ margin: '23px' }}
                    >
                      Add Transaction
                    </button>
                  </Link>
                </div>
              </div>
            </div>
            <div className="card col-12 mt-3">
              <div className="card-body">
                <div className="col-12">
                  <nav
                    className="navigation-bar-tertiary"
                    id="navigation-bar-tertiary"
                  >
                    <ul>
                      <li>
                        <button
                          className={`navigation-bar-tertiary__nav-link ${selectedTab == '1' ? 'active' : ''
                            }`}
                          onClick={() => setSelectedTab('1')}
                        >
                          {' '}
                          Day{' '}
                        </button>
                      </li>
                      <li>
                        <button
                          className={`navigation-bar-tertiary__nav-link ${selectedTab == '2' ? 'active' : ''
                            }`}
                          onClick={() => setSelectedTab('2')}
                        >
                          Week
                        </button>
                      </li>
                      <li>
                        <button
                          className={`navigation-bar-tertiary__nav-link ${selectedTab == '3' ? 'active' : ''
                            }`}
                          onClick={() => setSelectedTab('3')}
                        >
                          {' '}
                          Month{' '}
                        </button>
                      </li>
                      <li>
                        <button
                          className={`navigation-bar-tertiary__nav-link ${selectedTab == '4' ? 'active' : ''
                            }`}
                          onClick={() => setSelectedTab('4')}
                        >
                          {' '}
                          Year{' '}
                        </button>
                      </li>
                      <li>
                        <button
                          className={`navigation-bar-tertiary__nav-link ${selectedTab == '5' ? 'active' : ''
                            }`}
                          onClick={() => setSelectedTab('5')}
                        >
                          All time
                        </button>
                      </li>
                    </ul>
                  </nav>
                </div>
                <p className="mt-5 col-12 content-section-description"></p>
                <div className="col-12 row">
                  <div className="col-4">
                    <div className="col-12">
                      <div className=" dropdown dropdown--single-select">
                        <Select
                          showSearch
                          className="dropdown-toggle"
                          onChange={(value: any) => {
                            setSelectedToken(value)
                          }}
                          allowClear
                          value={selectedToken}
                        >
                          {uniqueTokens &&
                            uniqueTokens!.map((element, index) => (
                              <Option
                                key={index}
                                className="dropdown-item"
                                value={element}
                              >
                                {' '}
                                {element}
                              </Option>
                            ))}
                        </Select>
                        <label
                          className={`textinput-group__label ${isEmpty(selectedToken) ? '' : 'focus'
                            }`}
                          htmlFor="text-input-default7"
                        >
                          Token
                        </label>
                      </div>
                    </div>{' '}
                    <div className="col-12 pt-5">
                      <div className=" dropdown dropdown--single-select">
                        <Select
                          showSearch
                          className="dropdown-toggle"
                          placeholder="Select Type"
                          onChange={(value: any) => {
                            setSelectedType(value)
                          }}
                          allowClear
                          value={selectedType}
                          options={typeOptions}
                        />
                        <label
                          className={`textinput-group__label ${isEmpty(selectedType) ? '' : 'focus'
                            }`}
                          htmlFor="text-input-default7"
                        >
                          Type
                        </label>
                      </div>
                    </div>
                  </div>
                  <div className="col-8">
                    <LineChart
                      data={allTransactions!}
                      title={String('test')}
                      tabSelected={selectedTab}
                      selectedType={selectedType}
                      selectedToken={selectedToken}
                    />
                  </div>
                </div>
                <div className="mt-3 row col-12 transaction-header">
                 
                    <div className="col-3 bordor">Token</div>
                    <div className="col-2">CurrentRate</div>
                    <div className="col-2">Total In</div>
                    <div className="col-2">Total Out</div>
                    <div className="width10">Net Price</div>
                    <div className="width15">Net Amount</div>
                 
                </div>
                <div className="row transaction-collapse">
                  <div className="col-12 mb-3">
                    <Collapse
                      accordion
                      className="accordion full-width tada-shadow"
                      expandIconPosition="right"
                      onChange={(selected) => {
                        tokenCollapseChange(selected)
                      }}
                      activeKey={[
                        selectedToken ? selectedToken!.toString() : '',
                      ]}
                    >
                      {paginatedTransactions &&
                        paginatedTransactions!.map((eachToken) => {
                          return (
                            <Panel
                              header={
                                <div className="accordion__title row">
                                  {' '}
                                  {
                                    <span className="col-3 pl-0 collapse-token">
                                      <img
                                        style={{ maxHeight: 25 }}
                                        className="img-icon"
                                        src={setImagePath(
                                          `${eachToken.Token!.toLocaleLowerCase()}`,
                                          eachToken.Token,
                                        )}
                                      />
                                      {eachToken.Token}
                                    </span>
                                  }
                                  <span className="col-2">

                                    <label className={`currentRate ${eachToken.currentRate > 0.5 ? 'red' : 'green'}`}>{eachToken.currentRate > 0.5 ? <ArrowDownOutlined /> : <ArrowUpOutlined />}{`$${eachToken.currentRate.toFixed(4).toString()} `}</label>

                                  </span>
                                  <span
                                    className="col-2 currency-font"
                                    title={String(eachToken.inPrice)}
                                  >
                                  
                                    {isEmpty(eachToken.inPrice)
                                      ? ''
                                      : numberIntoCurrency(
                                        Number(eachToken.inPrice!),
                                      )}
                                  </span>
                                  <span
                                    className="col-2 currency-font"
                                    title={String(eachToken.outPrice)}
                                  >
                                    
                                    {isEmpty(eachToken.outPrice)
                                      ? ''
                                      : numberIntoCurrency(
                                        Number(eachToken.outPrice!),
                                      )}
                                  </span>
                                  <span className='width10'>
                                    <span
                                      className={`ml-2 mt-0 mb-0 pill ${eachToken.total! >= 0
                                          ? 'pill--approved'
                                          : 'pill--failed'
                                        }`}
                                    >
                                      {eachToken.total! < 0 ? '-' : ''}
                                      {numberIntoCurrency(
                                        Number(eachToken.total!),
                                      )}
                                    </span>
                                  </span>
                                  <span className="width15 amt-pill">

                                    <span title={eachToken.totalAmount!.toString()}
                                      className={`ml-2 mt-0 mb-0 pill ${(eachToken.totalAmount)! >= 0
                                          ? 'pill--approved'
                                          : 'pill--failed'
                                        }`}
                                    >

                                      {
                                        (eachToken.totalAmount!.toString().length > 10 ? (eachToken.totalAmount!.toString().substring(0, 9) + "...") : eachToken.totalAmount!.toString())

                                      }
                                    </span>
                                  </span>
                                </div>
                              }
                              key={eachToken.key}
                            >
                              <div className="data-table-standard-container">
                                <div className="table-responsive transaction-table">
                                  <Table
                                    scroll={{ y: '230px', x: '100%' }}
                                    loading={transactionTableLoader}
                                    pagination={pagination}
                                    columns={transactionsColumns}
                                    dataSource={eachToken.children}
                                    onChange={handleChangeTransactions}
                                  />
                                </div>
                              </div>
                            </Panel>
                          )
                        })}
                    </Collapse>
                  </div>
                  <div className="col-12  ">
                    <span className="float-right">
                      {' '}
                      {tableTransactions && (
                        <Pagination
                          pageSize={5}
                          onChange={paginationChange}
                          total={tableTransactions!.length}
                        />
                      )}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </LoadingOverlay>
    </>
  )
}
export default Transaction
