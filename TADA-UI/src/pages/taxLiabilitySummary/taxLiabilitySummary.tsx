import React, { useState } from 'react'
import { Breadcrumb,DatePicker,Select,Space} from 'antd'
import BarChart from '../../components/common/charts/barChart/barChart'
import { Link } from 'react-router-dom';
import useTaxLiabilitySummary from './useTaxLiabilitySummary';
import LoadingOverlay from 'react-loading-overlay-ts';
import { DownloadOutlined, LoadingOutlined } from '@ant-design/icons';
import { Spin } from 'antd';
import { Value } from 'node-sass';


const { Option } = Select;
const antIcon = (
    <LoadingOutlined
      style={{
        fontSize: 30,
      }}
      spin
    />
  );
const TaxLiabilitySummary = () => {
    
const {taxSummaryData,loader,loaderMessage,setTaxFormData,taxFormData,downloadBcatReport} = useTaxLiabilitySummary();

  return (
    <LoadingOverlay
    active={loader}
    spinner={<Spin tip={loaderMessage}
    indicator={antIcon} 
    style={{color:"#FFE600"}}
    />}
  >
<div className="container content-wrapper">
<div className="mb-2 row">
    <div className="col-12 p-0 align-items-center">
        <div aria-label="Breadcrumb" className="d-flex breadcrumb-item ">
            <Breadcrumb separator="›" aria-label="breadcrumb">
                <Breadcrumb.Item> <Link color="inherit" to="/TADA/profileSummary">
                    Profile Summary
                </Link></Breadcrumb.Item>
                <Breadcrumb.Item>Tax Summary</Breadcrumb.Item>
            </Breadcrumb>
        </div>
    </div>
    <div className="col-md-12 p-0">
        <div className="d-flex mb-3  align-items-center">
            <div className="col-5 pl-0 mt-3">
                <h4 className="font-weight-bold mb-0">Tax Summary</h4>
            </div>
            <div className='col-2 pr-0 float-right '>
          <button
                    className="float-right btn btn--progress btn--progress-secondary"
                    title="Button"
                    onClick={downloadBcatReport}
                    style={{verticalAlign:'initial', marginTop:'2px'}}
                  >
                    BCAT-Template
                    <DownloadOutlined style={{ fontSize: '14px', padding:'6px',verticalAlign:'initial'}}/>
          </button>
          </div>
            <div className="col-5 pr-0 float-right dropdown dropdown--single-select">
            <div className="yearDropdon taxSummaryTopButons">
            <Select showSearch
                defaultValue={taxFormData.year}
                placeholder="Financial Year"
                allowClear
                onChange={(value) => { setTaxFormData({ ...taxFormData, year: value !== undefined ? value : ''})}}
                className="dropdown-toggle"
              >
                <Option key="2022">2022</Option>
                <Option key="2021">2021</Option>
                <Option key="2020">2020</Option>
              </Select>
              </div>
              <div>
              <Select
                className="dropdown-toggle"
                onChange={(value) => { setTaxFormData({ ...taxFormData, taxFormType: value !== undefined ? value : '' })}}
                showSearch
                style={{ width: 200 }}
                placeholder="Tax Form Type"
                allowClear
              >
                <Option key="8949" value="8949">8949</Option>
              </Select>
              </div>
               <Link color="inherit" to={{pathname:"/TADA/taxform"}} state={{taxFormData}}>
              <button disabled={taxFormData.year == "" || taxFormData.taxFormType == ""} className="float-right  btn btn--progress btn--primary generateButton" title="Button">View Tax Form</button>
              </Link> 
            </div>
            
        </div>
    </div>

    <div className="card mt-3">
        <div className="card-body">
            <div className="col-12" style={{width:"1248px",height:"697"}}>
            <BarChart taxSummaryData={taxSummaryData}/>
            </div>
        </div>
    </div>

</div>
</div>
</LoadingOverlay>
  )
}

export default TaxLiabilitySummary
