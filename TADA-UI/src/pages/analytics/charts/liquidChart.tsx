import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Liquid } from '@ant-design/plots';
import PinMenu from './pinMenu';
import { Card } from 'antd';

const AnalyticsLiquid = () => {
  let percentage = Math.random()
  const config = {
    percent: percentage,
    height: 250,
    outline: {
      border: 4,
      distance: 8,
    },
    wave: {
      length: 128,
    },
    color: () => { return percentage > .5 ? 'red' : 'green' }

  };
  return (<Card title="Taxable Holdings" className='tada-shadow' extra={<PinMenu name="TaxableHoldings" size={3} />}>
    <div className="col-12 pt-3 pb-5"><Liquid {...config} /></div></Card>);
};

export default AnalyticsLiquid
