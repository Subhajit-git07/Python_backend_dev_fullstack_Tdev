import { CaretDownOutlined, CaretUpOutlined } from '@ant-design/icons'
import { Card, Dropdown, Menu, message, Statistic, Tabs, Tooltip } from 'antd'
import React, { useState } from 'react'
import { numberIntoCurrency } from '../../utils/helper'
import AnalyticsColumn from './charts/columnChart'
import AnalyticsDonet from './charts/donetChart'
import AnalyticsArea from './charts/areaChart'
import AnalyticsLine from './charts/lineChart'
import AnalyticsBar from './charts/barChart'
import AnalyticsPie from './charts/pieChart'
import AnalyticsLiquid from './charts/liquidChart'
import AnalyticsMultiLineArea from './charts/multiLineAreaChart'
import { PinMenuProps } from './analyticsInterface'
import { useNavigate } from 'react-router-dom'
import TotalHoldings from './charts/totalHoldings'
import Portfolio from '../../components/portfolio/portfolio';
import EstimatedTaxLiability from '../../components/estimatedTaxLiability/estimatedTaxLiability';
const fs = require('fs')
const Analytics = () => {
    return (

        <div className="container content-wrapper">
            <div className='row'>
                <div className="col-3">
                    <AnalyticsArea></AnalyticsArea>

                </div>
                <div className="col-3">
                    <TotalHoldings />

                </div>
                <div className="col-3">
                    <AnalyticsColumn></AnalyticsColumn>

                </div>
                <div className="col-3">
                    <AnalyticsDonet></AnalyticsDonet>

                </div>
            </div>
            <div className="tada-shadow mt-3">
                <AnalyticsLine></AnalyticsLine>

            </div>
            <div className="  row  mt-3">
                <div className=" col-6">
                    <Portfolio></Portfolio>
                </div>
                <div className="col-6 ">
                    <EstimatedTaxLiability></EstimatedTaxLiability>
                   
                </div>
            </div>
            <div className="  row  mt-3">
                <div className=" col-6">
                    <AnalyticsBar></AnalyticsBar>
                </div>
                <div className="col-6 ">
                    <AnalyticsPie></AnalyticsPie>
                   
                </div>
            </div>
            <div className="  row  mt-3">
                <div className=" col-8">
   <AnalyticsMultiLineArea></AnalyticsMultiLineArea>



                </div>
                <div className="col-4 ">
                     <AnalyticsLiquid></AnalyticsLiquid>
                   
                </div>
            </div>
        </div>


    )
}
export default Analytics