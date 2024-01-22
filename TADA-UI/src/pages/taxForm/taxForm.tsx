import React, { useEffect, useState } from 'react'
import { Breadcrumb, Collapse, Modal, Popconfirm, Table } from 'antd'
import { Link, useLocation } from 'react-router-dom';
import { LoadingOutlined } from '@ant-design/icons';
import UserInfo from '../../components/userInfo/userInfo';
import Checkbox from '../../components/common/checkbox/checkbox';
import taxFormDomain from './taxFormDomain';
import EditableTable from '../../components/editableGrid/editableGrid';
import { taxFormDataType, taxFormTableDataType, taxFormTableCellDataTyoe, taxFormTableConfigDataType } from './taxFormInterface';
import commonConstants from '../../utils/constants/commonConstants';
import { isEmpty } from '../../utils/helper';
import TaxFormPreview from '../taxFormPreview/taxFormPreview';
var _ = require('lodash')
const { Panel } = Collapse
const antIcon = (
    <LoadingOutlined
        style={{
            fontSize: 30,
        }}
        spin
    />
);
const TaxForm = () => {
    const location = useLocation();
    const state = location.state as any;
    const [openPreviewModal, setOpenPreviewModal] = useState(false);
    const [taxData, setTaxData] = useState<taxFormDataType>();
    const { isSubmitData, updateFinalData, taxFormData, taxFormFinalData, onSaveButtonClick, onSubmitButtonClick } = taxFormDomain();

    useEffect(() => {
        setTaxData(taxFormData)
    }, [taxFormData])


    return (
        <div className="container content-wrapper">
            <div className="mb-2 row">
                <div className="col-12 p-0 align-items-center">
                    <div aria-label="Breadcrumb" className="d-flex breadcrumb-item ">
                        <Breadcrumb separator="›" aria-label="breadcrumb">
                            <Breadcrumb.Item> <Link color="inherit" to="/TADA/profileSummary">
                                Profile Summary
                            </Link></Breadcrumb.Item>
                            <Breadcrumb.Item> <Link color="inherit" to="/TADA/viewtaxliability">
                                Tax Summary
                            </Link></Breadcrumb.Item>
                            <Breadcrumb.Item> Tax Form</Breadcrumb.Item>
                        </Breadcrumb>
                    </div>
                </div>
                <div className="col-md-12 p-0">{/*grid-margin*/}
                    <div className="d-flex mb-3  align-items-center">
                        <div className="col-8 pl-0 mt-3">
                            <h4 className="font-weight-bold mb-0">{`Tax Form  /   ${commonConstants.taxform.type} : ${state && state.taxFormData && state.taxFormData.taxFormType}  /  ${commonConstants.taxform.year} : ${state && state.taxFormData && state.taxFormData.year} `}</h4>
                        </div>
                        <div className="col-3 pl-0 mt-3">

                        </div>
                        <div className="col-3 pl-0 mt-3">

                        </div>
                    </div>
                </div>
                <div className="col-md-12 taxForm">
                    <UserInfo />
                    <Collapse accordion className="accordion  tada-shadow" expandIconPosition="right"
                        defaultActiveKey={[(taxFormData && taxFormData.sections && taxFormData.sections.length > 0) ? taxFormData.sections[0].sectionId : ""]}
                    // defaultActiveKey={["8b909d8b-4308-4de0-b62b-77f5a62f26a5"]}
                    >
                        {taxData && taxData!.sections.map((eachSection) => {

                            return (<Panel header={<div className="accordion__title"> {eachSection.sectionName }{eachSection.part?(" (" + eachSection.part + ")"):""}

                            </div>} key={eachSection.sectionId} >
                                <div className='taxFormPanel' key={eachSection.sectionId}>
                                    {eachSection.description && <> <p data-test-id="description" className="taxFormDescription">{eachSection.description}</p>
                                        <hr />
                                    </>}
                                    {eachSection.instruction && <>
                                        <p data-test-id="instruction" className='taxFormInstruction'>{eachSection.instruction}</p>
                                        <hr />
                                    </>}
                                    <Checkbox config={eachSection.checkBoxConfig} data={eachSection.checkBoxData} updateFinalData={updateFinalData} sectionId={eachSection.sectionId} isDisabled={false} />

                                    <EditableTable columns={eachSection.tableConfig} data={_.cloneDeep(eachSection.tableData)} updateFinalData={updateFinalData} sectionId={eachSection.sectionId}></EditableTable>

                                </div>

                            </Panel>)
                        })}

                    </Collapse>
                </div>
                <div className="col-md-12 d-flex pt-4">
                    <div className="col-md-9 backbtn">
                        <Link to="/TADA/viewtaxliability">
                            <button data-testid="back" className="btn btn--progress btn--progress-secondary" title="Button">Back</button></Link>
                    </div>
                    <div className="col-md-3 saveSubButton">
                        <button data-testid="Preview" className="float-right btn btn--progress btn--primary" title="Button"
                            onClick={() => setOpenPreviewModal(true)}
                        >Preview</button>
                        {/* <Popconfirm
                                //style={{paddingLeft:"637px"}}
                                title="This form Cannot be edited once Submitted.Are You sure you want to Submit this form?"
                                onConfirm={onSubmitButtonClick}
                                okText="Submit"
                                cancelText="Cancel"
                            > <button data-testid="submit" className="float-right btn btn--progress btn--primary" title="Button"> Submit</button>
                            </Popconfirm>     */}
                        <button data-testid="save" className="float-right btn btn--progress btn--primary" title="Button" onClick={onSaveButtonClick}> Save</button>
                    </div>
                </div>

            </div>
            <Modal
                centered
                visible={openPreviewModal}
                onOk={() => setOpenPreviewModal(false)}
                onCancel={() => setOpenPreviewModal(false)}
                width={1100}
                destroyOnClose={true}
                closeIcon={false}
                okButtonProps={{
                    style: {
                        display: "none",
                    },
                }}
                cancelButtonProps={{
                    style: {
                        display: "none",
                    },
                }}
            >
                <TaxFormPreview
                    isSubmitData={isSubmitData}
                    taxformAllData={taxData}
                    state={state}
                    updateFinalData={updateFinalData}
                    setOpenPreviewModal={setOpenPreviewModal}
                    onSubmitButtonClick={onSubmitButtonClick} />
            </Modal>
        </div>
    );
}
export default TaxForm


