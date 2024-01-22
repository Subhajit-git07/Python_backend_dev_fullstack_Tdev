import React from 'react'
import { Breadcrumb, Select } from 'antd'
import { Link } from 'react-router-dom'
import taxFormDocDomain from './taxFormDocDomain';
// @ts-ignore
import TaxForm8949 from "../../assets/TaxForms/TaxForm8949.pdf"
const { Option } = Select;

const documents = () => {
const {setTaxFormData,taxFormData}=taxFormDocDomain();
  return (
    <div className="container content-wrapper">
      <div className="mb-2 row">
        <div className="col-12 p-0 align-items-center">
          <div aria-label="Breadcrumb" className="d-flex breadcrumb-item ">
            <Breadcrumb separator="›" aria-label="breadcrumb">
              <Breadcrumb.Item>
                {' '}
                <Link color="inherit" to="/TADA/profileSummary">
                  Profile Summary
                </Link>
              </Breadcrumb.Item>
              <Breadcrumb.Item>Documents</Breadcrumb.Item>
            </Breadcrumb>
          </div>
        </div>
        <div className="col-md-12 pt-5">
        <div className="dropdown dropdown--single-select">
            <div className="yearDropdon docTopButtons">
            <Select showSearch
                data-testid="financialYear"
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
              data-testid="taxFormType"
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
              <a href={TaxForm8949} download> <button data-testid="downloadBtn" disabled={taxFormData.year == "" || taxFormData.taxFormType == ""} className="float-right  btn btn--progress btn--primary generateButton" title="Button">Download Tax Form</button></a>
            </div>
        </div>
      </div>
    </div>
  )
}

export default documents
