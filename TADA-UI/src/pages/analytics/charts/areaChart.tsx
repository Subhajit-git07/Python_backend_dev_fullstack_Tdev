import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Area, Line } from '@ant-design/plots';
import { Card, Statistic, Tooltip } from 'antd';
import PinMenu from './pinMenu';

const AnalyticsArea = () => {
    const [data, setData] = useState([
        {
            "Date": "2010-01",
            "price": 8934
        },
        {
            "Date": "2011-01",
            "price": 7834
        },
        {
            "Date": "2012-01",
            "price": 9834
        },
        {
            "Date": "2013-01",
            "price": 10382
        },
        {
            "Date": "2014-01",
            "price": 13892
        },
        {
            "Date": "2015-01",
            "price": 14343
        },
        {
            "Date": "2016-01",
            "price": 12000
        },
        {
            "Date": "2017-01",
            "price": 16372
        },
        {
            "Date": "2018-01",
            "price": 17000
        },
        {
            "Date": "2019-01",
            "price": 18400
        },
        {
            "Date": "2020-01",
            "price": 18000
        },
        {
            "Date": "2021-01",
            "price": 19204
        },
        {
            "Date": "2022-01",
            "price": 20093
        },




    ]);

    const config = {
        data,
        xField: 'Date',
        yField: 'price',
        height: 60,
        line: { color: '#2E2E38' },
        color: '#FFE600',
        xAxis: false,
        yAxis: false
    };

    return (
        <Card title="Current Price" className='tada-shadow' extra={<PinMenu name="CurrentPrice" size={3} />} >
                     
            <div className="card ">
                <div className="card-body">
                    <div className="col-12 row">
                        <div className="col-10">
                            <Statistic title="" value={20093} />
                        </div>
                        <div className="col-2 ">
                            <Tooltip title="Current Price of Wallet">
                                <i className="tasks material-icons text-center" > info_outlined_icon </i>
                            </Tooltip>
                        </div>
                    </div>
                    <div className="col-12 mt-3">

                        <Area {...config} />
                    </div>
                    <div className=" col-12 horizondal-line mt-2"></div>
                    <div className=" row mt-2">

                        <div className="col-6">Avg Price</div>
                        <div className="col-6">15934</div>

                    </div>

                </div>
            </div>
      </Card>
    )
};


export default AnalyticsArea