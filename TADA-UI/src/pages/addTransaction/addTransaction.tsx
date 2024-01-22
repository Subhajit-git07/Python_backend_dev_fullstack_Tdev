import React, { useState } from 'react'
import { Breadcrumb, Tabs } from 'antd'
import WalletAddress from '../../components/walletAddress/addWalletAddress'
import AddExchange from '../../components/addExchange/addExchange'
import AddManually from '../../components/addManually/addMaually'
import { Link, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom'
import AddTransactionDomain from './addTransactionDomain'
const { TabPane } = Tabs

const AddTransaction = () => {
  const { currentRoute,setCurrentRoute } = AddTransactionDomain();
 
  return (
    <div className="main-panel">
      <div className="container content-wrapper">
        <div className="mb-2 row">
          <div className="col-12 p-0 align-items-center">
            <div aria-label="Breadcrumb" className="d-flex breadcrumb-item ">
              <Breadcrumb separator="›" aria-label="breadcrumb">
                <Breadcrumb.Item>
                  <Link color="inherit" to="/TADA/profileSummary">
                    Profile Summary
                  </Link></Breadcrumb.Item>
                  <Breadcrumb.Item>
                  <Link color="inherit" to="/TADA/transactions">
                   Transactions
                  </Link></Breadcrumb.Item>
                <Breadcrumb.Item> Add Transactions</Breadcrumb.Item>
              </Breadcrumb>
            </div></div>
        </div>
        <div className="col-12 addTransaction-tab">
          <nav className="navigation-bar-tertiary" id="navigation-bar-tertiary">
            <ul>
              <li>
              <Link to="/TADA/addtransactions/wallet">
                <button className={`navigation-bar-tertiary__nav-link ${currentRoute=='wallet'?'active':''}`}> Add Wallet Address </button>
                </Link>
              </li>
              <li>
              <Link to="/TADA/addtransactions/exchange">
                <button className={`navigation-bar-tertiary__nav-link ${currentRoute=='exchange'?'active':''}`}>Add Exchange</button>
                </Link>
              </li>
              <li>
              <Link to="/TADA/addtransactions/manual">
                <button className={`navigation-bar-tertiary__nav-link ${currentRoute=='manual'?'active':''}`}> Add Manually </button>
                </Link>
              </li>

            </ul>
          </nav>
        </div>
        
        <Routes>
          <Route  path="wallet" element={    <WalletAddress />} />
          <Route  path="exchange" element={     <AddExchange />} />
          <Route  path="manual" element={    <AddManually />} />
        </Routes>
       
        {/* <div className="card-container"> */}
        {/* <Tabs
        activeKey={source}
        onChange={(path) => {
          navigate(`/TADA/addtransactions/${path}`); // <-- sibling path
        }}
        type="card" centered
      >
       <TabPane tab="Add Wallet Address" key="1">
            <WalletAddress />
          </TabPane>
          <TabPane tab="Add Exchange" key="2">
            <AddExchange />
          </TabPane>
          <TabPane tab="Add Manually" key="3">
            <AddManually />
          </TabPane>
      </Tabs> */}
        {/* <Tabs type="card" centered>
          <TabPane tab="Add Wallet Address" key="1">
            <WalletAddress />
          </TabPane>
          <TabPane tab="Add Exchange" key="2">
            <AddExchange />
          </TabPane>
          <TabPane tab="Add Manually" key="3">
            <AddManually />
          </TabPane>
        </Tabs> */}

        {/* </div> */}
      </div>
    </div>
  )
}
export default AddTransaction
