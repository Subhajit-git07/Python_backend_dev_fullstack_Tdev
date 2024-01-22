import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Column } from '@ant-design/plots';
import { getRndIntegerBetWeen, numberIntoCurrency } from '../../../utils/helper';
import { Card, Statistic, Tooltip } from 'antd';
import PinMenu from './pinMenu';

const AnalyticsColumn = () => {
  const data = [
    {
      holding: "ETH",
      price: getRndIntegerBetWeen(132034, 162733),
    },
    {
      holding: 'USDT',
      price: getRndIntegerBetWeen(310239, 333933),
    },
    {
      holding: 'AVL',
      price: getRndIntegerBetWeen(210239, 233433),
    },
    {
      holding: 'MSG',
      price: getRndIntegerBetWeen(879203, 893748),
    },
    {
      holding: 'BIT',
      price: getRndIntegerBetWeen(879203, 890283),
    },
    {
      holding: 'MAD',
      price: getRndIntegerBetWeen(314234, 343434),
    },
    {
      holding: 'APE',
      price: getRndIntegerBetWeen(879203, 890283),
    },
    {
      holding: 'ODE',
      price: getRndIntegerBetWeen(87920, 89083),
    },
  ];
  const config = {
    data,
    xField: 'holding',
    yField: 'price',
    height: 60,
    color: '#FFE600',
    xAxis: false,
    yAxis: false,
  };
  return (<Card title="Highest Holdings" className='tada-shadow' extra={<PinMenu name="HighestHoldings" size={3} />}>
  <div className="card ">
    <div className="card-body">
      <div className="col-12 row">
        <div className="col-10">
          <Statistic title="" value={numberIntoCurrency(893748)} />
        </div>
        <div className="col-2 ">
          <Tooltip title="Highest Holdings details">
            <i className="tasks material-icons text-center" > info_outlined_icon </i>
          </Tooltip>
        </div>
      </div>
      <div className="col-12 mt-3">

        <Column {...config} />
      </div>
      <div className=" col-12 horizondal-line mt-2"></div>
      <div className=" row mt-2">

        <div className="col-6">Total Gain</div>
        <div className="col-6">12 %</div>

      </div>

    </div>
  </div></Card>)
};

export default AnalyticsColumn
