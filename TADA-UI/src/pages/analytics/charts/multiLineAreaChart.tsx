import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Area, Line } from '@ant-design/plots';
import { ECDH } from 'crypto';
import { getRndIntegerBetWeen } from '../../../utils/helper';
import { Card } from 'antd';
import PinMenu from './pinMenu';

const AnalyticsMultiLineArea = () => {
    const [data, setData] = useState<any[]>([]);
    var monthNameList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let tokens = ["ETH", "BIT", "USDT",  "APE" ]
    useEffect(() => {
        let Data: any[] = [];
        monthNameList.map(eachMonth => {
            tokens.map(eachToken => {
                Data.push({ "token": eachToken, "month": eachMonth, "holding": getRndIntegerBetWeen(0, 1000) })
            })
        })
        setData(Data);
    }, [])

    const config = {
        data,
        xField: 'month',
        height:250,
        yField: 'holding',
        seriesField: 'token',
        point: {
            size: 3,
            shape: 'cicle',
          
        },
    };

    return     (  <Card title="Current Holdings" className='tada-shadow' extra={<PinMenu name="CurrentHoldings" size={3} />}>
    <div className="col-12 pt-3 pb-5"><Line {...config} /></div></Card>)
};

export default AnalyticsMultiLineArea
