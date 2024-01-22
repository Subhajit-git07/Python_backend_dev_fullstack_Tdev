import { CaretDownOutlined, CaretUpOutlined } from '@ant-design/icons'
import { Card, Statistic, Tooltip } from 'antd'
import React, { useState } from 'react'
import { numberIntoCurrency } from '../../../utils/helper'
import PinMenu from './pinMenu'

 const TotalHoldings=()=>{
    return(  <Card title="Total Holdings" className='tada-shadow' extra={<PinMenu name="TotalHoldings" size={3} />}>
    <div className="card ">
<div className="card-body">
    <div className="col-12 row">
        <div className="col-10">
            <Statistic title="" value={numberIntoCurrency(678928)} />
        </div>
        <div className="col-2 ">
            <Tooltip title="Total Holdings of wallets" placement='top'>
                <i className="tasks material-icons text-center" > info_outlined_icon </i>
            </Tooltip>
        </div>
    </div>
    <div className="col-12 row mt-3 analytics-holding">
        <div className=" col-8">
            <div className="weekly" title="" >
                <span>Weekly
                    <span className="percentage">12%</span>
                </span>
                <span className="red float-right">
                    <CaretDownOutlined />
                </span>
            </div>
            <div className="weekly" title="" >
                <span>Daily
                    <span className="percentage">14%</span>
                </span>
                <span className="green float-right">
                    <CaretUpOutlined />
                </span>
            </div>
        </div>
    </div>
    <div className=" col-12 horizondal-line mt-2"></div>
    <div className=" row mt-2">

        <div className="col-6">Today</div>
        <div className="col-6">{numberIntoCurrency(23434)}</div>

    </div>

</div>
</div></Card>)
 }
 export default TotalHoldings
