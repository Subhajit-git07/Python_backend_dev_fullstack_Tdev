import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Bar } from '@ant-design/plots';
import { Legend } from '@antv/g6';
import { getRndIntegerBetWeen } from '../../../utils/helper';
import { Card } from 'antd';
import PinMenu from './pinMenu';

const AnalyticsBar = () => {
  const data = [
    {
      type:"Lifo",
      value: getRndIntegerBetWeen(30,50),
    },
    {
      type: "Fifo",
      value: getRndIntegerBetWeen(40,60),
    },
    {
     type :"Hifo",
      value: getRndIntegerBetWeen(30,65),
    },
    
 
  ];
  const config = {
    data,
    xField: 'value',
    yField: 'type',
    seriesField: 'year',
    color:["#FFE600"],
    height:300,
    
  };
  return (   <Card title="Tax Summary" className='tada-shadow' extra={<PinMenu name="TaxSummary" size={3} />}>
  <div className="col-12 pt-3 pb-5"><Bar {...config} /></div></Card>);
};

export default AnalyticsBar
