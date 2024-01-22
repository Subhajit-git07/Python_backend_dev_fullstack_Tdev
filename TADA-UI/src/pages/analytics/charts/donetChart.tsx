import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Pie } from '@ant-design/plots';
import { getRndIntegerBetWeen, numberIntoCurrency } from '../../../utils/helper';
import { Card, Statistic, Tooltip } from 'antd';
import PinMenu from './pinMenu';

const AnalyticsDonet = () => {
  const data = [
    {
      type: 'STCG',
      value: getRndIntegerBetWeen(100,130),
    },
    {
      type: 'LTCG',
      value: getRndIntegerBetWeen(10,45),
    },
  
  ];
  const config = {
    height: 60,
    data,
    angleField: 'value',
    colorField: 'type',
    radius: 1,
    color:['#2E2E38','#FFE600'],
    innerRadius: 0.6,
    label:false,
    statistic:false,
   
    
    
  };
  return (   <Card title="Estimated Tax" className='tada-shadow' extra={<PinMenu name="EstimatedTax" size={3} />}>
                     
    <div className="card ">
                            <div className="card-body">
                                <div className="col-12 row">
                                    <div className="col-10">
                                        <Statistic title="" value={numberIntoCurrency(166)} />
                                    </div>
                                    <div className="col-2 ">
                                        <Tooltip title="Estimated Tax for Holdings">
                                            <i className="tasks material-icons text-center" > info_outlined_icon </i>
                                        </Tooltip>
                                    </div>
                                </div>
                                <div className="col-12 mt-3">

                                <Pie {...config} />
                                </div>
                                <div className=" col-12 horizondal-line mt-2"></div>
                                <div className=" row mt-2 analytics-donet-footer">

                                    <div className="col-3 ">STCG</div>
                                    <div className="col-3 pad5">{numberIntoCurrency(123)}</div>
                                    <div className="col-3 pad5">LTCG</div>
                                    <div className="col-3 pad5">{numberIntoCurrency(43)}</div>

                                </div>

                            </div>
                        </div>
                        </Card>
  ) 
};

export default AnalyticsDonet
