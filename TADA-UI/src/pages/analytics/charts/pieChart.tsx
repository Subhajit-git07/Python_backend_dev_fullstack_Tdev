import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Pie } from '@ant-design/plots';
import { getRndIntegerBetWeen } from '../../../utils/helper';
import { Card } from 'antd';
import PinMenu from './pinMenu';

const AnalyticsPie = () => {
    const data = [
        {
          holding: "ETH",
          sales: getRndIntegerBetWeen(1500,2000) ,
        },
        {
            holding: 'USDT',
          sales: getRndIntegerBetWeen(2000,2200) ,
        },
        {
            holding: 'AVL',
          sales: getRndIntegerBetWeen(1000,1400) ,
        },
        {
            holding: 'MSG',
          sales: getRndIntegerBetWeen(2500,3000) ,
        },
        {
            holding: 'BIT',
          sales: getRndIntegerBetWeen(1000,1300) ,
        },
        {
            holding: 'MAD',
          sales: getRndIntegerBetWeen(1400,1600) ,
        },
        {
            holding: 'APE',
          sales:  getRndIntegerBetWeen(2000,2400) ,
        },
        {
            holding: 'ODE',
          sales:  getRndIntegerBetWeen(300,1400) ,
        },
      ];
  const config = {
    appendPadding: 10,
    data,
    angleField: 'sales',
    colorField: 'holding',
    height:300,
    radius: 0.75,
    innerRadius:.6,
    label: {
      type: 'spider',
      labelHeight: 28,
      content: '{name}\n{percentage}',
    },
    interactions: [
      {
        type: 'element-selected',
      },
      {
        type: 'element-active',
      },
    ],
  };
  return (
    <Card title="Holdings by percentage" className='tada-shadow' extra={<PinMenu name="HoldingsByPercentage" size={3} />}>
    <div className="col-12 pt-3 pb-5"><Pie {...config} /></div></Card>)
};

export default AnalyticsPie
