import React, { useEffect, useState } from 'react';

import {
  Select
} from 'antd'
import { Link } from 'react-router-dom';
import Portfolio from '../../components/portfolio/portfolio';
import EstimatedTaxLiability from '../../components/estimatedTaxLiability/estimatedTaxLiability';
import { LoadingOutlined } from '@ant-design/icons';
import { Spin } from 'antd';
import LoadingOverlay from 'react-loading-overlay-ts';
import Holdings from '../../components/holdings/holdings';
import profileSummaryDomain from './profileSummaryDomain';
import { PinMenuProps } from '../analytics/analyticsInterface';
import AnalyticsColumn from '../analytics/charts/columnChart'
import AnalyticsDonet from '../analytics/charts/donetChart'
import AnalyticsArea from '../analytics/charts/areaChart'
import AnalyticsLine from '../analytics/charts/lineChart'
import AnalyticsBar from '../analytics/charts/barChart'
import AnalyticsPie from '../analytics/charts/pieChart'
import AnalyticsLiquid from '../analytics/charts/liquidChart'
import AnalyticsMultiLineArea from '../analytics/charts/multiLineAreaChart'
import TotalHoldings from '../analytics/charts/totalHoldings'
import { ComponentsProps } from './profileSummaryInterface';

const { Option } = Select;
 
const Components:ComponentsProps = {
  "HighestHoldings": AnalyticsColumn,
  "EstimatedTax": AnalyticsDonet,
  "CurrentPrice": AnalyticsArea,
  "TransactionByWallet": AnalyticsLine,
  "TaxSummary": AnalyticsBar,
  "HoldingsByPercentage": AnalyticsPie,
  "TaxableHoldings": AnalyticsLiquid,
  "CurrentHoldings": AnalyticsMultiLineArea,
  "TotalHoldings": TotalHoldings,
}
const antIcon = (
  <LoadingOutlined
    style={{
      fontSize: 30,
    }}
    spin
  />
);
const ProfileSummaryPage = () => {
  const { taxValues, loaderTaxValue, setPSYear, psYear } = profileSummaryDomain();
  const myPreferences: PinMenuProps[] = JSON.parse(localStorage.getItem("MyPreferences")!)
  const [holdingLoader, setholdingLoader] = useState(true);

  const setHoldingLoader = (holdingStatus: boolean | ((prevState: boolean) => boolean)) => {
    setholdingLoader(holdingStatus)
  }

  return (
    <LoadingOverlay
      active={loaderTaxValue && holdingLoader}
      spinner={<Spin tip="Data is loading Please wait..."
        indicator={antIcon}
        style={{ color: "#FFE600" }}
      />}
    >
      <div className="container content-wrapper">
        <div className="mb-2 row">
          <div className="col-md-12">
            <div className="d-flex   align-items-center">
              <div className="col-9 mt-3">
                <h4 className="font-weight-bold mb-0">Profile Summary</h4>
              </div>
              <div className="dropdown dropdown--single-select yearDropdon">
                <Select showSearch
                  defaultValue={psYear.year}
                  onChange={(value) => { setPSYear({ ...psYear, year: value }) }}
                  placeholder="Financial Year"
                  allowClear
                  className="dropdown-toggle"
                >
                  <Option key="2022">2022</Option>
                  <Option key="2021">2021</Option>
                  <Option key="2020">2020</Option>
                </Select>
              </div>
              <Link to='/TADA/viewtaxliability'>   <button className="ml-3 btn btn--progress btn--progress-secondary" title="Button"> View Tax
                Liability</button>
              </Link>
            </div>
          </div>
        </div>

        <div className="row " >
          <div className="col-md-6 ">
            <Portfolio />
          </div>
          <div className="col-md-6 ">

            <EstimatedTaxLiability             />
          </div>
        </div>
        {/* <div className="row mt-4">
          {myPreferences && myPreferences.length > 0 && myPreferences.map((eachPreferences) => {

            const countryName: any = eachPreferences.name;
            if (typeof Components[countryName as keyof ComponentsProps] !== "undefined") {
               
              return ( <div className="col-md-6 ">
                {React.createElement(Components[countryName as keyof ComponentsProps], {})}
                </div>)
            }})}

        </div> */}

        <Holdings setHoldingLoader={setHoldingLoader} />
      </div>
    </LoadingOverlay>
  )
}

export default ProfileSummaryPage