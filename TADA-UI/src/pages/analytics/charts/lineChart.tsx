import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Line } from '@ant-design/plots';
import { getRndIntegerBetWeen } from '../../../utils/helper';
import PinMenu from './pinMenu';
import { Card } from 'antd';

const AnalyticsLine = () => {
    const [selectedTab, setSelectedTab] = useState<string>("1");
    const data = [
        {
            year: 'Jan',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Feb',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Mar',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Apr',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'May',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Jun',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Jul',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Aug',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Sep',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Oct',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Nov',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Dec',
            txDirection: "In",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Jan',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Feb',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Mar',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Apr',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'May',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Jun',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Jul',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Aug',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Sep',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Oct',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Nov',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
        {
            year: 'Dec',
            txDirection: "Out",
            value: getRndIntegerBetWeen(0, 12323),
        },
    ];
    const config = {
        data,
        xField: 'year',
        yField: 'value',
        seriesField: 'txDirection',
        color: ['green', 'red'],
        label: {},
        point: {
            size: 5,
            shape: 'diamond',
            style: ({ txDirection }: any) => {
                return {
                    fill: txDirection == "In" ? "green" : "red",
                    stroke: txDirection == "In" ? "green" : "red",
                    lineWidth: 1,
                };
            },
        },
        tooltip: {
            showMarkers: false,
        },

        interactions: [
            {
                type: 'marker-active',
            },
        ],
    };
    return (
        <Card title="Transactions By Wallet" extra={<PinMenu name="TransactionByWallet" size={3} />}>
                   
    <div className="col-12">
        <div className="col-12">
            <nav
                className="navigation-bar-tertiary"
                id="navigation-bar-tertiary"
            >
                <ul>
                    <li>
                        <button
                            className={`navigation-bar-tertiary__nav-link ${selectedTab == '1' ? 'active' : ''
                                }`}
                            onClick={() => setSelectedTab('1')}
                        >
                            {' '}
                            ETH{' '}
                        </button>
                    </li>
                    <li>
                        <button
                            className={`navigation-bar-tertiary__nav-link ${selectedTab == '2' ? 'active' : ''
                                }`}
                            onClick={() => setSelectedTab('2')}
                        >
                            USDT
                        </button>
                    </li>
                    <li>
                        <button
                            className={`navigation-bar-tertiary__nav-link ${selectedTab == '3' ? 'active' : ''
                                }`}
                            onClick={() => setSelectedTab('3')}
                        >
                            {' '}
                            AVL{' '}
                        </button>
                    </li>
                    <li>
                        <button
                            className={`navigation-bar-tertiary__nav-link ${selectedTab == '4' ? 'active' : ''
                                }`}
                            onClick={() => setSelectedTab('4')}
                        >
                            {' '}
                            MSG{' '}
                        </button>
                    </li>
                    <li>
                        <button
                            className={`navigation-bar-tertiary__nav-link ${selectedTab == '5' ? 'active' : ''
                                }`}
                            onClick={() => setSelectedTab('5')}
                        >
                            BIT
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
        <div className="col-12 row analytics-transactions-grid mt-3 pb-5">
            <Line {...config} />
        </div>
    </div>
    </Card>)
};

export default AnalyticsLine
